import sys
from PyQt6.QtWidgets import *
from core.DataAnalysis.DataDeal import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
# from random import randint

class SubWindow1(QDialog):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 200, 10, 10)
        # 设置子窗口的背景颜色
        self.setStyleSheet("background-color: lightblue;")
        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建实线框架（QFrame）作为分隔区域
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.Box)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # 向布局添加分隔区域和一些文本或其他控件
        layout.addWidget(separator)

        # 将布局设置为子窗口的布局
        self.setLayout(layout)



class SubWindow2(QDialog):
    def __init__(self):
        super().__init__()

        #设置定时器用于周期性读取串口数据
        # self.timer = QTimer()
        # self.timer.setInterval(100)  # 每100毫秒更新一次
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

        # 初始化数据
        self.x = list(range(100))  # 100个数据点
        self.y = [0 for _ in range(100)]  # 初始化为0

        # 创建一个串口对象
        self.OpenSeri = SerialCommunication()
        self.OpenSeri.speed_data_received.connect(self.update_plot_speed)

        # 设置子窗口的背景颜色
#        self.setStyleSheet("background-color: #F5FFFA;")

        # 创建控制端的实线框架（QFrame）作为分隔区域
        Controlseparator = QFrame(self)
#        Controlseparator.setStyleSheet("background-color: #F5FFFA;")
        Controlseparator.setFrameShape(QFrame.Shape.Box)
        Controlseparator.setFrameShadow(QFrame.Shadow.Sunken)
        Controlseparator.setFixedSize(240, 700)

        Controlseparator_Frame1 = QFrame(Controlseparator)
