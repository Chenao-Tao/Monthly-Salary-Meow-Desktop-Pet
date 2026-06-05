# -*- coding: utf-8 -*-
"""月薪喵桌面宠物 v2 - 10 种状态 + 随机 GIF"""

import sys, json, random, os, winreg
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QMenu, QAction,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QMovie, QColor, QFont, QCursor
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

SCRIPT_DIR = Path(__file__).parent
ASSET_DIR = SCRIPT_DIR / "\u6708\u85aa\u55b5\u7d20\u6750"
MUSIC_DIR = SCRIPT_DIR / "\u97f3\u4e50\u7d20\u6750"
CONFIG_FILE = SCRIPT_DIR / "config.json"

DEFAULT_CONFIG = {
    "pet_size": 150,
    "always_on_top": True,
    "start_position": None,
    "move_speed": 2,
    "enable_random_quote": True,
    "quote_interval_seconds": 30,
}

# 状态 -> 文件夹名映射
STATE_DIRS = {
    "idle":    "\u653e\u677e",
    "walk":    "\u8d70\u52a8",
    "work":    "\u4e0a\u73ed",
    "sleep":   "\u7761\u89c9",
    "home":    "\u5728\u5bb6",
    "lazy":    "\u6478\u9c7c",
    "greet":   "\u6253\u62db\u547c",
    "like":    "\u559c\u6b22",
    "angry":   "\u751f\u6c14",
    "mvp":     "MVP\u7ed3\u7b97",
    "quote":   "\u6253\u5de5\u8bed\u5f55",
}

# 状态中文名
STATE_NAMES = {
    "idle":    "\u653e\u677e",
    "walk":    "\u8d70\u52a8",
    "work":    "\u4e0a\u73ed",
    "sleep":   "\u7761\u89c9",
    "home":    "\u5728\u5bb6",
    "lazy":    "\u6478\u9c7c",
    "greet":   "\u6253\u62db\u547c",
    "like":    "\u559c\u6b22",
    "angry":   "\u751f\u6c14",
    "mvp":     "MVP\u7ed3\u7b97",
    "quote":   "\u6253\u5de5\u8bed\u5f55",
}

QUOTES = [
    "\u4eca\u5929\u4e5f\u8981\u52aa\u529b\u8d5a\u732b\u7cae\uff01",
    "\u5de5\u8d44\u8fd8\u6ca1\u5230\u8d26\uff0c\u5148\u6478\u4f1a\u9c7c\u3002",
    "\u8001\u677f\u770b\u4e0d\u89c1\u6211\uff0c\u770b\u4e0d\u89c1\u6211\u3002",
    "\u518d\u575a\u6301\u4e00\u4e0b\uff0c\u5feb\u4e0b\u73ed\u5566\uff01",
    "\u55b5\u55b5\u6b63\u5728\u8ba4\u771f\u4e0a\u73ed\u3002",
    "\u6708\u85aa\u5230\u8d26\u4e4b\u524d\uff0c\u6211\u5148\u7761\u4e00\u4e0b\u3002",
    "\u4e0d\u8981\u7126\u8651\uff0c\u732b\u732b\u966a\u4f60\u3002",
    "\u6478\u9c7c\u662f\u6253\u5de5\u4eba\u7684\u57fa\u672c\u529f\u55b5\uff5e",
    "\u52a0\u6cb9\uff01\u79bb\u53d1\u5de5\u8d44\u53c8\u8fd1\u4e86\u4e00\u5929\uff01",
    "\u8ba4\u771f\u5de5\u4f5c\u7684\u732b\u732b\u6700\u53ef\u7231\u3002",
    "\u4f60\u5f88\u68d2\uff0c\u732b\u732b\u8ba4\u8bc1\uff01",
]
IDLE_QUOTES = [
    "\u4f60\u4eca\u5929\u4e5f\u5f88\u68d2\uff01",
    "\u732b\u732b\u89c9\u5f97\u4f60\u8d85\u5389\u5bb3\uff01",
    "\u4f60\u662f\u6700\u68d2\u7684\u94f2\u5c4e\u5b98\uff01",
    "\u4eca\u5929\u7684\u4f60\u4e5f\u5f88\u597d\u770b\u54e6\uff5e",
    "\u732b\u732b\u4e3a\u4f60\u52a0\u6cb9\uff01\u55b5\uff5e",
    "\u4f60\u771f\u7684\u5f88\u52aa\u529b\u4e86\uff0c\u62b1\u62b1\uff01",
    "\u7d27\u5f20\u7684\u65f6\u5019\u5c31\u6478\u6478\u732b\u732b\u5427\uff5e",
    "\u4f60\u6bd4\u4f60\u60f3\u8c61\u7684\u66f4\u4f18\u79c0\uff01",
    "\u732b\u732b\u5f88\u559c\u6b22\u4f60\u54e6\uff5e",
    "\u4eca\u5929\u4e5f\u662f\u5145\u6ee1\u732b\u732b\u7684\u4e00\u5929\uff01",
    "\u522b\u5fd8\u4e86\u4f11\u606f\uff0c\u732b\u732b\u5173\u5fc3\u4f60\uff5e",
    "\u4f60\u505a\u5f97\u5f88\u597d\uff0c\u732b\u732b\u8ba4\u8bc1\uff01",
    "\u6709\u732b\u732b\u5728\uff0c\u4e0d\u5bb3\u6015\u54e6\uff5e",
    "\u4f60\u662f\u732b\u732b\u6700\u559c\u6b22\u7684\u94f2\u5c4e\u5b98\uff01",
    "\u4eca\u5929\u4e5f\u8981\u5f00\u5fc3\u54e6\uff01",
    "\u732b\u732b\u77e5\u9053\u4f60\u5f88\u8f9b\u82e6\uff0c\u62b1\u62b1\u4f60\uff5e",
    "\u52aa\u529b\u7684\u4f60\u6700\u53ef\u7231\u4e86\uff01",
    "\u4f60\u5c31\u662f\u732b\u732b\u5fc3\u4e2d\u7684 MVP\uff01",
    "\u522b\u7740\u6025\uff0c\u4e00\u5207\u90fd\u4f1a\u597d\u8d77\u6765\u7684\uff5e",
    "\u732b\u732b\u6c38\u8fdc\u7ad9\u5728\u4f60\u8fd9\u8fb9\uff01",
]

