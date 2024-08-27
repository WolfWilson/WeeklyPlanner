import sys
import logging
import pandas as pd
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
                             QInputDialog, QHeaderView, QMenu, QMessageBox, QCheckBox, 
                             QSystemTrayIcon, QDialog, QTimeEdit, QPushButton, QComboBox,
                             QGroupBox, QFrame)
from PyQt6.QtGui import QIcon, QColor, QFont, QAction
from PyQt6.QtCore import Qt, QTimer
import pygame

# Configuración del logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class WeeklyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weekly Planner')
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon('Source/calendar.ico'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        # Barra lateral
        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(10, 10, 10, 10)
        self.sidebar.setSpacing(20)

        # Iconos de la barra lateral
        icons = ['home.png', 'tasks.png', 'calendar.png', 'settings.png']
        for icon in icons:
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(f'Source/{icon}').pixmap(32, 32))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sidebar.addWidget(icon_label)

        # Layout principal para la vista semanal
        self.week_layout = QVBoxLayout()
        self.week_layout.setContentsMargins(10, 10, 10, 10)
        self.week_layout.setSpacing(20)

        # Layout de días y fechas
        self.days_layout = QHBoxLayout()
        self.days_layout.setSpacing(10)

        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        current_date = datetime.now()

        for day in days:
            day_column = QVBoxLayout()
            day_column.setSpacing(5)

            # Etiqueta de día
            day_label = QLabel(day)
            day_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            day_column.addWidget(day_label)

            # Etiqueta de fecha
            date_label = QLabel(current_date.strftime("%d de %B de %Y"))
            date_label.setFont(QFont("Arial", 10))
            day_column.addWidget(date_label)

            # Tabla de actividades para cada día
            day_table = QTableWidget(10, 1)  # 10 filas para actividades, 1 columna
            day_table.setHorizontalHeaderLabels([f'{day} Actividades'])
            day_table.verticalHeader().setVisible(False)
            day_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            day_table.setFrameShape(QFrame.Shape.NoFrame)
            day_table.setStyleSheet("""
                QTableWidget {
                    background-color: #f7f7f7;
                    border: 1px solid #ddd;
                }
            """)
            day_column.addWidget(day_table)

            self.days_layout.addLayout(day_column)
            current_date += timedelta(days=1)

        self.week_layout.addLayout(self.days_layout)

        # Sección de listas personalizadas
        self.custom_lists_layout = QHBoxLayout()
        self.custom_lists_layout.setSpacing(10)

        lists = ["Lista Personalizada", "Lista De Compras", "Ideas"]
        for list_name in lists:
            list_box = QGroupBox(list_name)
            list_layout = QVBoxLayout()
            list_box.setLayout(list_layout)

            list_layout.addWidget(QLabel(f"Agregar elementos a {list_name.lower()} aquí..."))

            self.custom_lists_layout.addWidget(list_box)

        self.week_layout.addLayout(self.custom_lists_layout)

        # Agregar barra lateral y layout principal al layout de la ventana
        self.main_layout.addLayout(self.sidebar, 1)
        self.main_layout.addLayout(self.week_layout, 5)

        # Configuración de sonido para notificaciones
        pygame.mixer.init()

        # Configuración para minimizar a la bandeja del sistema
        self.tray_icon = QSystemTrayIcon(QIcon('Source/calendar.ico'), self)
        self.tray_icon.activated.connect(self.tray_icon_clicked)
        self.tray_menu = QMenu(self)
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.exit_app)
        self.tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()

    def closeEvent(self, event):
        self.hide()
        self.tray_icon.showMessage(
            "Weekly Planner",
            "La aplicación sigue ejecutándose en el área de notificaciones.",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
        event.ignore()

    def exit_app(self):
        logging.info('Aplicación cerrada desde el menú de la bandeja del sistema')
        sys.exit(0)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            color: #333333;
        }
        QLabel {
            font-size: 12px;
        }
        QGroupBox {
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)
    
    window = WeeklyPlanner()
    window.showMaximized()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