#        Controlseparator_Frame1.setStyleSheet("background-color: #F5FFFA;")
        Controlseparator_Frame1.setFrameShape(QFrame.Shape.Box)
        Controlseparator_Frame1.setFrameShadow(QFrame.Shadow.Sunken)
        Controlseparator_Frame1.setFixedSize(210, 200)

        label1 = QLabel("Serial Port Configuration")
        label1.setStyleSheet("color: black")
        label1.setFixedSize(180, 20)
        # 创建一个字体对象
        font1 = QFont()
        font1.setPointSize(15)  # 设置字体大小
        font1.setBold(True)     # 设置为粗体
        label1.setFont(font1)

        # 串口布局安排
        label2 = QLabel("Port")
        label2.setStyleSheet("color: black")

        font2 = QFont()
        font2.setPointSize(10)  # 设置字体大小
        font2.setBold(True)     # 设置为粗体
        label2.setFont(font2)

        # 串口的下拉选框
        COM = QComboBox(self)
        COM.addItem('COM1')
        COM.addItem('COM2')
        COM.addItem('COM3')
        COM.addItem('COM4')
        COM.addItem('COM5')
        COM.addItem('COM6')
        COM.setMinimumWidth(90)
        COM.setMaximumWidth(90)
        COM.setStyleSheet("background-color: #F0F8FF; color: black")
        # 将COM和BAUD作为类的成员变量
        self.COM = COM

        # 将串口选择的水平布局设置
        PortLayout = QHBoxLayout()
        PortLayout.addWidget(label2)
        PortLayout.addWidget(COM)


        # 波特率选择
        label3 = QLabel("Baudrate")
        label3.setStyleSheet("color: black")
        label3.setFont(font2)
        # 串口的下拉选框
        BAUD = QComboBox(self)
        BAUD.addItem('2400', 2400)
        BAUD.addItem('4800', 4800)
        BAUD.addItem('9600', 9600)
        BAUD.addItem('19200', 19200)
        BAUD.addItem('38400', 38400)
        BAUD.addItem('57600', 57600)
        BAUD.addItem('115200', 115200)
        BAUD.addItem('128000', 128000)
        BAUD.addItem('230400', 230400)
        BAUD.addItem('256000', 256000)
        BAUD.setMinimumWidth(90)
        BAUD.setMaximumWidth(90)
        BAUD.setStyleSheet("background-color: #F0F8FF; color: black")
        # 将COM和BAUD作为类的成员变量
        self.BAUD = BAUD

        # 将波特率选择的水平布局设置
        BAUDLayout = QHBoxLayout()
        BAUDLayout.addWidget(label3)
        BAUDLayout.addWidget(BAUD)

        # 开串口选择
        self.indicatior = QLabel()
        self.indicatior.setFixedSize(20, 20)
        self.indicatior.setStyleSheet("background-color: gray; border-radius: 10px;")

        post_com_button = QPushButton("Open Serial")
        post_com_button.setFixedSize(80, 20)  # 设置按钮1的尺寸
        post_com_button.setStyleSheet("background-color: #F0F8FF; color: black")
        post_com_button.clicked.connect(self.PostSerialInfo)

        # 将开启选择的水平布局设置
        CommunicaitonLayout = QHBoxLayout()
        CommunicaitonLayout.addWidget(self.indicatior)
        CommunicaitonLayout.addWidget(post_com_button)

        # 创建控制面板中串口通讯框架的布局
        Controlseparator_Frame1_Layout = QVBoxLayout(Controlseparator_Frame1)
        Controlseparator_Frame1_Layout.addWidget(label1)
        Controlseparator_Frame1_Layout.addLayout(PortLayout)
        Controlseparator_Frame1_Layout.addLayout(BAUDLayout)
        Controlseparator_Frame1_Layout.addLayout(CommunicaitonLayout)

        # 控制面板中的框架2
        #创建控制面板中电机控制框架
        Controlseparator_Frame2 = QFrame(Controlseparator)
        Controlseparator_Frame2.setStyleSheet("background-color: #F5FFFA;")
        Controlseparator_Frame2.setFrameShape(QFrame.Shape.Box)
        Controlseparator_Frame2.setFrameShadow(QFrame.Shadow.Sunken)
        Controlseparator_Frame2.setFixedSize(210, 400)

        label5 = QLabel("PID Setting")
        label5.setFixedSize(180, 15)
        label5.setStyleSheet("color: black")
        label5.setFont(font1)

        # P的控制框
        lable_p = QLabel("P")
        lable_p.setFixedSize(20, 15)
        lable_p.setStyleSheet("color: black")
        lable_p.setFont(font1)

        self.P_RPMEdit = QLineEdit(self)
        self.P_RPMEdit.setFixedSize(100, 22)
        self.P_RPMEdit.setPlaceholderText('1.00')
        self.P_RPMEdit.setStyleSheet("background-color: #F0F8FF; color: black")

        # P的控制框的水平布局设置
        P_Layout = QHBoxLayout()
        P_Layout.addWidget(lable_p)
        P_Layout.addWidget(self.P_RPMEdit)
        P_Layout.setSpacing(2)

        # I的控制框
        lable_I = QLabel("I")
        lable_I.setFixedSize(20, 15)
        lable_I.setStyleSheet("color: black")
        lable_I.setFont(font1)

        self.I_RPMEdit = QLineEdit(self)
        self.I_RPMEdit.setFixedSize(100, 22)
        self.I_RPMEdit.setPlaceholderText('1.00')
        self.I_RPMEdit.setStyleSheet("background-color: #F0F8FF; color: black")

        # I的控制框的水平布局设置
        I_Layout = QHBoxLayout()
        I_Layout.addWidget(lable_I)
        I_Layout.addWidget(self.I_RPMEdit)
        I_Layout.setSpacing(2)

        # D的控制框
        lable_D = QLabel("D")
        lable_D.setFixedSize(20, 15)
        lable_D.setStyleSheet("color: black")
        lable_D.setFont(font1)

        self.D_RPMEdit = QLineEdit(self)
        self.D_RPMEdit.setFixedSize(100, 22)
        self.D_RPMEdit.setPlaceholderText('1.00')
        self.D_RPMEdit.setStyleSheet("background-color: #F0F8FF; color: black")

        # D的控制框的水平布局设置
        D_Layout = QHBoxLayout()
        D_Layout.addWidget(lable_D)
        D_Layout.addWidget(self.D_RPMEdit)
        D_Layout.setSpacing(2)

        # 发送PID按钮
        PIDButton = QPushButton("Send PID")
        PIDButton.setFixedSize(80, 20)
        PIDButton.setStyleSheet("background-color: #F0F8FF; color: black")
        PIDButton.clicked.connect(lambda: self.PostPID(0x10, self.P_RPMEdit.text(), self.I_RPMEdit.text(), self.D_RPMEdit.text()))

        PIDButton_Layout = QHBoxLayout()
        PIDButton_Layout.addWidget(PIDButton)
        PIDButton_Layout.setContentsMargins(30, 0, 30, 0)

        # 转速设定
        lable_speed = QLabel("Speed")
        lable_speed.setFixedSize(65, 15)
        lable_speed.setStyleSheet("color: black")
        lable_speed.setFont(font1)

        self.SpeedRPMEdit = QLineEdit(self)
        self.SpeedRPMEdit.setFixedSize(60, 22)
        self.SpeedRPMEdit.setPlaceholderText('100')
        self.SpeedRPMEdit.setStyleSheet("background-color:#F0F8FF; color: black")

        SpeedGo = QPushButton("Go")
        SpeedGo.setFixedSize(50, 20)
        SpeedGo.setStyleSheet("background-color: #F0F8FF; color: black")
        SpeedGo.clicked.connect(lambda: self.PostCommandInfo(0x11, self.SpeedRPMEdit.text()))

        # speed的控制框的水平布局设置
        speed_Layout = QHBoxLayout()
        speed_Layout.addWidget(lable_speed)
        speed_Layout.addWidget(self.SpeedRPMEdit)
        speed_Layout.addWidget(SpeedGo)
        speed_Layout.setSpacing(2)

        # 位置设定
        lable_location = QLabel("Position")
        lable_location.setFixedSize(65, 15)
        lable_location.setStyleSheet("color: black")
        lable_location.setFont(font1)

        self.LocationRPMEdit = QLineEdit(self)
        self.LocationRPMEdit.setFixedSize(60, 22)
        self.LocationRPMEdit.setPlaceholderText('100')
        self.LocationRPMEdit.setStyleSheet("background-color:#F0F8FF; color: black")

        LocationGo = QPushButton("Go")
        LocationGo.setFixedSize(50, 20)
        LocationGo.setStyleSheet("background-color: #F0F8FF; color: black")
        LocationGo.clicked.connect(lambda: self.PostCommandInfo(0x12, self.LocationRPMEdit.text()))

        # speed的控制框的水平布局设置
        Location_Layout = QHBoxLayout()
        Location_Layout.addWidget(lable_location)
        Location_Layout.addWidget(self.LocationRPMEdit)
        Location_Layout.addWidget(LocationGo)
        Location_Layout.setSpacing(2)

        # 方向控制以及停止按钮
        LeftButton = QPushButton("<-")
        LeftButton.setFixedSize(50, 20)
        LeftButton.setStyleSheet("background-color: #F0F8FF; color: black")
        LeftButton.clicked.connect(lambda: self.PostCommandInfo(0x13, 0x0))

        StopButton = QPushButton("stop")
        StopButton.setFixedSize(50, 20)
        StopButton.setStyleSheet("background-color: #F0F8FF; color: black")
        StopButton.clicked.connect(lambda: self.PostCommandInfo(0x14, 0x0))

        RightButton = QPushButton("->")
        RightButton.setFixedSize(50, 20)
        RightButton.setStyleSheet("background-color: #F0F8FF; color: black")
        RightButton.clicked.connect(lambda: self.PostCommandInfo(0x15, 0x0))


        orition_Layout = QHBoxLayout()
        orition_Layout.addWidget(LeftButton)
        orition_Layout.addWidget(StopButton)
        orition_Layout.addWidget(RightButton)
        orition_Layout.setSpacing(2)

        # 重置按钮
        ResetButton = QPushButton("Reset")
        ResetButton.setFixedSize(50, 20)
        ResetButton.setStyleSheet("background-color: #F0F8FF; color: black")
        ResetButton.clicked.connect(lambda: self.PostCommandInfo(0x16, 0x0))

        ResetButton_Layout = QHBoxLayout()
        ResetButton_Layout.addWidget(ResetButton)
        ResetButton_Layout.setContentsMargins(120,0,0,0)

        # 创建控制面板中电机控制框架的布局
        Controlseparator_Frame2_Layout = QVBoxLayout(Controlseparator_Frame2)
        Controlseparator_Frame2_Layout.addWidget(label5)
        Controlseparator_Frame2_Layout.addLayout(P_Layout)
        Controlseparator_Frame2_Layout.addLayout(I_Layout)
        Controlseparator_Frame2_Layout.addLayout(D_Layout)
        Controlseparator_Frame2_Layout.addLayout(PIDButton_Layout)
        Controlseparator_Frame2_Layout.addLayout(speed_Layout)
        Controlseparator_Frame2_Layout.addLayout(Location_Layout)
        Controlseparator_Frame2_Layout.addLayout(orition_Layout)
        Controlseparator_Frame2_Layout.addLayout(ResetButton_Layout)
        Controlseparator_Frame2_Layout.setSpacing(0)

        # 创建垂直布局将两个框架添加到布局中
        ConrtolLayout = QVBoxLayout(Controlseparator)
        ConrtolLayout.addWidget(Controlseparator_Frame1)
        ConrtolLayout.addWidget(Controlseparator_Frame2)
        ConrtolLayout.setSpacing(5)

        ######## 显示模块的开始
        # 创建显示端的实线框架（QFrame）作为分隔区域
        Showseparator = QFrame(self)
        Showseparator.setStyleSheet("background-color: #F5FFFA;")
        Showseparator.setFrameShape(QFrame.Shape.Box)
        Showseparator.setFrameShadow(QFrame.Shadow.Sunken)
        Showseparator.setFixedSize(900, 700)

        #创建显示分区1
        Showseparator_Frame1 = QFrame(Showseparator)
        Showseparator_Frame1.setStyleSheet("background-color: #F5FFFA;")
        Showseparator_Frame1.setFrameShape(QFrame.Shape.Box)
        Showseparator_Frame1.setFrameShadow(QFrame.Shadow.Sunken)

        """ 创建图形控件 """
        self.graphWidget1 = pg.PlotWidget()
        self.setupGraphWidget(self.graphWidget1, "Speed/RPM", "rpm", "time/s")

        # 创建电机1显示布局
        Showseparator_Frame1_Layout = QVBoxLayout(Showseparator_Frame1)
        Showseparator_Frame1_Layout.addWidget(self.graphWidget1)

        # 创建显示分区2
        Showseparator_Frame2 = QFrame(Showseparator)
        Showseparator_Frame2.setStyleSheet("background-color: #F5FFFA;")
        Showseparator_Frame2.setFrameShape(QFrame.Shape.Box)
        Showseparator_Frame2.setFrameShadow(QFrame.Shadow.Sunken)

        self.graphWidget2 = pg.PlotWidget()
        self.setupGraphWidget(self.graphWidget2, "Position", "degree", "time/s")

        # 创建电机2显示布局
        Showseparator_Frame2_Layout = QVBoxLayout(Showseparator_Frame2)
        Showseparator_Frame2_Layout.addWidget(self.graphWidget2)

        # 创建垂直布局将两个框架添加到布局中
        ShowLayout = QVBoxLayout(Showseparator)
        ShowLayout.addWidget(self.graphWidget1)
        ShowLayout.addWidget(self.graphWidget2)
        ShowLayout.setSpacing(0)

        # 创建水平布局
        Sub2Mainlayout = QHBoxLayout()
        Sub2Mainlayout.addWidget(Controlseparator)
        Sub2Mainlayout.addWidget(Showseparator)

        # 将布局设置为子窗口的布局
        self.setLayout(Sub2Mainlayout)

    def setupGraphWidget(self, graphWidget, title, ylabel, xlabel):
        graphWidget.setBackground('#F5FFFA')
        graphWidget.setTitle(title, color="black", size="15pt")
        graphWidget.setLabel('left', ylabel, color='b', size=30)
        graphWidget.setLabel('bottom', xlabel, color='b', size=30)
        graphWidget.showGrid(x=True, y=True)


    def show_auto_close_dialog(self, message, timeout=2000):
        # 创建对话框
        dialog = QDialog(self)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QLabel(message))

        # 设置计时器关闭对话框
        QTimer.singleShot(timeout, dialog.close)
        dialog.exec()

    def PostSerialInfo(self):
        self.selected_port = self.COM.currentText()
        self.selected_baud = int(self.BAUD.currentText())
        if self.OpenSeri.ser is not None and self.OpenSeri.ser.isOpen():
            success, message = self.OpenSeri.close_ser()
            if success:
                self.COM.setDisabled(False)
                self.BAUD.setDisabled(False)
                self.indicatior.setStyleSheet("background-color: gray; border-radius: 10px;")
                self.show_auto_close_dialog("Serial State: " + message, 1000)
            else:
                self.show_auto_close_dialog("Serial State: " + message, 1000)
        else:
            success, message = self.OpenSeri.open_ser(self.selected_port, self.selected_baud)
            if success:
                self.indicatior.setStyleSheet("background-color: green; border-radius: 10px;")
                self.COM.setDisabled(True)
                self.BAUD.setDisabled(True)
                self.show_auto_close_dialog("Serial State: " + message, 1000)
                print("Selected port:", self.selected_port)
                print("Selected baud rate:", self.selected_baud)
            else:
                print(message)
                self.show_auto_close_dialog("Serial Err: " + message, 1000)

    """
        brief: 发送信息
        para1: 命令码
        para2: 参数
    """
    def PostCommandInfo(self, contcommand, parameter):
        try:
            HeaderCode = 0x55AA
            CombinPost = SerialCommunication()
            if parameter == '':
                self.show_auto_close_dialog("Error: The parameters is empty, please enter value", 2000)
                return  # Return early if parameter is empty
            parameter = int(parameter)
            # 检测parameter是否为负数
            if isinstance(parameter, int) and parameter < 0:
                # Convert negative integers to bytes
                parameter_bytes = parameter.to_bytes(8, byteorder='little', signed=True)
            else:
                # Convert non-negative integers to bytes
                parameter_bytes = int(parameter).to_bytes(8, byteorder='little', signed=False)

            CRC_bytes = CombinPost.CalCRC_16(HeaderCode, contcommand, parameter_bytes)
            print(f"CRC-16校验值: 0x{CRC_bytes:04X}")
            print("para: ", parameter_bytes, type(parameter_bytes))
            DataPacket = CombinPost.create_data_packet(HeaderCode, contcommand, parameter_bytes, CRC_bytes)
            hex_data_packet = ''.join([f'{byte:02x}' for byte in DataPacket])
            print("Data Packet in PostCommandInfo: ", hex_data_packet)
            CombinPost.send_msg(DataPacket)
        except Exception as e:
            self.show_auto_close_dialog(f"Warning: {str(e)}", 2000)


    """
        brief: 发送PID的信息
        contcommand: 命令码
        Pvalue: 比例值
        Ivalue: 积分值
        Dvalue: 微分值
        return: None/状态
    """
    def PostPID(self, contcommand, Pvalue, Ivalue, Dvalue):
        try:
            HeaderCode = 0x55AA
            CombinPost = SerialCommunication()
            if Pvalue == '' and Ivalue == '' and Dvalue == '':
                self.show_auto_close_dialog("Error: please input PID value", 2000)
                return  # Return early if parameter is empty
            """
            PID参数，一般是正数
            """
            Pvalue = int(Pvalue)
            if not 0 <= Pvalue <= 16777215:
                self.show_auto_close_dialog("范围错误: P值超出范围。它必须在0到16777215之间。", 2000)
                return

            Pvalue_bytes = Pvalue.to_bytes(3, byteorder='little', signed=False)

            Ivalue = int(Ivalue)
            if not 0 <= Ivalue <= 16777215:
                self.show_auto_close_dialog("范围错误: I值超出范围。它必须在0到16777215之间。", 2000)
                return
            Ivalue_bytes = Ivalue.to_bytes(3, byteorder='little', signed=False)

            Dvalue = int(Dvalue)
            if not 0 <= Dvalue <= 65535:
                self.show_auto_close_dialog("范围错误: D值超出范围。它必须在0到65535之间。", 2000)
                return
            Dvalue_bytes = Dvalue.to_bytes(2, byteorder='little', signed=False)

            PID_para = Pvalue_bytes + Ivalue_bytes + Dvalue_bytes
            CRC_bytes = CombinPost.CalCRC_16(HeaderCode, contcommand, PID_para)
            print(f"CRC-16校验值: 0x{CRC_bytes:04X}")
            print("Pvalue: ", Pvalue_bytes, type(Pvalue_bytes))
            print("Ivalue: ", Ivalue_bytes, type(Ivalue_bytes))
            print("Dvalue: ", Dvalue_bytes, type(Dvalue_bytes))
            DataPacket = CombinPost.create_data_packet(HeaderCode, contcommand, PID_para, CRC_bytes)
            hex_data_packet = ''.join([f'{byte:02x}' for byte in DataPacket])
            print("Data Packet in PostCommandInfo: ", hex_data_packet)
            CombinPost.send_msg(DataPacket)
        except Exception as e:
            self.show_auto_close_dialog(f"Warning: {str(e)}", 2000)

    # def update_plot_data(self):
    #     # 这里应该是获取新数据的逻辑
    #     self.x = self.x[1:]  # 删除第一个元素
    #     self.x.append(self.x[-1] + 1)  # 添加新的x值
    #
    #     self.y = self.y[1:]  # 删除第一个元素
    #     self.y.append(randint(0,100))  # 添加一个新的随机y值
    #
    #     # 更新图形
    #     self.graphWidget1.plot(self.x, self.y, pen=pg.mkPen(color=(255, 0, 0), width=5))
    #     # 更新图形
    #     self.graphWidget2.plot(self.x, self.y, pen=pg.mkPen(color=(255, 0, 0), width=5))

    def update_plot_speed(self, new_speed):
        self.x.append(self.x[-1] + 1)  # 增加新的x值
        self.y.append(new_speed)  # 添加新的速度值

        # 更新图形
        self.graphWidget1.plot(self.x, self.y, pen=pg.mkPen(color=(255, 0, 0), width=5))

