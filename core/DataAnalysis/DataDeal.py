import time
from core.QT.qt_show import *
from PyQt6.QtCore import *
import threading
from PyQt6.QtWidgets import *
import serial
from core.QT.qt_show import *

class SerialCommunication(QObject):
    # 创建一个新信号
    data_received = pyqtSignal(bytes)
    speed_data_received = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.ser = None
        self.running = False
        self.thread = QThread()   # 直接创建一个全局读数据线程
        # 定义命令处理函数的映射
        self.cmd_handlers = {
            b'\x17': self.handle17_ShowSpeed,
            b'\x18': self.handle18_ShowLocation,
            b'\x19': self.handle19_synchronousPID,
        }

    def open_ser(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            if self.ser.is_open:
                self.running = True
                self.start_reading_thread()  # 使用 QThread 启动读取流程
                print("The serial port successfully opened")
                return True, "Serial port successfully opened"
            else:
                error_msg = "Failed to open serial port."
                print(error_msg)
                return False, error_msg
        except Exception as exc:
            error_msg = f"Serial port opening failed: {str(exc)}"
            print(error_msg)
            return False, error_msg

    def start_reading_thread(self):
        print("Attempting to start the reading thread...")
        self.moveToThread(self.thread)  # 移动当前对象到新线程
        self.thread.started.connect(self.read_data)
        self.thread.finished.connect(lambda: print("Reading thread finished."))
        self.thread.start()
        print("Reading thread successfully started.")

    def close_ser(self):
        try:
            if self.thread is not None:
                # 确保从线程发出退出请求
                self.thread.requestInterruption()  # 请求线程中断
                self.thread.quit()  # 请求线程退出
                self.thread.wait()  # 等待线程完全退出
#                self.thread = None
            if self.ser is not None and self.ser.is_open:
                self.ser.close()
                self.ser = None  # 重置串口对象，准备下次打开
                self.running = False
                return True, "Serial port closed successfully."
            else:
                return False, "Serial port was not open."
        except Exception as exc:
            return False, f"Error while closing serial port: {str(exc)}"

    def send_msg(self, data):
        # print(f"Trying to send data. Serial port open: {self.ser.is_open}")
        if not self.ser or not self.ser.is_open:
            # print("Serial port is not open")
            return False, "Serial port is not open"
        # 尝试发送数据
        try:
            self.ser.write(data)
            print(f"Data sent successfully. Data is : {data.hex()}")
            return True, "Data sent successfully"
        except Exception as exc:
            # print("Error while sending data:", exc)
            return False, f"Error while sending data: {exc}"


    def handle17_ShowSpeed(self, para):
        # print("para Data17: ", para.hex())
        # print("Type of para Data:", type(para))
        SpeedValue = int.from_bytes(para, byteorder='little')  # 或者 'big'，取决于字节序
        # print("para Integer Value:", SpeedValue)
        self.speed_data_received.emit(SpeedValue)


    def handle18_ShowLocation(self, para):
        print("para Data18: ", para.hex())
        print("Type of para Data:", type(para))
        integer_value = int.from_bytes(para, byteorder='little')  # 或者 'big'，取决于字节序
        print("para Integer Value:", integer_value)

    def handle19_synchronousPID(self, para):
        print("para Data19: ", para.hex())
        print("Type of para Data:", type(para))
        integer_value = int.from_bytes(para, byteorder='little')  # 或者 'big'，取决于字节序
        print("para Integer Value:", integer_value)



    def read_data(self):
        print("Data reading started...")
        while self.running and not self.thread.isInterruptionRequested():
            try:
                if self.ser is not None and self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting)
                    hex_representation = data.hex()
                    print(hex_representation)
                    # 使用emit发出信号，传递读取到的原始数据
                    self.data_received.emit(data)

                    # 调用方法处理和验证数据
                    validated_data = self.process_and_validate_data(data)
                    if validated_data is not False:
                        cmd = validated_data['cmd']
                        para = validated_data['para']
                        # 根据解析出的命令和参数进行相应的处理
                        handler = self.cmd_handlers.get(cmd)
                        if handler:
                            handler(para)
                        else:
                            print("Unknown command:", cmd.hex())
                    else:
                        print("Invalid or incomplete data received")
            except Exception as e:
                print(f"Error reading data: {e}")

            QThread.msleep(10)  # 稍微延迟以减少CPU占用率

        print("Exiting read_data loop.")



    """
    brief: 数据处理
    para : data
    """
    def process_and_validate_data(self, data):
        header = b'\xAA\x55'
        header_index = data.find(header)

        if header_index == -1:
            return False  # 数据头未找到

        cmd_index = header_index + len(header)
        if cmd_index >= len(data):
            return False  # 验证数据长度

        # 假设命令是一个字节，参数是四个字节
        data_index = cmd_index + 1
        crc_index = data_index + 4
        if crc_index + 2 > len(data):
            return False  # 数据长度不足

        cmd = data[cmd_index:cmd_index + 1]  # 提取命令字节
        para = data[data_index:data_index + 4]  # 提取参数字节
        received_crc = data[crc_index:crc_index + 2]  # 提取接收到的CRC

        # 计算CRC
        calculated_crc = self.CalCRC_16_Reci(header, cmd, para)
        calculated_crc_bytes = calculated_crc.to_bytes(2, 'little')

        if received_crc == calculated_crc_bytes:
            return {'cmd': cmd, 'para': para}
        else:
            return False


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
            crc ^= (byte << 8)  # 将当前字节左移8位后与CRC异或,相当于加入了对crc的影响
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
        return crc & 0xFFFF

    def CalCRC_16_Reci(self, header, command, para):
        crc = 0xFFFF
        poly = 0x8005
        # 直接拼接字节数据
        combined_data = header + command + para
        hex_data_packet = ''.join([f'{byte:02x}' for byte in combined_data])
        print("Data Packet in CRC: ", hex_data_packet)

        for i, byte in enumerate(combined_data):
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