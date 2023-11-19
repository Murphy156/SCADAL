import serial
from core.QT.qt_show import *

class SerialCommunication:
    def __init__(self):
        self.ser = None

    def open_ser(self, port, baudrate):
        try:
            global ser
            ser = serial.Serial(port, baudrate, timeout=0.5)
            if (ser.isOpen() == True):
                print("the serial secessfully open")
                print("port:", port, "Type:", type(port))
                print("baudrate:", baudrate, "Type:", type(baudrate))
                return True, "serial secessfully open"
            else:
                return False, "Serial open fail"
        except Exception as exc:
            return False, f"{str(exc)}"

    def close_ser(self):
        try:
            global ser
            if ser.is_open:
                ser.close()
                print("Serial port closed successfully.")
            else:
                print("Serial port is not open.")
        except Exception as exc:
            print("Error while closing serial port:", exc)

    def send_msg(self, data):
        try:
            print("Serial port is open:", ser.is_open)
            ser.write(data)
            print("data post:", data.hex())
        except Exception as exc:
            print("post err", exc)

    def read_msg(self, num_bytes_to_read):
        try:
            if ser.is_open:
                data = ser.read(num_bytes_to_read)
                return data
            else:
                print("串行端口未打开。")
                return None
        except Exception as exc:
            print("从串行端口读取数据时出现错误：", exc)
            return None

    """
    brief:创建数据包
    para1:header_code:包头数据占两个bytes
    para2：command_code：命令数据占一个bytes
    para3：parameter：参数指令，有可能是负数，所以要对参数进行判断，占4个bytes
           这里的转换过程是：
        例子：-500（0xf4\x01\x00\x00）低字节在高位
        1、先将这个二进制数（0xf4\x01\x00\x00 = 1111 0100 0000 0001 0000 0000 0000 0000）计算反码：将所有位取反（ 0000 1011 1111 1110 1111 1111 1111 1111）
        2、在反码的基础上加1（0000 1011 1111 1110 1111 1111 1111 1111 + 1 = 0000 1011 1111 1110 1111 1111 1111 1111）
        3、将补码转换成十六进制得到'0x0b\xff\xff\xff'

        所以在mcu上求'0x0b\xff\xff\xff'的补码即可
        1、反码：将每一位取反得到 0xf3\x01\x00\x00
        2、补码：反码加1得到 0xf4\x01\x00\x00
        3、将 ’0xf4\x01\x00\x00‘ 转换为十进制，得到 -500。
    para4：parity：校验位，校验1的个数
    RETURN:返回拼接的而进行数据包
    """

    def create_data_packet(self, header_code, command_code, parameter, CRC):
        try:
            header_bytes = header_code.to_bytes(2, byteorder='little')
            command_bytes = command_code.to_bytes(1, byteorder='little')
            CRC_bytes = CRC.to_bytes(2, byteorder='little')
            data_packet = header_bytes + command_bytes + parameter + CRC_bytes
            # Convert each byte to hexadecimal and join them into a string
            hex_data_packet = ''.join([f'{byte:02x}' for byte in data_packet])
            print("Data Packet in create_data_packet: ", hex_data_packet)
            return data_packet
        except Exception as e:
            print("creating data err: ", str(e))



    """
    brief: 计算CRC-16校验值（生成多项式0x8005）
    param data: 要计算CRC的数据，为bytes类型
    return: CRC-16校验值，为整数
    """

    def CalCRC_16(self, header, command, para):
        crc = 0xFFFF
        poly = 0x8005
        combined_data = header.to_bytes(2, byteorder='little') + command.to_bytes(1, byteorder='little') + para
        hex_data_packet = ''.join([f'{byte:02x}' for byte in combined_data])
        print("Data Packet in CRC: ", hex_data_packet)
        for i, byte in enumerate(combined_data):
            #            print("循环次数:", i)  # 打印循环次数
            #           print("当前处理的字节:", hex(byte))  # 打印当前处理的字节
            crc ^= (byte << 8)  # 将当前字节左移8位后与CRC异或,相当于加入了对crc的影响
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
        return crc & 0xFFFF

    """
    brief: 计算CRC-16校验值（生成多项式0x8005）(PID参数专用)
    param data: 要计算CRC的数据，为bytes类型
    return: CRC-16校验值，为整数
    """
    def CalCRC_16_PID(self, header, command, Pvalue, Ivalue, Dvalue):
        crc = 0xFFFF
        poly = 0x8005
        combined_data = header.to_bytes(2, byteorder='little') + command.to_bytes(1, byteorder='little') + Pvalue + Ivalue + Dvalue
        hex_data_packet = ''.join([f'{byte:02x}' for byte in combined_data])
        print("Data Packet in CRC: ", hex_data_packet)
        for i, byte in enumerate(combined_data):
            #            print("循环次数:", i)  # 打印循环次数
            #           print("当前处理的字节:", hex(byte))  # 打印当前处理的字节
            crc ^= (byte << 8)  # 将当前字节左移8位后与CRC异或,相当于加入了对crc的影响
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
        return crc & 0xFFFF

    """
    计算奇偶校验位
    参数:
    data (str): 输入数据
    返回:
    int: 奇偶校验位（0 或 1）如果有偶数个1，则输出为0；如果有奇数个1，则输出为1；
    """
    def CalculateParityBit(self, data1, data2, data3):
        if isinstance(data3, int) and data3 < 0:
            # Convert negative integers to bytes
            Data31 = data3.to_bytes(4, byteorder='little', signed=True)
        else:
            # Convert non-negative integers to bytes
            Data31 = int(data3).to_bytes(4, byteorder='little', signed=False)
        combined_data = data1.to_bytes(2, byteorder='little') + data2.to_bytes(1, byteorder='little') + Data31
        count_ones = sum(bit == 1 for bit in combined_data)  # 计算输入数据中的 1 的个数
        parity_bit = count_ones % 2  # 求取奇偶校验位
        return parity_bit