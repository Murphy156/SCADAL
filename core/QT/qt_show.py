import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, QGraphicsEllipseItem
from core.DataAnalysis.DataDeal import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QPropertyAnimation, QByteArray, QEasingCurve, Qt

class SubWindow1(QDialog):
    def __init__(self):
        super().__init__()

        # 创建一个子界面容器
        sub_widget = QWidget()

        # 创建串口和波特率的选择
        self.selected_port = None
        self.selected_baud = None

        # 设置子窗口的背景颜色
        self.setStyleSheet("background-color: #bfc6c7;")

        # 创建子界面的主水平布局
        MainLayout = QHBoxLayout()

        sub_widget.setLayout(MainLayout)


        # 创建控制框的垂直布局
        ControlLayout = QVBoxLayout()

        # 将控制框的界面放入到主框的左边
        MainLayout.addLayout(ControlLayout)

        # 创建控制框中的串口设置垂直分布布局
        ContSeriLayout = QVBoxLayout()

        # 将串口设置布局放入控制框中的垂直分布中
        ControlLayout.addLayout(ContSeriLayout)

        # 创建控制框中的电机控制面板设置的垂直分布
        ContMotCLayout = QVBoxLayout()

        # 将电机控制面板设置放入控制框中的垂直分布
        ControlLayout.addLayout(ContMotCLayout)


# program start 这里是设置串口设置的布局
        lable1 = QLabel("Serial Port Configuration", )
        lable1.setFixedSize(200, 20)
        lable1.setStyleSheet("color: black")

        # 创建一个字体对象
        font1 = QFont()
        font1.setPointSize(15)  # 设置字体大小
        font1.setBold(True)     # 设置为粗体
        lable1.setFont(font1)
        # 将第一个文本框放在串口设置布局中
        ContSeriLayout.addWidget(lable1)

        # 串口布局安排
        PortLayout = QHBoxLayout()
        lable2 = QLabel("Port")
        lable2.setStyleSheet("color: black")

        font2 = QFont()
        font2.setPointSize(10)  # 设置字体大小
        font2.setBold(True)     # 设置为粗体
        lable2.setFont(font2)

        PortLayout.addWidget(lable2)

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
        COM.setStyleSheet("background-color: #bfc6c7; color: black")
        PortLayout.addWidget(COM)
        # 将COM和BAUD作为类的成员变量
        self.COM = COM

        # 将PortLayout放在ControlLayout
        ContSeriLayout.addLayout(PortLayout)


        # 波特率布局安排
        BaudLayout = QHBoxLayout()
        lable3 = QLabel("Baudrate")
        lable3.setStyleSheet("background-color: #bfc6c7; color: black")

        lable3.setFont(font2)

        BaudLayout.addWidget(lable3)

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
        BaudLayout.addWidget(BAUD)
        BAUD.setStyleSheet("background-color: #bfc6c7; color: black")
        # 将COM和BAUD作为类的成员变量
        self.BAUD = BAUD
        # BaudLayout
        ContSeriLayout.addLayout(BaudLayout)

        CommunicationLayout = QHBoxLayout()
        self.indicatior = QLabel()
        self.indicatior.setFixedSize(20, 20)
        self.indicatior.setStyleSheet("background-color: gray; border-radius: 10px;")
        CommunicationLayout.addWidget(self.indicatior)

        post_com_button = QPushButton("Open Serial")
        post_com_button.setFixedSize(80, 20)  # 设置按钮1的尺寸
        post_com_button.setStyleSheet("background-color: #838787; color: #d7dbdb")
        post_com_button.clicked.connect(self.PostSerialInfo)
        CommunicationLayout.addWidget(post_com_button)

        ContSeriLayout.addLayout(CommunicationLayout)
#program end


