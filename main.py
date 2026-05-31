import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QScrollArea, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QPalette

# ==========================================
# 📋 EDIT YOUR TASKS HERE (IN THE CLOUD!)
# ==========================================
# Format for deadlines: "YYYY-MM-DD HH:MM" (24-hour clock)
TASKS_DATA = [
    {
        "client": "Prof. Elias Vance (Digital Media)",
        "task": "Research Essay on AI Content Generation systems",
        "deadline": "2026-06-15 23:59"
    },
    {
        "client": "Dr. Miller (Environmental Science)",
        "task": "Case Study Analysis: Ocean Plastics Distribution",
        "deadline": "2026-06-01 14:00"  # This will trigger the urgent state!
    },
    {
        "client": "Manager Sarah (Internship Project)",
        "task": "Quarterly UI Wireframe Deliverables",
        "deadline": "2026-06-20 09:00"
    }
]

class TaskCard(QFrame):
    def __init__(self, client, task, deadline_str):
        super().__init__()
        self.client = client
        self.task = task
        self.target_dt = QDateTime.fromString(deadline_str, "yyyy-MM-dd hh:mm")
        self.pulse_state = 0
        
        # UI Setup
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.layout = QVBoxLayout(self)
        
        self.client_lbl = QLabel(f"👤 CLIENT: {self.client}")
        self.client_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        self.task_lbl = QLabel(f"📝 Task: {self.task}")
        self.task_lbl.setFont(QFont("Segoe UI", 10))
        self.task_lbl.setWordWrap(True)
        
        self.countdown_lbl = QLabel("Calculating time...")
        self.countdown_lbl.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        self.countdown_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.client_lbl)
        self.layout.addWidget(self.task_lbl)
        self.layout.addWidget(self.countdown_lbl)
        
        # Glow Effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        # Initial Color update
        self.update_timer()

    def update_timer(self):
        now = QDateTime.currentDateTime()
        secs_left = now.secsTo(self.target_dt)
        
        if secs_left <= 0:
            self.countdown_lbl.setText("⚠️ OVERDUE / SUBMIT NOW!")
            self.set_urgent_style(overdue=True)
            return

        # Calculate Breakdown
        days = secs_left // 86400
        hours = (secs_left % 86400) // 3600
        mins = (secs_left % 3600) // 60
        secs = secs_left % 60
        
        countdown_str = f"{days}d {hours:02d}h {mins:02d}m {secs:02d}s"
        self.countdown_lbl.setText(countdown_str)
        
        # Check if less than 3 days (259,200 seconds)
        if secs_left < 259200:
            self.pulse_state = (self.pulse_state + 1) % 2
            self.set_urgent_style(overdue=False)
        else:
            self.set_normal_style()

    def set_normal_style(self):
        # Premium Cyberpunk Cyan style
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(25, 35, 45, 200);
                border: 2px solid rgba(0, 240, 255, 100);
                border-radius: 12px;
                padding: 10px;
            }
            QLabel { color: #E0E0E0; }
        """)
        self.client_lbl.setStyleSheet("color: #00F0FF;")
        self.countdown_lbl.setStyleSheet("color: #00F0FF; background: rgba(0,0,0,50); padding: 5px; border-radius: 5px;")
        self.shadow.setColor(QColor(0, 240, 255, 150))

    def set_urgent_style(self, overdue):
        # Blazing Flame / Heartbeat Flashing Style
        alpha = 255 if self.pulse_state == 1 else 130
        border_color = "rgba(255, 0, 50, 255)" if overdue else f"rgba(255, 60, 0, {alpha})"
        bg_color = "rgba(50, 10, 15, 230)" if overdue else "rgba(45, 15, 10, 220)"
        text_color = "#FF3333" if overdue else "#FF6600"
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 10px;
            }}
            QLabel {{ color: #FFFFFF; }}
        """)
        self.client_lbl.setStyleSheet(f"color: {text_color}; text-transform: uppercase;")
        self.countdown_lbl.setStyleSheet(f"color: #FFFFFF; background: {border_color}; padding: 5px; border-radius: 5px;")
        self.shadow.setColor(QColor(255, 50, 0, alpha))


class TrackerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Make window frameless, transparent, and always stay on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Position right side of the screen
        screen = QApplication.primaryScreen().geometry()
        width = 420
        height = 700
        x = screen.width() - width - 20
        y = (screen.height() - height) // 2
        self.setGeometry(x, y, width, height)
        
        # Main Layout Container (Glassmorphic Window)
        main_layout = QVBoxLayout(self)
        
        window_frame = QFrame()
        window_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 20, 28, 180);
                border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 20px;
            }
        """)
        frame_layout = QVBoxLayout(window_frame)
        
        # Header
        header = QLabel("⚡ CLIENT TASK TRACKER")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #FFFFFF; border: none; padding: 5px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(header)
        
        # Scroll Area for handling multiple tasks smoothly
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: rgba(0,0,0,30);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 240, 255, 100);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 240, 255, 200);
            }
        """)
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setSpacing(15)
        
        # Load Cards
        self.cards = []
        for item in TASKS_DATA:
            card = TaskCard(item["client"], item["task"], item["deadline"])
            self.scroll_layout.addWidget(card)
            self.cards.append(card)
            
        scroll.setWidget(scroll_content)
        frame_layout.addWidget(scroll)
        
        # Footer Note
        footer = QLabel(f"{len(TASKS_DATA)} ACTIVE CLIENT PROJECTS")
        footer.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        footer.setStyleSheet("color: rgba(255,255,255,100); border: none;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(footer)
        
        main_layout.addWidget(window_frame)
        
        # Master Clock Engine (Updates every 1 second)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all_cards)
        self.timer.start(1000)
        
    def update_all_cards(self):
        for card in self.cards:
            card.update_timer()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = TrackerWidget()
    tracker.show()
    sys.exit(app.exec())
