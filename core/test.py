from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtMultimedia import QMediaPlayer, QMediaMetaData
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Video Player")

        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()

        # 设置中央窗口为视频窗口
        self.setCentralWidget(self.videoWidget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        try:
            # 加载视频文件
            self.mediaPlayer.setSource(QUrl.fromLocalFile("../Icons/cool.mp4"))

            # 播放视频
            self.mediaPlayer.play()

            # 连接信号
            self.mediaPlayer.errorOccurred.connect(self.handle_error)
            self.mediaPlayer.mediaStatusChanged.connect(self.handle_status_change)

        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_error(self, error):
        print(f"Error occurred: {error}")

    def handle_status_change(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            metadata = self.mediaPlayer.metaData()
            print(f"Video duration: {metadata.get(QMediaMetaData.Duration)}")
        else:
            print(f"Media status changed: {status}")


app = QApplication([])
window = VideoWindow()
window.show()
app.exec()
