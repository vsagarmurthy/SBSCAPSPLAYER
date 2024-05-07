import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFileDialog, QDialog, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QFont

class VideoSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Video Folders")

        # Create UI elements
        self.left_folder_label = QLabel("Left Folder:")
        self.left_folder_edit = QLineEdit()
        self.left_folder_button = QPushButton("Browse")
        self.right_folder_label = QLabel("Right Folder:")
        self.right_folder_edit = QLineEdit()
        self.right_folder_button = QPushButton("Browse")
        self.left_caption_label = QLabel("Left Caption:")
        self.left_caption_edit = QLineEdit()
        self.right_caption_label = QLabel("Right Caption:")
        self.right_caption_edit = QLineEdit()
        self.submit_button = QPushButton("Submit")

        # Connect browse button signals
        self.left_folder_button.clicked.connect(self.browse_left_folder)
        self.right_folder_button.clicked.connect(self.browse_right_folder)
        self.submit_button.clicked.connect(self.accept)

        # Layout
        layout = QVBoxLayout()
        left_folder_layout = QHBoxLayout()
        left_folder_layout.addWidget(self.left_folder_label)
        left_folder_layout.addWidget(self.left_folder_edit)
        left_folder_layout.addWidget(self.left_folder_button)
        layout.addLayout(left_folder_layout)
        right_folder_layout = QHBoxLayout()
        right_folder_layout.addWidget(self.right_folder_label)
        right_folder_layout.addWidget(self.right_folder_edit)
        right_folder_layout.addWidget(self.right_folder_button)
        layout.addLayout(right_folder_layout)
        left_caption_layout = QHBoxLayout()
        left_caption_layout.addWidget(self.left_caption_label)
        left_caption_layout.addWidget(self.left_caption_edit)
        layout.addLayout(left_caption_layout)
        right_caption_layout = QHBoxLayout()
        right_caption_layout.addWidget(self.right_caption_label)
        right_caption_layout.addWidget(self.right_caption_edit)
        layout.addLayout(right_caption_layout)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def browse_left_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Left Folder")
        if folder:
            self.left_folder_edit.setText(folder)

    def browse_right_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Right Folder")
        if folder:
            self.right_folder_edit.setText(folder)

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SBS Player sissy.kesug.com")
        self.setWindowState(Qt.WindowMaximized)

        # Create UI elements
        self.left_video_widget = QVideoWidget()
        self.right_video_widget = QVideoWidget()
        self.left_caption_label = QLabel()
        self.right_caption_label = QLabel()

        # Set caption label styles
        font = QFont("Arial", 32, QFont.Bold)
        self.left_caption_label.setFont(font)
        self.right_caption_label.setFont(font)

        # Create media players
        self.left_media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.right_media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Set video widgets
        self.left_media_player.setVideoOutput(self.left_video_widget)

        self.right_media_player.setVideoOutput(self.right_video_widget)

        # Connect media player signals
        self.left_media_player.mediaStatusChanged.connect(self.check_videos_finished)
        self.right_media_player.mediaStatusChanged.connect(self.check_videos_finished)

        # Layout
        main_layout = QVBoxLayout()
        video_layout = QHBoxLayout()
        video_layout.addWidget(self.left_video_widget, stretch=1)
        video_layout.addWidget(self.right_video_widget, stretch=1)
        main_layout.addLayout(video_layout, stretch=1)

        caption_layout = QHBoxLayout()
        left_caption_layout = QHBoxLayout()
        left_caption_layout.addStretch(1)
        left_caption_layout.addWidget(self.left_caption_label)
        left_caption_layout.addStretch(1)
        caption_layout.addLayout(left_caption_layout, stretch=1)

        right_caption_layout = QHBoxLayout()
        right_caption_layout.addStretch(1)
        right_caption_layout.addWidget(self.right_caption_label)
        right_caption_layout.addStretch(1)
        caption_layout.addLayout(right_caption_layout, stretch=1)

        main_layout.addLayout(caption_layout)
        self.setLayout(main_layout)

    def play_videos(self, left_folder, right_folder, left_caption, right_caption):
        self.left_caption_label.setText(left_caption)
        self.right_caption_label.setText(right_caption)

        self.left_videos = [os.path.join(left_folder, f) for f in os.listdir(left_folder) if f.endswith(('.mp4', '.avi', '.mkv'))]
        self.right_videos = [os.path.join(right_folder, f) for f in os.listdir(right_folder) if f.endswith(('.mp4', '.avi', '.mkv'))]
        self.left_media_player.setMuted(True)
        self.right_media_player.setMuted(True)
        self.play_next_videos()

    def play_next_videos(self):
        if self.left_videos and self.right_videos:
            left_video = QUrl.fromLocalFile(random.choice(self.left_videos))
            right_video = QUrl.fromLocalFile(random.choice(self.right_videos))

            self.left_media_player.setMedia(QMediaContent(left_video))
            self.right_media_player.setMedia(QMediaContent(right_video))

            self.left_media_player.play()
            self.right_media_player.play()

    def check_videos_finished(self, status):
        if self.left_media_player.mediaStatus() == QMediaPlayer.EndOfMedia and self.right_media_player.mediaStatus() == QMediaPlayer.EndOfMedia:
            self.play_next_videos()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show video selection dialog
    dialog = VideoSelectionDialog()
    if dialog.exec_() == QDialog.Accepted:
        left_folder = dialog.left_folder_edit.text()
        right_folder = dialog.right_folder_edit.text()
        left_caption = dialog.left_caption_edit.text()
        right_caption = dialog.right_caption_edit.text()

        # Create and show video player
        player = VideoPlayer()
        player.play_videos(left_folder, right_folder, left_caption, right_caption)
        player.show()

    sys.exit(app.exec_())