##program2 start 这里是创建电机控制面板模块的
        lable5 = QLabel("SpeedSet/RPM")
        lable5.setFixedSize(100, 15)
        lable5.setStyleSheet("background-color: #bfc6c7; color: black")
        ContMotCLayout.addWidget(lable5)

        # pump1的控制框
        Pump1Layout = QHBoxLayout()
        self.Pump1RPMEdit = QLineEdit(self)
        self.Pump1RPMEdit.setFixedSize(80, 20)
        self.Pump1RPMEdit.setPlaceholderText('Pump1')
        self.Pump1RPMEdit.setStyleSheet("background-color: #c1c7c7; color: black")
        Pump1Layout.addWidget(self.Pump1RPMEdit)

        Pump1Button1 = QPushButton("Enable")
        Pump1Button1.setFixedSize(50, 20)
        Pump1Button1.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump1Button1.clicked.connect(lambda: self.PostCommandInfo(0x1, self.Pump1RPMEdit.text()))
        Pump1Layout.addWidget(Pump1Button1)

        Pump1Button2 = QPushButton("Disable")
        Pump1Button2.setFixedSize(50, 20)
        Pump1Button2.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump1Button2.clicked.connect(lambda: self.PostCommandInfo(0x2, 0x0))
        Pump1Layout.addWidget(Pump1Button2)

        Pump1Button3 = QPushButton("Change")
        Pump1Button3.setFixedSize(50, 20)
        Pump1Button3.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump1Button3.clicked.connect(lambda: self.PostCommandInfo(0x11, self.Pump1RPMEdit.text()))
        Pump1Layout.addWidget(Pump1Button3)
        ContMotCLayout.addLayout(Pump1Layout)

        # pump2的控制框
        Pump2Layout = QHBoxLayout()
        self.Pump2RPMEdit = QLineEdit(self)
        self.Pump2RPMEdit.setFixedSize(80, 20)
        self.Pump2RPMEdit.setPlaceholderText('Pump2')
        self.Pump2RPMEdit.setStyleSheet("background-color: #c1c7c7; color: black")
        Pump2Layout.addWidget(self.Pump2RPMEdit)

        Pump2Button1 = QPushButton("Enable")
        Pump2Button1.setFixedSize(50, 20)
        Pump2Button1.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump2Button1.clicked.connect(lambda: self.PostCommandInfo(0x3, self.Pump2RPMEdit.text()))
        Pump2Layout.addWidget(Pump2Button1)

        Pump2Button2 = QPushButton("Disable")
        Pump2Button2.setFixedSize(50, 20)
        Pump2Button2.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump2Button2.clicked.connect(lambda: self.PostCommandInfo(0x4, 0x0))
        Pump2Layout.addWidget(Pump2Button2)

        Pump2Button3 = QPushButton("Change")
        Pump2Button3.setFixedSize(50, 20)
        Pump2Button3.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump2Button3.clicked.connect(lambda: self.PostCommandInfo(0x12, self.Pump2RPMEdit.text()))
        Pump2Layout.addWidget(Pump2Button3)
        ContMotCLayout.addLayout(Pump2Layout)

        # pump3的控制框
        Pump3Layout = QHBoxLayout()
        self.Pump3RPMEdit = QLineEdit(self)
        self.Pump3RPMEdit.setFixedSize(80, 20)
        self.Pump3RPMEdit.setPlaceholderText('Pump3')
        self.Pump3RPMEdit.setStyleSheet("background-color: #c1c7c7; color: black")
        Pump3Layout.addWidget(self.Pump3RPMEdit)

        Pump3Button1 = QPushButton("Enable")
        Pump3Button1.setFixedSize(50, 20)
        Pump3Button1.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump3Button1.clicked.connect(lambda: self.PostCommandInfo(0x5, self.Pump3RPMEdit.text()))
        Pump3Layout.addWidget(Pump3Button1)

        Pump3Button2 = QPushButton("Disable")
        Pump3Button2.setFixedSize(50, 20)
        Pump3Button2.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump3Button2.clicked.connect(lambda: self.PostCommandInfo(0x6, 0x0))
        Pump3Layout.addWidget(Pump3Button2)

        Pump3Button3 = QPushButton("Change")
        Pump3Button3.setFixedSize(50, 20)
        Pump3Button3.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump3Button3.clicked.connect(lambda: self.PostCommandInfo(0x13, self.Pump3RPMEdit.text()))
        Pump3Layout.addWidget(Pump3Button3)
        ContMotCLayout.addLayout(Pump3Layout)

        # pump4的控制框
        Pump4Layout = QHBoxLayout()
        self.Pump4RPMEdit = QLineEdit(self)
        self.Pump4RPMEdit.setFixedSize(80, 20)
        self.Pump4RPMEdit.setPlaceholderText('Pump4')
        self.Pump4RPMEdit.setStyleSheet("background-color: #c1c7c7; color: black")
        Pump4Layout.addWidget(self.Pump4RPMEdit)

        Pump4Button1 = QPushButton("Enable")
        Pump4Button1.setFixedSize(50, 20)
        Pump4Button1.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump4Button1.clicked.connect(lambda: self.PostCommandInfo(0x7, self.Pump4RPMEdit.text()))
        Pump4Layout.addWidget(Pump4Button1)

        Pump4Button2 = QPushButton("Disable")
        Pump4Button2.setFixedSize(50, 20)
        Pump4Button2.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump4Button2.clicked.connect(lambda: self.PostCommandInfo(0x8, 0x0))
        Pump4Layout.addWidget(Pump4Button2)

        Pump4Button3 = QPushButton("Change")
        Pump4Button3.setFixedSize(50, 20)
        Pump4Button3.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump4Button3.clicked.connect(lambda: self.PostCommandInfo(0x14, self.Pump4RPMEdit.text()))
        Pump4Layout.addWidget(Pump4Button3)
        ContMotCLayout.addLayout(Pump4Layout)

        # pump5的控制框
        Pump5Layout = QHBoxLayout()
        self.Pump5RPMEdit = QLineEdit(self)
        self.Pump5RPMEdit.setFixedSize(80, 20)
        self.Pump5RPMEdit.setPlaceholderText('Pump4')
        self.Pump5RPMEdit.setStyleSheet("background-color: #c1c7c7; color: black")
        Pump5Layout.addWidget(self.Pump5RPMEdit)

        Pump5Button1 = QPushButton("Enable")
        Pump5Button1.setFixedSize(50, 20)
        Pump5Button1.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump5Button1.clicked.connect(lambda: self.PostCommandInfo(0x9, self.Pump5RPMEdit.text()))
        Pump5Layout.addWidget(Pump5Button1)

        Pump5Button2 = QPushButton("Disable")
        Pump5Button2.setFixedSize(50, 20)
        Pump5Button2.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump5Button2.clicked.connect(lambda: self.PostCommandInfo(0xA, 0x0))
        Pump5Layout.addWidget(Pump5Button2)

        Pump5Button3 = QPushButton("Change")
        Pump5Button3.setFixedSize(50, 20)
        Pump5Button3.setStyleSheet("background-color: #838787; color: #d7dbdb")
        Pump5Button3.clicked.connect(lambda: self.PostCommandInfo(0x15, self.Pump5RPMEdit.text()))
        Pump5Layout.addWidget(Pump5Button3)
        ContMotCLayout.addLayout(Pump5Layout)