class SubWindow3(QDialog):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 200, 10, 10)
        # 设置子窗口的背景颜色
        self.setStyleSheet("background-color: lightblue;")
# 创建垂直布局
        layout = QVBoxLayout()

        # 创建实线框架（QFrame）作为分隔区域
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.Box)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # 向布局添加分隔区域和一些文本或其他控件
        layout.addWidget(separator)

        # 将布局设置为子窗口的布局
        self.setLayout(layout)

class SubWindow4(QDialog):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 200, 10, 10)
        # 设置子窗口的背景颜色
        self.setStyleSheet("background-color: lightgreen;")
# 创建垂直布局
        layout = QVBoxLayout()

        # 创建实线框架（QFrame）作为分隔区域
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.Box)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # 向布局添加分隔区域和一些文本或其他控件
        layout.addWidget(separator)

        # 将布局设置为子窗口的布局
        self.setLayout(layout)


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Peristaltic Pump Debugging Assistant")
#         self.setGeometry(300, 200, 1000, 800)
#         # 创建一个主界面容器
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#
#         # 创建垂直布局
#         main_layout = QVBoxLayout()
#
#         # 设置主窗口容器的布局为垂直布局
#         main_widget.setLayout(main_layout)
#
#         # 创建按钮布局
#         button_layout = QHBoxLayout()
#
#         # 创建四个按钮
#         button1 = QPushButton("串口调试助手")
#         button1.setFixedSize(300, 50)  # 设置按钮1的尺寸
#         button1.clicked.connect(self.open_window1)
#         button1.setStyleSheet("background-color: gray; color: white;")
#         button_layout.addWidget(button1)
#
#
#         button2 = QPushButton("PID调试助手")
#         button2.setFixedSize(300, 50)  # 设置按钮2的尺寸
#         button2.clicked.connect(self.open_window2)
#         button2.setStyleSheet("background-color: gray; color: white;")
#         button_layout.addWidget(button2)
#
#         button3 = QPushButton("摄像头调试助手")
#         button3.setFixedSize(300, 50)  # 设置按钮3的尺寸
#         button3.clicked.connect(self.open_window3)
#         button3.setStyleSheet("background-color: gray; color: white;")
#         button_layout.addWidget(button3)
#
#         button4 = QPushButton("网络调试助手")
#         button4.setFixedSize(300, 50)  # 设置按钮4的尺寸
#         button4.clicked.connect(self.open_window4)
#         button4.setStyleSheet("background-color: gray; color: white;")
#         button_layout.addWidget(button4)
#         button_layout.setSpacing(0)
#
#         # 创建视频播放器组件
#         self.mediaPlayer = QMediaPlayer()
#         self.videoWidget = QVideoWidget()
#
#         # 设置视频播放器输出
#         self.mediaPlayer.setVideoOutput(self.videoWidget)
#         # 加载视频文件
#         self.mediaPlayer.setSource(QUrl.fromLocalFile("../Icons/cool.mp4"))
#         # 连接信号
#         self.mediaPlayer.mediaStatusChanged.connect(self.media_status_changed)
#         # 开始播放视频
#         self.mediaPlayer.play()
#
#         # 添加水平布局到垂直布局
#         main_layout.addLayout(button_layout)
#         # 添加视频播放器到布局
#         main_layout.addWidget(self.videoWidget)
#
#         # 设置主窗口的背景颜色
#         self.setStyleSheet("background-color: #F5FFFA;")
#
#         # 创建一个堆叠窗口，用于显示子窗口
#         self.stacked_widget = QStackedWidget()
#         main_layout.addWidget(self.stacked_widget)
#         main_layout.setSpacing(0)
#
#     def media_status_changed(self, status):
#         if status == QMediaPlayer.MediaStatus.EndOfMedia:
#             self.mediaPlayer.play()
#
#     def open_window1(self):
#         sub_window1 = SubWindow1()
#         self.stacked_widget.addWidget(sub_window1)
#         self.stacked_widget.setCurrentWidget(sub_window1)
#         self.setWindowTitle("串口调试助手")
#
#     def open_window2(self):
#         sub_window2 = SubWindow2()
#         self.stacked_widget.addWidget(sub_window2)
#         self.stacked_widget.setCurrentWidget(sub_window2)
#         self.setWindowTitle("PID调试助手")
#
#
#     def open_window3(self):
#         sub_window3 = SubWindow3()
#         self.stacked_widget.addWidget(sub_window3)
#         self.stacked_widget.setCurrentWidget(sub_window3)
#         self.setWindowTitle("摄像头调试助手")
#
#     def open_window4(self):
#         sub_window4 = SubWindow4()
#         self.stacked_widget.addWidget(sub_window4)
#         self.stacked_widget.setCurrentWidget(sub_window4)
#         self.setWindowTitle("网络调试助手")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Peristaltic Pump Debugging Assistant")
        self.setGeometry(300, 200, 1000, 800)

        # 主界面容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 主界面布局
        main_layout = QVBoxLayout(main_widget)

        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()

        # 按钮布局
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # 创建子窗口实例
        self.subWindow1 = SubWindow1()
        self.subWindow2 = SubWindow2()
        self.subWindow3 = SubWindow3()
        self.subWindow4 = SubWindow4()

        # 视频播放器组件
        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()

        self.stacked_widget.addWidget(self.videoWidget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # 创建堆叠窗口
        self.stacked_widget.addWidget(self.subWindow1)
        self.stacked_widget.addWidget(self.subWindow2)
        self.stacked_widget.addWidget(self.subWindow3)
        self.stacked_widget.addWidget(self.subWindow4)

        # main_layout.addWidget(self.stacked_widget)

        self.createButton("串口调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow1))
        self.createButton("PID调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow2))
        self.createButton("摄像头调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow3))
        self.createButton("网络调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow4))

        # 视频播放器组件
        # self.mediaPlayer = QMediaPlayer()
        # self.videoWidget = QVideoWidget()
        # self.mediaPlayer.setVideoOutput(self.videoWidget)
        # 视频文件路径
        # 加载视频文件
        self.mediaPlayer.setSource(QUrl.fromLocalFile("../Icons/cool.mp4"))
        self.mediaPlayer.play()
        # 连接信号
        self.mediaPlayer.mediaStatusChanged.connect(self.media_status_changed)

        # 添加视频播放器到布局
        main_layout.addWidget(self.stacked_widget)

    def media_status_changed(self, status):
        # 检查媒体播放状态
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.mediaPlayer.play()  # 重复播放视频

    def createButton(self, text, layout, callback):
        button = QPushButton(text)
        button.setFixedSize(300, 50)
        button.setStyleSheet("background-color: gray; color: white;")
        button.clicked.connect(callback)
        layout.addWidget(button)








