import sys
from PyQt6.QtWidgets import *
from pyqtgraph import PlotWidget, plot
from core.DataAnalysis.DataDeal import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, pyqtBoundSignal
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

        # 初始化数据
        self.x = list(range(100))  # 100个数据点
        self.y = [0] * 100  # 初始化Y轴数据为0

        # 创建一个串口对象
        self.OpenSeri = SerialCommunication()
        self.OpenSeri.speed_data_received.connect(self.update_plot_speed)

        # 创建控制端的实线框架（QFrame）作为分隔区域
        self.Controlseparator = QFrame(self)
        self.Controlseparator.setFixedSize(180, 650)
        self.Controlseparator.setStyleSheet("""
                    QFrame {
                        background-color: #E3E3E3;  /* 淡灰色背景 */
                        border-radius: 10px;  /* 圆角边框 */
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);  /* 轻微阴影 */
                    }
                """)
        self.Controlseparator.setFrameShape(QFrame.Shape.NoFrame)  # 移除内置边框样式

        self.Controlseparator_Frame1 = QFrame(self.Controlseparator)
        self.Controlseparator_Frame1.setFrameShape(QFrame.Shape.Box)
        self.Controlseparator_Frame1.setFrameShadow(QFrame.Shadow.Sunken)
        self.Controlseparator_Frame1.setFixedSize(160, 200)

        self.label1 = self.create_label("Serial Configuration", "Segoe UI", 10, True, "#000080")

        # 串口布局安排
        self.label2 = self.create_label("Port", "Segoe UI", 10, True, "#000080")

        # 串口的下拉选框
        self.COM = QComboBox(self)
        self.COM.addItem('COM1')
        self.COM.addItem('COM2')
        self.COM.addItem('COM3')
        self.COM.addItem('COM4')
        self.COM.addItem('COM5')
        self.COM.addItem('COM6')
        self.COM.setMinimumWidth(70)
        self.COM.setMaximumWidth(70)
        self.COM.setStyleSheet("""
            QComboBox {
                background-color: #F0F8FF;  /* 淡蓝色背景 */
                color: #2e2e2e;             /* 深灰色字体 */
                border: 1px solid #A9A9A9;  /* 边框 */
                border-radius: 4px;         /* 圆角边框 */
                padding: 2px 5px;           /* 内边距 */
            }
            QComboBox:hover {
                border-color: #87CEEB;     /* 悬浮时边框颜色变化 */
            }
            QComboBox::drop-down {
                border: none;              /* 下拉箭头的边框 */
            }
            QComboBox QAbstractItemView {
                selection-background-color: #ADD8E6; /* 选中项的背景颜色 */
            }
        """)

        # 将串口选择的水平布局设置
        self.PortLayout = QHBoxLayout()
        self.PortLayout.addWidget(self.label2)
        self.PortLayout.addWidget(self.COM)

        # 波特率选择
        self.label3 = self.create_label("Baudrate", "Segoe UI", 10, True, "#000080")
        # 串口的下拉选框
        self.BAUD = QComboBox(self)
        self.BAUD.addItem('2400', 2400)
        self.BAUD.addItem('4800', 4800)
        self.BAUD.addItem('9600', 9600)
        self.BAUD.addItem('19200', 19200)
        self.BAUD.addItem('38400', 38400)
        self.BAUD.addItem('57600', 57600)
        self.BAUD.addItem('115200', 115200)
        self.BAUD.addItem('128000', 128000)
        self.BAUD.addItem('230400', 230400)
        self.BAUD.addItem('256000', 256000)
        self.BAUD.setMinimumWidth(70)
        self.BAUD.setMaximumWidth(70)
        self.BAUD.setStyleSheet("""
            QComboBox {
                background-color: #F0F8FF;  /* 淡蓝色背景 */
                color: #2e2e2e;             /* 深灰色字体 */
                border: 1px solid #A9A9A9;  /* 边框 */
                border-radius: 4px;         /* 圆角边框 */
                padding: 2px 5px;           /* 内边距 */
            }
            QComboBox:hover {
                border-color: #87CEEB;     /* 悬浮时边框颜色变化 */
            }
            QComboBox::drop-down {
                border: none;              /* 下拉箭头的边框 */
            }
            QComboBox QAbstractItemView {
                selection-background-color: #ADD8E6; /* 选中项的背景颜色 */
            }
        """)

        # 将波特率选择的水平布局设置
        self.BAUDLayout = QHBoxLayout()
        self.BAUDLayout.addWidget(self.label3)
        self.BAUDLayout.addWidget(self.BAUD)

        # 开串口选择
        self.indicatior = QLabel()
        self.indicatior.setStyleSheet("""
            QLabel {
                background-color: #D3D3D3;  /* 淡灰色背景 */
                border-radius: 10px;        /* 设置圆角为高度的一半 */
                width:  20px;                /* 设置宽度 */
                height: 20px;               /* 设置高度 */
            }
        """)
        self.indicatior.setFixedSize(20, 20)

        self.post_com_button = self.create_button("Open", 50, 30)
        self.post_com_button.clicked.connect(self.PostSerialInfo)

        # 将开启选择的水平布局设置
        self.CommunicaitonLayout = QHBoxLayout()
        self.CommunicaitonLayout.addWidget(self.indicatior)
        self.CommunicaitonLayout.addWidget(self.post_com_button)

        # 创建控制面板中串口通讯框架的布局
        self.Controlseparator_Frame1_Layout = QVBoxLayout(self.Controlseparator_Frame1)
        self.Controlseparator_Frame1_Layout.addWidget(self.label1)
        self.Controlseparator_Frame1_Layout.addLayout(self.PortLayout)
        self.Controlseparator_Frame1_Layout.addLayout(self.BAUDLayout)
        self.Controlseparator_Frame1_Layout.addLayout(self.CommunicaitonLayout)

        # 控制面板中的框架2
        # 创建控制面板中电机控制框架
        self.Controlseparator_Frame2 = QFrame(self.Controlseparator)
        self.Controlseparator_Frame2.setFrameShape(QFrame.Shape.Box)
        self.Controlseparator_Frame2.setFrameShadow(QFrame.Shadow.Sunken)
        self.Controlseparator_Frame2.setFixedSize(160, 400)

        self.label5 = self.create_label("PID Setting", "Segoe UI", 10, True, "#000080")

        # P的控制框
        self.lable_p = self.create_label("P", "Segoe UI", 10, True, "#000080")

        self.P_RPMEdit = self.create_line_edit("1.000", 60, 22)

        # P的控制框的水平布局设置
        self.P_Layout = QHBoxLayout()
        self.P_Layout.addWidget(self.lable_p)
        self.P_Layout.addWidget(self.P_RPMEdit)
        self.P_Layout.setSpacing(0)

        # I的控制框
        self.lable_I = self.create_label("I", "Segoe UI", 10, True, "#000080")
        self.I_RPMEdit = self.create_line_edit("1.000", 60, 22)

        # I的控制框的水平布局设置
        self.I_Layout = QHBoxLayout()
        self.I_Layout.addWidget(self.lable_I)
        self.I_Layout.addWidget(self.I_RPMEdit)
        self.I_Layout.setSpacing(2)

        # D的控制框
        self.lable_D = self.create_label("D", "Segoe UI", 10, True, "#000080")
        self.D_RPMEdit = self.create_line_edit("1.000", 60, 22)

        # D的控制框的水平布局设置
        self.D_Layout = QHBoxLayout()
        self.D_Layout .addWidget(self.lable_D)
        self.D_Layout .addWidget(self.D_RPMEdit)
        self.D_Layout .setSpacing(2)

        # 发送PID按钮
        self.PIDButton = self.create_button("Send PID", 80, 25)
        self.PIDButton.clicked.connect(lambda: self.PostPID(0x10, self.P_RPMEdit.text(), self.I_RPMEdit.text(), self.D_RPMEdit.text()))

        self.PIDButton_Layout = QHBoxLayout()
        self.PIDButton_Layout.addWidget(self.PIDButton)
        self.PIDButton_Layout.setContentsMargins(30, 0, 30, 0)

        # 转速设定
        self.lable_speed = self.create_label("Speed", "Segoe UI", 10, True, "#000080")
        self.SpeedRPMEdit = self.create_line_edit("100", 60, 22)

        self.SpeedGo = self.create_button("Go", 50, 25)
        self.SpeedGo.clicked.connect(lambda: self.PostCommandInfo(0x11, self.SpeedRPMEdit.text()))

        # speed的控制框的水平布局设置
        self.speed_Layout = QHBoxLayout()
        self.speed_Layout.addWidget(self.SpeedRPMEdit)
        self.speed_Layout.addWidget(self.SpeedGo)
        self.speed_Layout.setSpacing(2)

        # 位置设定
        self.lable_location = self.create_label("Position", "Segoe UI", 10, True, "#000080")
        self.LocationRPMEdit = self.create_line_edit("100", 60, 22)

        self.LocationGo = self.create_button("Go", 50, 25)
        self.LocationGo.clicked.connect(lambda: self.PostCommandInfo(0x12, self.LocationRPMEdit.text()))

        # speed的控制框的水平布局设置
        self.Location_Layout = QHBoxLayout()
        self.Location_Layout.addWidget(self.LocationRPMEdit)
        self.Location_Layout.addWidget(self.LocationGo)
        self.Location_Layout.setSpacing(2)

        # 方向控制以及停止按钮
        self.LeftButton = self.create_button("<-", 50, 25)
        self.LeftButton.clicked.connect(lambda: self.PostCommandInfo(0x13, 0x0))

        self.StopButton = self.create_button("Stop", 50, 25)
        self.StopButton.clicked.connect(lambda: self.PostCommandInfo(0x14, 0x0))

        self.RightButton = self.create_button("->", 50, 25)
        self.RightButton.clicked.connect(lambda: self.PostCommandInfo(0x15, 0x0))

        self.orition_Layout = QHBoxLayout()
        self.orition_Layout.addWidget(self.LeftButton)
        self.orition_Layout.addWidget(self.StopButton)
        self.orition_Layout.setSpacing(0)

        # 重置按钮
        self.ResetButton = self.create_button("Reset", 50, 25)
        self.ResetButton.clicked.connect(lambda: self.PostCommandInfo(0x16, 0x0))

        self.ResetButton_Layout = QHBoxLayout()
        self.ResetButton_Layout.addWidget(self.RightButton)
        self.ResetButton_Layout.addWidget(self.ResetButton)

        # 创建控制面板中电机控制框架的布局
        self.Controlseparator_Frame2_Layout = QVBoxLayout(self.Controlseparator_Frame2)
        self.Controlseparator_Frame2_Layout.addWidget(self.label5)
        self.Controlseparator_Frame2_Layout.addLayout(self.P_Layout)
        self.Controlseparator_Frame2_Layout.addLayout(self.I_Layout)
        self.Controlseparator_Frame2_Layout.addLayout(self.D_Layout )
        self.Controlseparator_Frame2_Layout.addLayout(self.PIDButton_Layout)
        self.Controlseparator_Frame2_Layout.addWidget(self.lable_speed)
        self.Controlseparator_Frame2_Layout.addLayout(self.speed_Layout)
        self.Controlseparator_Frame2_Layout.addWidget(self.lable_location)
        self.Controlseparator_Frame2_Layout.addLayout(self.Location_Layout)
        self.Controlseparator_Frame2_Layout.addLayout(self.orition_Layout)
        self.Controlseparator_Frame2_Layout.addLayout(self.ResetButton_Layout)
        self.Controlseparator_Frame2_Layout.setSpacing(0)

        # 创建垂直布局将两个框架添加到布局中
        self.ConrtolLayout = QVBoxLayout(self.Controlseparator)
        self.ConrtolLayout.addWidget(self.Controlseparator_Frame1)
        self.ConrtolLayout.addWidget(self.Controlseparator_Frame2)
        self.ConrtolLayout.setSpacing(5)

        ######## 显示模块的开始
        # 创建显示端的实线框架（QFrame）作为分隔区域
        self.Showseparator = QFrame(self)
        self.Showseparator.setFixedSize(700, 700)
        self.Showseparator.setStyleSheet("""
                    QFrame {
                        background-color: #E3E3E3;  /* 淡灰色背景 */
                        border-radius: 10px;  /* 圆角边框 */
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);  /* 轻微阴影 */
                    }
                """)

        # 创建显示分区1
        self.Showseparator_Frame1 = QFrame(self.Showseparator)
        self.Showseparator_Frame1.setStyleSheet("""
                    QFrame {
                        background-color: #E3E3E3;  /* 淡灰色背景 */
                        border-radius: 10px;  /* 圆角边框 */
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);  /* 轻微阴影 */
                    }
                """)

        """ 创建图形控件 """
        self.graphWidget1 = pg.PlotWidget()
        self.setupGraphWidget(self.graphWidget1, "Speed/RPM", "rpm", "time/s")
        # 创建一个图形数据项
        self.plotDataItem = self.graphWidget1.plot(self.x, self.y, pen='r')

        # 创建电机1显示布局
        self.Showseparator_Frame1_Layout = QVBoxLayout(self.Showseparator_Frame1)
        self.Showseparator_Frame1_Layout.addWidget(self.graphWidget1)

        # 创建显示分区2
        self.Showseparator_Frame2 = QFrame(self.Showseparator)
        self.Showseparator_Frame2.setStyleSheet("""
                    QFrame {
                        background-color: #E3E3E3;  /* 淡灰色背景 */
                        border-radius: 10px;  /* 圆角边框 */
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);  /* 轻微阴影 */
                    }
                """)

        self.graphWidget2 = pg.PlotWidget()
        self.setupGraphWidget(self.graphWidget2, "Position", "degree", "time/s")

        # 创建电机2显示布局
        self.Showseparator_Frame2_Layout = QVBoxLayout(self.Showseparator_Frame2)
        self.Showseparator_Frame2_Layout.addWidget(self.graphWidget2)

        # 创建垂直布局将两个框架添加到布局中
        self.ShowLayout = QVBoxLayout(self.Showseparator)
        self.ShowLayout.addWidget(self.graphWidget1)
        self.ShowLayout.addWidget(self.graphWidget2)
        self.ShowLayout.setSpacing(0)

        # 视频播放器组件
        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        # 加载视频文件
        self.mediaPlayer.setSource(QUrl.fromLocalFile("../Icons/cool3.mp4"))
        self.mediaPlayer.play()
        # 连接信号
        self.mediaPlayer.mediaStatusChanged.connect(self.media_status_changed)
        self.videoWidget.setFixedSize(400, 350)

        # 创建水平布局
        self.Sub2Mainlayout = QHBoxLayout()
        self.Sub2Mainlayout .addWidget(self.Controlseparator)
        self.Sub2Mainlayout .addWidget(self.Showseparator)
        self.Sub2Mainlayout .addWidget(self.videoWidget)


        # 将布局设置为子窗口的布局
        self.setLayout(self.Sub2Mainlayout )



    def create_button(self, text, width, height):
        """
        创建一个定制样式的 QPushButton。

        :param text: 按钮显示的文本。
        :param width: 按钮的宽度。
        :param height: 按钮的高度。
        :return: QPushButton对象
        """
        button = QPushButton(text)
        button.setFixedSize(width, height)
        button.setStyleSheet("""
            QPushButton {
                background-color: #F0F8FF;  /* 淡蓝色背景 */
                color: black;               /* 文字颜色 */
                border-radius: 5px;         /* 圆角 */
                padding: 5px;               /* 内边距 */
                border: 1px solid #A9A9A9;  /* 边框 */
            }
            QPushButton:hover {
                background-color: #ADD8E6;  /* 悬浮时背景颜色变化 */
            }
            QPushButton:pressed {
                background-color: #87CEEB;  /* 按下时背景颜色变化 */
            }
        """)
        return button

    def create_line_edit(self, placeholder_text, width, height):
        """
        创建一个定制样式的 QLineEdit。

        :param placeholder_text: 占位符文本。
        :param width: 输入框的宽度。
        :param height: 输入框的高度。
        :return: QLineEdit对象
        """
        line_edit = QLineEdit()
        line_edit.setFixedSize(width, height)
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setStyleSheet("""
            QLineEdit {
                background-color: #F0F8FF;  /* 输入框的背景颜色 */
                color: black;               /* 输入文字的颜色 */
                border: 1px solid #A9A9A9;  /* 边框颜色和大小 */
                border-radius: 5px;         /* 边框圆角 */
                padding: 3px;               /* 内边距 */
            }
            QLineEdit:focus {
                border: 1px solid #87CEEB;  /* 焦点时边框颜色 */
            }
            QLineEdit:hover {
                border: 1px solid #ADD8E6;  /* 鼠标悬停时边框颜色 */
            }
        """)
        return line_edit

    def create_label(self, text, font_name="Segoe UI", font_size=10, bold=False, color="#000000"):
        """
        创建一个具有特定字体和颜色的 QLabel 对象。

        :param text: 标签上显示的文本。
        :param font_name: 字体名称，默认为 'Segoe UI'。
        :param font_size: 字体大小，默认为 10。
        :param bold: 是否加粗，默认为 False。
        :param color: 字体颜色，默认为黑色。
        :return: QLabel对象
        """
        label = QLabel(text)
        font = QFont(font_name, font_size)
        font.setBold(bold)
        label.setFont(font)
        label.setFixedSize(170, 20)
        label.setStyleSheet(f"color: {color};")
        return label

    def setupGraphWidget(self, graphWidget, title, ylabel, xlabel):
        graphWidget.setBackground('#F5FFFA')
        graphWidget.setTitle(title, color="#000080", size="15pt")
        graphWidget.setLabel('left', ylabel, color="#000080", size=30)
        graphWidget.setLabel('bottom', xlabel, color="#000080", size=30)
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
                self.indicatior.setStyleSheet("""
                    QLabel {
                        background-color: #D3D3D3;  /* 淡灰色背景 */
                        border-radius: 10px;        /* 设置圆角为高度的一半 */
                        width:  20px;                /* 设置宽度 */
                        height: 20px;               /* 设置高度 */
                    }
                """)
                self.show_auto_close_dialog("Serial State: " + message, 1000)
            else:
                self.show_auto_close_dialog("Serial State: " + message, 1000)
        else:
            success, message = self.OpenSeri.open_ser(self.selected_port, self.selected_baud)
            if success:
                self.indicatior.setStyleSheet("""
                    QLabel {
                        background-color: #00CD66;  /* 淡绿色背景 */
                        border-radius: 10px;        /* 设置圆角为高度的一半 */
                        width:  20px;                /* 设置宽度 */
                        height: 20px;               /* 设置高度 */
                    }
                """)
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

            CRC_bytes = self.OpenSeri.CalCRC_16(HeaderCode, contcommand, parameter_bytes)
            print(f"CRC-16校验值: 0x{CRC_bytes:04X}")
            print("para: ", parameter_bytes, type(parameter_bytes))
            DataPacket = self.OpenSeri.create_data_packet(HeaderCode, contcommand, parameter_bytes, CRC_bytes)
            hex_data_packet = ''.join([f'{byte:02x}' for byte in DataPacket])
            print("Data Packet in PostCommandInfo: ", hex_data_packet)
            self.OpenSeri.send_msg(DataPacket)
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
            if Pvalue == '' and Ivalue == '' and Dvalue == '':
                self.show_auto_close_dialog("Error: please input PID value", 2000)
                return  # Return early if parameter is empty
            """
            PID参数，一般是正数
            """
            # 转换浮点数为整数，用1000倍来保留三位小数,默认值设置为0
            Pvalue = int(float(Pvalue) * 1000) if Pvalue else 0
            if not 0 <= Pvalue <= 16777215:
                self.show_auto_close_dialog("范围错误: P值超出范围。它必须在0到16777之间。", 2000)
                return
            Pvalue_bytes = Pvalue.to_bytes(3, byteorder='little', signed=False)

            Ivalue = int(float(Ivalue) * 1000) if Ivalue else 0
            if not 0 <= Ivalue <= 16777215000:
                self.show_auto_close_dialog("范围错误: I值超出范围。它必须在0到16777之间。", 2000)
                return
            Ivalue_bytes = Ivalue.to_bytes(3, byteorder='little', signed=False)

            Dvalue = int(float(Dvalue) * 1000) if Dvalue else 0
            if not 0 <= Dvalue <= 65535000:
                self.show_auto_close_dialog("范围错误: D值超出范围。它必须在0到65之间。", 2000)
                return
            Dvalue_bytes = Dvalue.to_bytes(2, byteorder='little', signed=False)

            PID_para = Pvalue_bytes + Ivalue_bytes + Dvalue_bytes
            CRC_bytes = self.OpenSeri.CalCRC_16(HeaderCode, contcommand, PID_para)
            print(f"CRC-16校验值: 0x{CRC_bytes:04X}")
            print("Pvalue: ", Pvalue_bytes, type(Pvalue_bytes))
            print("Ivalue: ", Ivalue_bytes, type(Ivalue_bytes))
            print("Dvalue: ", Dvalue_bytes, type(Dvalue_bytes))
            DataPacket = self.OpenSeri.create_data_packet(HeaderCode, contcommand, PID_para, CRC_bytes)
            hex_data_packet = ''.join([f'{byte:02x}' for byte in DataPacket])
            print("Data Packet in PostCommandInfo: ", hex_data_packet)
            self.OpenSeri.send_msg(DataPacket)
        except Exception as e:
            print("Error while sending PID data:", e)
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
        self.plotDataItem.setData(self.x, self.y)
        # self.graphWidget1.plot(self.x, self.y, pen=pg.mkPen(color=(255, 0, 0), width=5))

    def media_status_changed(self, status):
        # 检查媒体播放状态
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.mediaPlayer.play()  # 重复播放视频

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("神策电机调试助手")
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
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        # 创建堆叠窗口
        self.stacked_widget.addWidget(self.subWindow1)
        self.stacked_widget.addWidget(self.subWindow2)
        self.stacked_widget.addWidget(self.subWindow3)
        self.stacked_widget.addWidget(self.subWindow4)


        self.createButton("串口调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow1))
        self.createButton("PID调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow2))
        self.createButton("摄像头调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow3))
        self.createButton("网络调试助手", button_layout, lambda: self.stacked_widget.setCurrentWidget(self.subWindow4))

        # 加载视频文件
        self.mediaPlayer.setSource(QUrl.fromLocalFile("../Icons/COOL2.mp4"))
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
        button.setStyleSheet("""
            QPushButton {
                background-color: #5CACEE;  # 一个明亮的天蓝色
                color: white;
                border-radius: 10px;  # 圆角
                padding: 10px;
                margin: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B9C9C;  # 悬停时的颜色变化
            }
        """)
        button.clicked.connect(callback)
        layout.addWidget(button)