CLICK_QUOTES = [
    "\u54ce\u5440\uff0c\u88ab\u53d1\u73b0\u4e86\uff01",
    "\u4e0d\u8981\u6233\u732b\u732b\u5566\uff5e",
    "\u55b5\uff1f\u6709\u4ec0\u4e48\u4e8b\u5417\uff1f",
    "\u563f\u563f\uff0c\u6478\u5230\u732b\u732b\u4e86\uff01",
    "\u518d\u6233\u5c31\u8981\u6536\u8d39\u4e86\u55b5\uff01",
]

# 一次性状态（播完自动恢复）
TRANSIENT_STATES = {"greet", "mvp", "quote", "like"}

def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception:
            pass
    return cfg

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
REG_NAME = "MiaoMiaoPet"

def _get_startup_cmd():
    """获取当前程序的启动命令"""
    # 优先用 bat 文件路径
    bat = SCRIPT_DIR / "\u6708\u85aa\u55b5\u684c\u5ba0.bat"
    if bat.exists():
        return str(bat)
    # 否则用 python + main.py
    return f'"{sys.executable}" "{SCRIPT_DIR / "main.py"}"'

def is_startup_enabled():
    """检查是否已设置开机自启"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, REG_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False

def enable_startup():
    """设置开机自启"""
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, REG_NAME, 0, winreg.REG_SZ, _get_startup_cmd())
    winreg.CloseKey(key)

def disable_startup():
    """取消开机自启"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, REG_NAME)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass


class SpeechBubble(QWidget):

    """半透明圆角气泡"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(220)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Microsoft YaHei", 11))
        self.label.setStyleSheet("""
            QLabel {
                color: #5A4A3A;
                background: rgba(255, 255, 255, 230);
                border: 1.5px solid #E8D5C0;
                border-radius: 12px;
                padding: 8px 12px;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self.label)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.label.setGraphicsEffect(shadow)
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)

    def show_text(self, text, duration=3000):
        self.label.setText(text)
        self.label.adjustSize()
        self.resize(self.label.size())
        self.show()
        self.hide_timer.start(duration)

    def follow(self, pet_pos, pet_w):
        x = pet_pos.x() + (pet_w - self.width()) // 2
        y = pet_pos.y() - self.height() - 5
        self.move(x, max(0, y))

