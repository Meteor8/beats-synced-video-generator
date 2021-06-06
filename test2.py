from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
from mygui import Ui_MainWindow
from scipy.signal import detrend
from pydub import AudioSegment

import matplotlib.pyplot as plt
import numpy as np
import struct
import wave
import os
import sys
import time

chunk = 1024

# 将该路径文件从mp3转为wav
def change_format(path):
    new_path = path.replace('mp3', 'wav')
    # 将mp3文件转换成wav
    sound = AudioSegment.from_mp3(path)
    sound.export(new_path, format="wav")


# FigureCanvas 对象
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.figure(figsize=(width, height), dpi=dpi, facecolor='#f0f0f0')       # facecolor 背景色
        self.ax = fig.gca(projection='polar')
        self.ax.set_axis_off()
        self.ln, = self.ax.plot([], [])
        FigureCanvas.__init__(self, fig)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.initialize()

    '''初始化'''
    def initialize(self):
        self.setWindowTitle("音乐播放器^_^")
        self.setWindowIcon(QIcon('icon/音乐.png'))
        self.fileName = ""
        self.cur_song = ''
        self.is_pause = True
        self.y_temp = np.zeros(chunk)

        self.playlist = QMediaPlaylist()  # 播放列表
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)  # 列表循环
        self.player = QMediaPlayer(self)
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(50.0)

        # 按键
        self.btn_openFile.clicked.connect(lambda: self.btn_openFile_click())
        self.btn_start.clicked.connect(lambda: self.btn_start_click())

        # 进度条
        self.slider_time.sliderMoved[int].connect(lambda: self.player.setPosition(self.slider_time.value()))

        # 计时器:控制进度条和进度时间
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.player_timer)

        # 音乐可视化
        self.visualization()

    # 坐标初始化
    def init_draw(self):
        self.canvas.ax.set_ylim(-0.1, 0.1)
        self.canvas.ln.set_data(np.linspace(0, 2 * np.pi, chunk), np.zeros(chunk))


        return self.canvas.ln,

    # 坐标更新
    def update_line(self, frame):
        if self.is_pause is False:
            data = self.wf.readframes(chunk)
            data_int = struct.unpack(str(chunk * 4) + 'B', data)
            y_detrend = detrend(data_int)
            yft = np.abs(np.fft.fft(y_detrend))
            y_vals = yft[:chunk] / (chunk * chunk * 4)
            ind = np.where(y_vals > (np.max(y_vals) + np.min(y_vals)) / 2)
            y_vals[ind[0]] *= 3
            self.y_temp = y_vals
        else:
            y_vals = self.y_temp       # 当暂停时，保存的是上一次的值

        self.canvas.ln.set_ydata(y_vals)
        return self.canvas.ln,

    # 音乐可视化
    def visualization(self):
        self.canvas = MyMplCanvas(self.container, width=6, height=6, dpi=100)
        self.container.addWidget(self.canvas)  # 6
        self.ani = FuncAnimation(self.canvas.figure, self.update_line, init_func=self.init_draw, interval=32, blit=True)

    # 设置进度条和播放时间
    def player_timer(self):
        self.slider_time.setMinimum(0)
        self.slider_time.setMaximum(self.player.duration())
        self.slider_time.setValue(self.slider_time.value() + 1000)

        self.lab_time.setText(time.strftime('%M:%S', time.localtime(self.player.position() / 1000)))
        self.lab_duration.setText(time.strftime('%M:%S', time.localtime(self.player.duration() / 1000)))

        # 进度条满了之后回零
        if self.player.duration() == self.slider_time.value():
            self.slider_time.setValue(0)

    # 打开音乐文件，并添加至playlist
    def btn_openFile_click(self):
        self.playlist.clear()     # 读取歌曲前，清空playlist
        self.fileName, filetype = QFileDialog.getOpenFileName(self, '选择文件', '', '音频文件 (*.mp3; *.wav)')
        if len(self.fileName) == 0:
            print("取消选择")
            return
        else:
            print('当前歌曲路径：' + self.fileName)
            self.cur_song = os.path.basename(self.fileName)
            self.lab_name.setText(self.cur_song)

            # 如果是mp3格式，则将mp3转换wav，保存到同一目录下
            if self.cur_song[-3:] == 'mp3':
                change_format(self.fileName)
                self.fileName = self.fileName.replace('mp3', 'wav')
                print('new '+ self.fileName)

            # 将音频文件添加到playlist
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))

            # 可视化部分wave
            self.wf = wave.open(self.fileName)

        # 正在播放音乐时，中断播放
        if self.is_pause is False:
            self.player.pause()
            self.btn_start.setText('播放')

    def btn_start_click(self):

        if self.is_pause:
            self.is_pause = False
            self.player.play()
            self.btn_start.setText('暂停')
            print('当前播放歌曲： ' + self.cur_song)
        else:
            self.is_pause = True
            self.player.pause()
            self.btn_start.setText('播放')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