##program2 end

# 放入显示组件
        # 创建两组显示组件垂直布局图
        GraAllLayout = QHBoxLayout()
        GraAllLayout.setSpacing(0)
        GraLayout1 = QVBoxLayout()
        GraLayout2 = QVBoxLayout()
        GraLayout1.setSpacing(0)
        GraLayout2.setSpacing(0)
        GraAllLayout.addLayout(GraLayout1)
        GraAllLayout.addLayout(GraLayout2)
        MainLayout.addLayout(GraAllLayout)

        Grab1Lable = QLabel("Pump 1")
        Gra1 = self.create_axis()
        GraLayout1.addWidget(Gra1)
        Grab1Lable.setStyleSheet("background-color: #18191c; color: white")
        Grab1Lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        GraLayout1.addWidget(Grab1Lable)

        Grab2Lable = QLabel("Pump 2")
        Gra2 = self.create_axis()
        GraLayout1.addWidget(Gra2)
        Grab2Lable.setStyleSheet("background-color: #18191c; color: white")
        Grab2Lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        GraLayout1.addWidget(Grab2Lable)

        Grab3Lable = QLabel("Pump 3")
        Gra3 = self.create_axis()
        GraLayout2.addWidget(Gra3)
        Grab3Lable.setStyleSheet("background-color: #18191c; color: white")
        Grab3Lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        GraLayout2.addWidget(Grab3Lable)

        Grab4Lable = QLabel("Pump 4")
        Gra4 = self.create_axis()
        GraLayout2.addWidget(Gra4)
        Grab4Lable.setStyleSheet("background-color: #18191c; color: white")
        Grab4Lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        GraLayout2.addWidget(Grab4Lable)

        self.setLayout(MainLayout)

    def PostSerialInfo(self):
        self.selected_port = self.COM.currentText()
        self.selected_baud = int(self.BAUD.currentText())
        OpenSeri = SerialCommunication()
        if self.indicatior.styleSheet() == "background-color: gray; border-radius: 10px;":
            self.indicatior.setStyleSheet("background-color: green; border-radius: 10px;")
            self.COM.setDisabled(True)
            self.BAUD.setDisabled(True)
            OpenSeri.open_ser(self.selected_port, self.selected_baud)
        else:
            self.indicatior.setStyleSheet("background-color: gray; border-radius: 10px;")
            self.COM.setEnabled(True)
            self.BAUD.setEnabled(True)
            OpenSeri.close_ser()
        print("Selected port:", self.selected_port)
        print("Selected baud rate:", self.selected_baud)

    def PostCommandInfo(self, contcommand, parameter):
        try:
            HeaderCode = 0x55AA
            CombinPost = SerialCommunication()

            if parameter == '':
                print("Parameter is empty. Please enter a value.")
                return  # Return early if parameter is empty

            # 检测parameter是否为负数
            if isinstance(parameter, int) and parameter < 0:
                # Convert negative integers to bytes
                parameter_bytes = parameter.to_bytes(4, byteorder='little', signed=True)
            else:
                # Convert non-negative integers to bytes
                parameter_bytes = int(parameter).to_bytes(4, byteorder='little', signed=False)

            CRC_bytes = CombinPost.CalCRC_16(HeaderCode, contcommand, parameter_bytes)
            print(f"CRC-16校验值: 0x{CRC_bytes:04X}")
            print("para: ", parameter_bytes, type(parameter_bytes))
            DataPacket = CombinPost.create_data_packet(HeaderCode, contcommand, parameter_bytes, CRC_bytes)
            hex_data_packet = ''.join([f'{byte:02x}' for byte in DataPacket])
            print("Data Packet in PostCommandInfo: ", hex_data_packet)
            CombinPost.send_msg(DataPacket)
        except Exception as e:
            print("An exception occurred:", str(e))


    def create_axis(self):
        # 创建一个 QGraphicsView
        graphics_view = QGraphicsView()

        # 设置场景
        scene = QGraphicsScene()
        graphics_view.setScene(scene)

        # 调整可视化显示的大小
        width = 300  # 根据需要调整
        height = 300  # 根据需要调整

        # 创建左侧的y轴（速度）
        y_axis = QGraphicsLineItem(0, 0, 0, height)
        y_axis.setPen(QPen(QColor("white")))
        scene.addItem(y_axis)

        # 创建x轴（时间）
        x_axis = QGraphicsLineItem(0, height / 2, width, height / 2)
        x_axis.setPen(QPen(QColor("white")))
        scene.addItem(x_axis)

        # 添加网格
        for i in range(0, int(width) + 1, int(width / 8)):
            grid_line = QGraphicsLineItem(i, 0, i, height)
            grid_line.setPen(QPen(QColor("#555555")))  # 设置网格线颜色
            scene.addItem(grid_line)

        for i in range(0, int(height) + 1, int(height / 8)):
            grid_line = QGraphicsLineItem(0, i, width, i)
            grid_line.setPen(QPen(QColor("#555555")))  # 设置网格线颜色
            scene.addItem(grid_line)


        # 为x轴添加刻度线和标签
        for i in range(0, int(width) + 1, int(width / 4)):
            tick = QGraphicsLineItem(i, height / 2 - 5, i, height / 2 + 5)
            tick.setPen(QPen(QColor("white")))  # 设置刻度线颜色为白色
            scene.addItem(tick)
            label = QGraphicsTextItem(str(i))
            label.setPos(i - 10, height / 2 + 142)
            label.setDefaultTextColor(QColor("white"))
            scene.addItem(label)

        # 为y轴添加刻度线和标签
        for i in range(-200, 201, 50):
            tick = QGraphicsLineItem(-5, height * (1 - (i + 200) / 400), 5, height * (1 - (i + 200) / 400))
            tick.setPen(QPen(QColor("white")))  # 设置刻度线颜色为白色
            scene.addItem(tick)
            label = QGraphicsTextItem(str(i))
            label.setPos(-40, height * (1 - (i + 200) / 400) - 10)
            label.setDefaultTextColor(QColor("white"))
            scene.addItem(label)

        graphics_view.setStyleSheet("background-color: #18191c;")

        return graphics_view