class MVPWindow(QWidget):
    """MVP 结算弹窗 - 居中大尺寸 GIF + 背景音乐"""

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 540)

        # GIF 展示
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, 500, 500)
        self.gif_label.setScaledContents(True)
        self.movie = None

        # 关闭按钮
        from PyQt5.QtWidgets import QPushButton
        self.close_btn = QPushButton("\u2716 \u5173\u95ed", self)
        self.close_btn.setGeometry(200, 505, 100, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,200);
                border: 1px solid #E8D5C0;
                border-radius: 8px;
                font-family: 'Microsoft YaHei';
                font-size: 12px;
                padding: 4px;
            }
            QPushButton:hover { background: rgba(245,230,211,255); }
        """)
        self.close_btn.clicked.connect(self.close_mvp)

        # 音乐播放器
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self._on_media_status)

    def play(self, gif_path, music_path):
        """播放 GIF + 音乐"""
        # 加载 GIF
        self.movie = QMovie(str(gif_path))
        self.movie.setCacheMode(QMovie.CacheAll)
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # 播放音乐
        url = QUrl.fromLocalFile(str(music_path))
        self.player.setMedia(QMediaContent(url))
        self.player.setVolume(80)
        self.player.play()

        # 居中显示
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 500) // 2
        y = (screen.height() - 540) // 2
        self.move(x, y)
        self.show()

    def _on_media_status(self, status):
        """音乐播放结束时自动关闭"""
        if status == QMediaPlayer.EndOfMedia:
            self.close_mvp()

    def close_mvp(self):
        """关闭 MVP 窗口并停止音乐"""
        self.player.stop()
        if self.movie:
            self.movie.stop()
        self.close()

    def closeEvent(self, event):
        self.player.stop()
        if self.movie:
            self.movie.stop()
        event.accept()


class PetWidget(QWidget):

    """月薪喵桌宠主窗口"""

    def __init__(self, config):
        super().__init__()
        self.cfg = config
        self.size = config["pet_size"]
        self.state = "idle"
        self.prev_state = "idle"
        self.is_walk = False
        self.walk_dir = 1
        self.is_dragging = False
        self.drag_pos = QPoint()

        flags = Qt.FramelessWindowHint | Qt.Tool
        if config["always_on_top"]:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.size, self.size)

        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, self.size, self.size)
        self.gif_label.setScaledContents(True)
        self.movie = None

        self.bubble = SpeechBubble()

        # 走动定时器
        self.walk_timer = QTimer(self)
        self.walk_timer.setInterval(50)
        self.walk_timer.timeout.connect(self._do_walk)

        # 随机语录定时器
        self.quote_timer = QTimer(self)
        self.quote_timer.setInterval(config["quote_interval_seconds"] * 1000)
        self.quote_timer.timeout.connect(self._random_quote)
        if config["enable_random_quote"]:
            self.quote_timer.start()

        # 一次性状态恢复定时器
        self.transient_timer = QTimer(self)
        self.transient_timer.setSingleShot(True)
        self.transient_timer.setInterval(5000)
        self.transient_timer.timeout.connect(self._recover_from_transient)

        # 加载所有状态的 GIF 列表
        self.gif_map = {}  # state -> [QMovie, QMovie, ...]
        self._load_all_gifs()
        self.set_state("greet")

    def _load_all_gifs(self):
        """扫描每个状态文件夹，加载所有 GIF"""
        for state, folder_name in STATE_DIRS.items():
            folder = ASSET_DIR / folder_name
            movies = []
            if folder.is_dir():
                for gif_file in sorted(folder.glob("*.gif")):
                    try:
                        movie = QMovie(str(gif_file))
                        movie.setCacheMode(QMovie.CacheAll)
                        if movie.isValid():
                            movies.append(movie)
                    except Exception as e:
                        print(f"[ERR] {gif_file}: {e}")
            if movies:
                self.gif_map[state] = movies
                print(f"[OK] {folder_name} -> {state} ({len(movies)} GIFs)")
            else:
                print(f"[跳过] {folder_name} 无有效GIF")

    def _pick_random_movie(self, state):
        """从状态对应的 GIF 列表中随机选一个"""
        movies = self.gif_map.get(state)
        if not movies:
            return None
        return random.choice(movies)

    def set_state(self, new_state):
        """切换状态，随机选一张对应文件夹的 GIF"""
        if new_state not in self.gif_map:
            new_state = "idle"
        if new_state not in self.gif_map:
            return

        # 记录前一个状态（用于一次性状态恢复）
        if new_state not in TRANSIENT_STATES:
            self.prev_state = new_state

        self.state = new_state
        movie = self._pick_random_movie(new_state)
        if not movie:
            return

        if self.movie:
            self.movie.stop()
        self.movie = movie
        self.movie.jumpToFrame(0)
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # 一次性状态自动恢复
        if new_state in TRANSIENT_STATES:
            self.transient_timer.start()
        else:
            self.transient_timer.stop()

    def _recover_from_transient(self):
        """从一次性状态恢复"""
        if self.state in TRANSIENT_STATES:
            self.set_state(self.prev_state)

    def show_bubble(self, text, duration=3000):
        self.bubble.show_text(text, duration)
        self.bubble.follow(self.pos(), self.size)

    def _random_quote(self):
        if self.state not in TRANSIENT_STATES and self.state != "sleep":
            self.show_bubble(random.choice(IDLE_QUOTES))

    # ── 走动 ──
    def _do_walk(self):
        if not self.is_walk or self.is_dragging:
            return
        screen = QApplication.primaryScreen().availableGeometry()
        nx = self.x() + self.walk_dir * self.cfg["move_speed"]
        if nx < screen.left() + 10:
            self.walk_dir = 1; nx = screen.left() + 10
        if nx > screen.right() - self.size - 10:
            self.walk_dir = -1; nx = screen.right() - self.size - 10
        self.move(nx, self.y())
        self.bubble.follow(self.pos(), self.size)

    # ── 鼠标事件 ──
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.LeftButton:
            screen = QApplication.primaryScreen().availableGeometry()
            new_pos = event.globalPos() - self.drag_pos
            x = max(screen.left(), min(new_pos.x(), screen.right() - self.size + 1))
            y = max(screen.top(), min(new_pos.y(), screen.bottom() - self.size + 1))
            self.move(x, y)
            self.bubble.follow(self.pos(), self.size)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_dragging:
            delta = (event.globalPos() - self.frameGeometry().topLeft() - self.drag_pos).manhattanLength()
            if delta < 6:
                self.prev_state = self.state
                self.set_state("like")
                self.transient_timer.start()
            event.accept()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.bubble.follow(self.pos(), self.size)

    def closeEvent(self, event):
        pos = self.pos()
        self.cfg["start_position"] = [pos.x(), pos.y()]
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        event.accept()

    # ── 右键菜单 ──
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #FFFDF8;
                border: 1px solid #E8D5C0;
                border-radius: 8px;
                padding: 4px;
                font-family: 'Microsoft YaHei';
                font-size: 12px;
            }
            QMenu::item { padding: 6px 20px; border-radius: 4px; }
            QMenu::item:selected { background: #F5E6D3; }
        """)

        # 走动
        walk_act = QAction("\u505c\u6b62\u8d70\u52a8" if self.is_walk else "\u5f00\u59cb\u8d70\u52a8", self)
        walk_act.triggered.connect(self._toggle_walk)
        menu.addAction(walk_act)

        # 打工
        work_act = QAction("\u505c\u6b62\u6253\u5de5" if self.state == "work" else "\u5f00\u59cb\u6253\u5de5", self)
        work_act.triggered.connect(self._toggle_work)
        menu.addAction(work_act)
        menu.addSeparator()

        # 切换表情子菜单
        expr_menu = menu.addMenu("\u5207\u6362\u8868\u60c5")
        expr_items = [
            ("\u653e\u677e(\u5f85\u673a)", "idle"),
            ("\u5728\u5bb6", "home"),
            ("\u6478\u9c7c", "lazy"),
            ("\u7761\u89c9", "sleep"),
            ("\u751f\u6c14", "angry"),
            ("\u559c\u6b22", "like"),
        ]
        for label, st in expr_items:
            act = QAction(label, self)
            act.triggered.connect(lambda checked, s=st: self.set_state(s))
            expr_menu.addAction(act)
        menu.addSeparator()

        # 今日打工语录
        quote_act = QAction("\u4eca\u65e5\u6253\u5de5\u8bed\u5f55", self)
        quote_act.triggered.connect(lambda: (self.set_state("quote"), self.show_bubble(random.choice(QUOTES))))
        menu.addAction(quote_act)

        # MVP 结算
        mvp_act = QAction("MVP\u7ed3\u7b97", self)
        mvp_act.triggered.connect(self._trigger_mvp)
        menu.addAction(mvp_act)
        menu.addSeparator()

        # 调整大小
        size_menu = menu.addMenu("\u8c03\u6574\u5927\u5c0f")
        for sz in (100, 150, 200, 250, 300):
            act = QAction(f"{sz}x{sz}", self)
            act.triggered.connect(lambda checked, s=sz: self.resize_pet(s))
            size_menu.addAction(act)
        menu.addSeparator()

        # \u5f00\u673a\u81ea\u52a8\u542f\u52a8
        startup_act = QAction("\u2714 \u5f00\u673a\u81ea\u52a8\u542f\u52a8" if is_startup_enabled() else "\u5f00\u673a\u81ea\u52a8\u542f\u52a8", self)
        startup_act.triggered.connect(self._toggle_startup)
        menu.addAction(startup_act)
        menu.addSeparator()

        # 退出
        quit_act = QAction("\u9000\u51fa\u7a0b\u5e8f", self)
        quit_act.triggered.connect(QApplication.quit)
        menu.addAction(quit_act)

        menu.exec_(event.globalPos())

    def _toggle_walk(self):
        if self.is_walk:
            self.is_walk = False
            self.walk_timer.stop()
            self.set_state("idle")
            self.show_bubble("\u597d\u7684\uff0c\u732b\u732b\u505c\u4e0b\u6765\u4e86\u3002")
        else:
            self.is_walk = True
            self.walk_dir = random.choice([1, -1])
            self.walk_timer.start()
            self.set_state("walk")
            self.show_bubble("\u732b\u732b\u5f00\u59cb\u5de1\u903b\u5566\uff5e")

    def _trigger_mvp(self):
        """触发 MVP 结算：随机 GIF + 背景音乐"""
        mvp_gif_dir = ASSET_DIR / "MVP\u7ed3\u7b97"
        mvp_music_dir = MUSIC_DIR / "MVP\u7ed3\u7b97"
        # 随机选一张 GIF
        gifs = list(mvp_gif_dir.glob("*.gif"))
        if not gifs:
            self.show_bubble("MVP\u7d20\u6750\u4e0d\u8db3\uff01")
            return
        gif_path = random.choice(gifs)
        # 找音乐文件
        musics = list(mvp_music_dir.glob("*.mp3"))
        if not musics:
            self.show_bubble("\u97f3\u4e50\u7d20\u6750\u4e0d\u8db3\uff01")
            return
        music_path = musics[0]
        # 弹出 MVP 窗口
        self.mvp_window = MVPWindow()
        self.mvp_window.play(gif_path, music_path)

    def _toggle_work(self):
        if self.state == "work":
            self.set_state("idle")
            self.show_bubble("\u4e0b\u73ed\u5566\uff01")
        else:
            self.set_state("work")
            self.show_bubble("\u5f00\u59cb\u8ba4\u771f\u6253\u5de5\uff01")

    def _toggle_startup(self):
        if is_startup_enabled():
            disable_startup()
            self.show_bubble("\u5df2\u5173\u95ed\u5f00\u673a\u81ea\u542f")
        else:
            enable_startup()
            self.show_bubble("\u5df2\u5f00\u542f\u5f00\u673a\u81ea\u542f")

    def resize_pet(self, new_size):
        self.size = new_size
        self.cfg["pet_size"] = new_size
        self.setFixedSize(new_size, new_size)
        self.gif_label.setGeometry(0, 0, new_size, new_size)
        self.show_bubble(f"\u732b\u732b\u53d8{new_size}\u5566\uff01")


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    cfg = load_config()
    pet = PetWidget(cfg)
    screen = app.primaryScreen().availableGeometry()
    if cfg.get("start_position"):
        pet.move(cfg["start_position"][0], cfg["start_position"][1])
    else:
        pet.move(screen.right() - cfg["pet_size"] - 20,
                 screen.bottom() - cfg["pet_size"] - 20)
    pet.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()