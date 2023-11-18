import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
from random import randint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口
        self.setWindowTitle('双实时图形示例')
        self.setGeometry(100, 100, 800, 600)

        # 创建中心控件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 创建两个图形控件
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.layout.addWidget(self.graphWidget1)
        self.layout.addWidget(self.graphWidget2)

        # 图形控件设置
        self.setup_graph(self.graphWidget1, "实时数据 1")
        self.setup_graph(self.graphWidget2, "实时数据 2")

        # 定时器更新数据
        self.timer = QTimer()
        self.timer.setInterval(500)  # 每500毫秒更新一次
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # 初始化数据
        self.x1 = list(range(100))  # 100个数据点
        self.y1 = [0 for _ in range(100)]  # 初始化为0
        self.x2 = list(range(100))  # 100个数据点
        self.y2 = [0 for _ in range(100)]  # 初始化为0

    def setup_graph(self, graph_widget, title):
        graph_widget.setBackground('w')
        graph_widget.setTitle(title, color="b", size="30pt")
        graph_widget.setLabel('left', '值', color='red', size=30)
        graph_widget.setLabel('bottom', '时间', color='red', size=30)
        graph_widget.showGrid(x=True, y=True)

    def update_plot_data(self):
        # 更新第一个图形
        self.x1 = self.x1[1:]
        self.x1.append(self.x1[-1] + 1)
        self.y1 = self.y1[1:]
        self.y1.append(randint(0, 100))
        self.graphWidget1.plot(self.x1, self.y1, pen=pg.mkPen(color=(255, 0, 0), width=5), clear=True)

        # 更新第二个图形
        self.x2 = self.x2[1:]
        self.x2.append(self.x2[-1] + 1)
        self.y2 = self.y2[1:]
        self.y2.append(randint(0, 100))
        self.graphWidget2.plot(self.x2, self.y2, pen=pg.mkPen(color=(0, 255, 0), width=5), clear=True)

# 创建应用实例
app = QApplication(sys.argv)
window = MainWindow()
window.show()

# 启动应用的事件循环
sys.exit(app.exec())