class SubWindow2(QDialog):
    def __init__(self):
        super().__init__()

        # 设置子窗口的背景颜色
        self.setStyleSheet("background-color: #F5FFFA;")

        # 创建控制端的实线框架（QFrame）作为分隔区域
        Controlseparator = QFrame(self)
        Controlseparator.setStyleSheet("background-color: #F5FFFA;")
        Controlseparator.setFrameShape(QFrame.Shape.Box)
        Controlseparator.setFrameShadow(QFrame.Shadow.Sunken)
        Controlseparator.setFixedSize(240, 700)

        Controlseparator_Frame1 = QFrame(Controlseparator)
        Controlseparator_Frame1.setStyleSheet("background-color: #F5FFFA;")
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
        COM.setStyleSheet("background-color: #F0FFF0; color: black")
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
        BAUD.setStyleSheet("background-color: #F0FFF0; color: black")
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
        post_com_button.setStyleSheet("background-color: #F0FFF0; color: black")
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
        # Controlseparator_Frame1_Layout.setSpacing(5)

########## 控制面板中的框架2
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
        PIDButton.setStyleSheet("background-color: #F0FFF0; color: black")
#        Pump4Button1.clicked.connect(lambda: self.PostCommandInfo(0x7, self.Pump4RPMEdit.text()))

        # 转速设定
        lable_speed = QLabel("Speed Set")
        lable_speed.setFixedSize(80, 15)
        lable_speed.setStyleSheet("color: black")
        lable_speed.setFont(font1)

        self.SpeedRPMEdit = QLineEdit(self)
        self.SpeedRPMEdit.setFixedSize(60, 22)
        self.SpeedRPMEdit.setPlaceholderText('100')
        self.SpeedRPMEdit.setStyleSheet("background-color:#F0F8FF; color: black")

        # speed的控制框的水平布局设置
        speed_Layout = QHBoxLayout()
        speed_Layout.addWidget(lable_speed)
        speed_Layout.addWidget(self.SpeedRPMEdit)
        speed_Layout.setSpacing(2)

        # 创建控制面板中电机控制框架的布局
        Controlseparator_Frame2_Layout = QVBoxLayout(Controlseparator_Frame2)
        Controlseparator_Frame2_Layout.addWidget(label5)
        Controlseparator_Frame2_Layout.addLayout(P_Layout)
        Controlseparator_Frame2_Layout.addLayout(I_Layout)
        Controlseparator_Frame2_Layout.addLayout(D_Layout)
        Controlseparator_Frame2_Layout.addWidget(PIDButton)
        Controlseparator_Frame2_Layout.addLayout(speed_Layout)
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
        Showseparator_Frame1.setFixedSize(900, 350)


        label6 = QLabel("Speed Display")
        label6.setStyleSheet("color: black")
        label6.setFixedSize(180, 20)
        label6.setFont(font1)

        # 创建坐标轴
        Grab1Lable = QLabel("Pump 1")
        Gra1 = self.create_axis()
        Grab1Lable.setStyleSheet("background-color: #F5FFFA; color: black")
        Grab1Lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建电机1显示布局
        Showseparator_Frame1_Layout = QVBoxLayout(Showseparator_Frame1)
        Showseparator_Frame1_Layout.addWidget(label6)
        Showseparator_Frame1_Layout.addWidget(Grab1Lable)
        Showseparator_Frame1_Layout.addWidget(Gra1)

        # 创建显示分区2
        Showseparator_Frame2 = QFrame(Showseparator)
        Showseparator_Frame2.setStyleSheet("background-color: #F5FFFA;")
        Showseparator_Frame2.setFrameShape(QFrame.Shape.Box)
        Showseparator_Frame2.setFrameShadow(QFrame.Shadow.Sunken)
        Showseparator_Frame2.setFixedSize(900, 350)

        # 创建坐标轴
        Grab2Lable = QLabel("Pump 2")
        Gra2 = self.create_axis()
        Grab2Lable.setStyleSheet("background-color: #F5FFFA; color: black")
        Grab2Lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建电机2显示布局
        Showseparator_Frame2_Layout = QVBoxLayout(Showseparator_Frame2)
        Showseparator_Frame2_Layout.addWidget(Grab2Lable)
        Showseparator_Frame2_Layout.addWidget(Gra2)

        # 创建垂直布局将两个框架添加到布局中
        ShowLayout = QVBoxLayout(Showseparator)
        ShowLayout.addWidget(Showseparator_Frame1)
        ShowLayout.addWidget(Showseparator_Frame2)
        ShowLayout.setSpacing(0)



        # 创建水平布局
        Sub2Mainlayout = QHBoxLayout()
        Sub2Mainlayout.addWidget(Controlseparator)
        Sub2Mainlayout.addWidget(Showseparator)

        # 将布局设置为子窗口的布局
        self.setLayout(Sub2Mainlayout)

    def PostSerialInfo(self):
        self.selected_port = self.COM.currentText()
        self.selected_baud = int(self.BAUD.currentText())
        OpenSeri = SerialCommunication()
        if self.indicatior.styleSheet() == "background-color: gray; border-radius: 10px;":
            self.indicatior.setStyleSheet("background-color: green; border-radius: 10px;")
            self.COM.setDisabled(True)
            self.BAUD.setDisabled(True)
            OpenSeri.open_ser(self.selected_port, self.selected_baud)
        else:
            self.indicatior.setStyleSheet("background-color: gray; border-radius: 10px;")
            self.COM.setEnabled(True)
            self.BAUD.setEnabled(True)
            OpenSeri.close_ser()
        print("Selected port:", self.selected_port)
        print("Selected baud rate:", self.selected_baud)

    def PostCommandInfo(self, contcommand, parameter):
        try:
            HeaderCode = 0x55AA
            CombinPost = SerialCommunication()
            if parameter == '':
                print("Parameter is empty. Please enter a value.")
                return  # Return early if parameter is empty

            parameter = int(parameter)

            # 检测parameter是否为负数
            if isinstance(parameter, int) and parameter < 0:
                # Convert negative integers to bytes
                parameter_bytes = parameter.to_bytes(4, byteorder='little', signed=True)
            else:
                # Convert non-negative integers to bytes
                parameter_bytes = int(parameter).to_bytes(4, byteorder='little', signed=False)

            CRC_bytes = CombinPost.CalCRC_16(HeaderCode, contcommand, parameter_bytes)
            print(f"CRC-16校验值: 0x{CRC_bytes:04X}")
            print("para: ", parameter_bytes, type(parameter_bytes))
            DataPacket = CombinPost.create_data_packet(HeaderCode, contcommand, parameter_bytes, CRC_bytes)
            hex_data_packet = ''.join([f'{byte:02x}' for byte in DataPacket])
            print("Data Packet in PostCommandInfo: ", hex_data_packet)
            CombinPost.send_msg(DataPacket)
        except Exception as e:
            print("An exception occurred:", str(e))

    def create_axis(self):
        # 创建一个 QGraphicsView
        graphics_view = QGraphicsView()

        # 设置场景
        scene = QGraphicsScene()
        graphics_view.setScene(scene)

        # 调整可视化显示的大小
        width = 800  # 根据需要调整
        height = 220  # 根据需要调整

        # 创建左侧的y轴（速度）
        y_axis = QGraphicsLineItem(0, 0, 0, height)
        y_axis.setPen(QPen(QColor("black")))
        scene.addItem(y_axis)

        # 创建x轴（时间）
        x_axis = QGraphicsLineItem(0, height / 2, width, height / 2)
        x_axis.setPen(QPen(QColor("black")))
        scene.addItem(x_axis)

        # 添加网格
        for i in range(0, int(width) + 1, int(width / 8)):
            grid_line = QGraphicsLineItem(i, 0, i, height)
            grid_line.setPen(QPen(QColor("#808080")))  # 设置网格线颜色
            scene.addItem(grid_line)

        for i in range(0, int(height) + 1, int(height / 8)):
            grid_line = QGraphicsLineItem(0, i, width, i)
            grid_line.setPen(QPen(QColor("#808080")))  # 设置网格线颜色
            scene.addItem(grid_line)


        # 为x轴添加刻度线和标签
        for i in range(0, int(width) + 1, int(width / 4)):
            tick = QGraphicsLineItem(i, height / 2 - 5, i, height / 2 + 5)
            tick.setPen(QPen(QColor("black")))
            scene.addItem(tick)
            label = QGraphicsTextItem(str(i))
            label.setPos(i - 10, height / 2 + 120)
            label.setDefaultTextColor(QColor("black"))
            scene.addItem(label)

        # 为y轴添加刻度线和标签
        for i in range(-200, 201, 50):
            tick = QGraphicsLineItem(-5, height * (1 - (i + 200) / 400), 5, height * (1 - (i + 200) / 400))
            tick.setPen(QPen(QColor("black")))
            scene.addItem(tick)
            label = QGraphicsTextItem(str(i))
            label.setPos(-40, height * (1 - (i + 200) / 400) - 10)
            label.setDefaultTextColor(QColor("black"))
            scene.addItem(label)

        graphics_view.setStyleSheet("background-color: #F5FFFA;")

        return graphics_view

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

        self.setWindowTitle("Peristaltic Pump Debugging Assistant")
        self.setGeometry(300, 200, 1000, 800)
        # 创建一个主界面容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建垂直布局
        main_layout = QVBoxLayout()

        # 设置主窗口容器的布局为垂直布局
        main_widget.setLayout(main_layout)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        # 创建四个按钮
        button1 = QPushButton("串口调试助手")
        button1.setFixedSize(300, 50)  # 设置按钮1的尺寸
        button1.clicked.connect(self.open_window1)
        button1.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(button1)


        button2 = QPushButton("PID调试助手")
        button2.setFixedSize(300, 50)  # 设置按钮2的尺寸
        button2.clicked.connect(self.open_window2)
        button2.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(button2)

        button3 = QPushButton("摄像头调试助手")
        button3.setFixedSize(300, 50)  # 设置按钮3的尺寸
        button3.clicked.connect(self.open_window3)
        button3.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(button3)

        button4 = QPushButton("网络调试助手")
        button4.setFixedSize(300, 50)  # 设置按钮4的尺寸
        button4.clicked.connect(self.open_window4)
        button4.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(button4)

        button_layout.setSpacing(0)

        # 添加水平布局到垂直布局
        main_layout.addLayout(button_layout)

        # 设置主窗口的背景颜色
        self.setStyleSheet("background-color: lightblack;")

        # 创建一个堆叠窗口，用于显示子窗口
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        main_layout.setSpacing(0)

    def open_window1(self):
        sub_window1 = SubWindow1()
        self.stacked_widget.addWidget(sub_window1)
        self.stacked_widget.setCurrentWidget(sub_window1)
        self.setWindowTitle("串口调试助手")

    def open_window2(self):
        sub_window2 = SubWindow2()
        self.stacked_widget.addWidget(sub_window2)
        self.stacked_widget.setCurrentWidget(sub_window2)
        self.setWindowTitle("PID调试助手")


    def open_window3(self):
        sub_window3 = SubWindow3()
        self.stacked_widget.addWidget(sub_window3)
        self.stacked_widget.setCurrentWidget(sub_window3)
        self.setWindowTitle("摄像头调试助手")

    def open_window4(self):
        sub_window4 = SubWindow4()
        self.stacked_widget.addWidget(sub_window4)
        self.stacked_widget.setCurrentWidget(sub_window4)
        self.setWindowTitle("网络调试助手")









