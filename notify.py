import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor


class NotificationCircle(QWidget):
    def __init__(self):
        super().__init__()
        # ウィンドウの設定
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # フレームを非表示
            Qt.Tool |                 # タスクバーに表示しない
            Qt.WindowStaysOnTopHint   # 常に最前面
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景を透明に
        self.resize(50, 50)  # ウィンドウサイズ

        # 画面中央に配置
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.width() // 2 - self.width() // 2,
            screen.height() // 2 - self.height() // 2
        )

        # 透明度エフェクトの設定
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        # アニメーションの設定
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(3000)  # 300ms
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.finished.connect(self.on_animation_finished)

        # 表示後0.5秒後にフェードアウト開始
        QTimer.singleShot(500, self.start_fade_out)

    def start_fade_out(self):
        print("Starting fade out...")  # デバッグ用
        self.fade_animation.start()

    def on_animation_finished(self):
        print("Animation finished...")  # デバッグ用
        self.close()
        QTimer.singleShot(0, QApplication.instance().quit)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 赤い円を描画
        painter.setBrush(QColor(255, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(5, 5, 40, 40)


def main():
    app = QApplication(sys.argv)
    circle = NotificationCircle()
    circle.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
