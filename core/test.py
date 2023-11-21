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
        button.setStyleSheet("background-color: gray; color: white;")
        button.clicked.connect(callback)
        layout.addWidget(button)