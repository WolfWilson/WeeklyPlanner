import sys
import logging
import pandas as pd
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTableWidget, QTableWidgetItem, QInputDialog, QHeaderView,
                             QMenu, QMessageBox, QCheckBox, QHBoxLayout, QLabel, QSystemTrayIcon, QDialog, QTimeEdit, QPushButton)
from PyQt6.QtGui import QIcon, QColor, QFont, QAction
from PyQt6.QtCore import Qt, QTimer, QTime
from plyer import notification
import pygame

# Configuración del logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Configurar Notificación')
        self.layout = QVBoxLayout(self)
        
        # Selector de tiempo
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat('HH:mm')
        self.time_edit.setTime(QTime.currentTime())
        
        self.layout.addWidget(self.time_edit)
        
        # Botones para confirmar o cancelar
        self.button_box = QHBoxLayout()
        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancelar', self)
        self.cancel_button.clicked.connect(self.reject)
        
        self.button_box.addWidget(self.ok_button)
        self.button_box.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_box)

    def get_selected_time(self):
        return self.time_edit.time().toString('HH:mm')

class WeeklyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Planificador Semanal')
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('Source/calendar.ico'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Crear la tabla de planificación
        self.table = QTableWidget(18, 7)  # 18 filas para horas de 7:00 a 00:00, 7 columnas para días de la semana
        self.table.setHorizontalHeaderLabels(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
        
        # Horas de 7:00 a 00:00
        hours = [f'{7 + i}:00' for i in range(15)] + ['22:00', '23:00', '00:00']
        self.table.setVerticalHeaderLabels(hours)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.cellDoubleClicked.connect(self.add_activity)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)

        self.layout.addWidget(self.table)

        # Timer para revisar y notificar actividades
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_activities)
        self.timer.start(60000)  # Revisa cada minuto

        # Configurar pygame para sonido
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
    
    def add_activity(self, row, column):
        day = self.table.horizontalHeaderItem(column).text()
        time = self.table.verticalHeaderItem(row).text()
        
        text, ok = QInputDialog.getText(self, 'Nueva Actividad', f'Agregar actividad para {day} a las {time}:')
        if ok and text:
            item = QTableWidgetItem(text)
            item.setBackground(QColor("#cce5ff"))
            item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Agregar un checkbox para marcar como completada
            checkbox = QCheckBox()
            checkbox_layout = QHBoxLayout()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addWidget(QLabel(text))
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setSpacing(5)
            
            checkbox_item = QWidget()
            checkbox_item.setLayout(checkbox_layout)
            self.table.setCellWidget(row, column, checkbox_item)

            logging.info(f'Actividad agregada: {text} en {day} a las {time}')
            self.save_to_excel()

    def open_context_menu(self, position):
        menu = QMenu()
        edit_action = QAction('Editar Actividad', self)
        delete_action = QAction('Eliminar Actividad', self)
        notification_action = QMenu('Notificaciones', self)
        priority_action = QMenu('Prioridad', self)

        configure_notification_action = QAction('Configurar', self)
        remove_notification_action = QAction('Eliminar', self)
        
        green_action = QAction('Actividad diaria', self)
        orange_action = QAction('Actividad recreativa', self)
        red_action = QAction('Actividad obligatoria', self)
        blue_action = QAction('Actividad opcional', self)

        green_action.triggered.connect(lambda: self.set_priority_color(position, QColor('green')))
        orange_action.triggered.connect(lambda: self.set_priority_color(position, QColor('orange')))
        red_action.triggered.connect(lambda: self.set_priority_color(position, QColor('red')))
        blue_action.triggered.connect(lambda: self.set_priority_color(position, QColor('lightblue')))

        configure_notification_action.triggered.connect(lambda: self.configure_notification(position))
        remove_notification_action.triggered.connect(lambda: self.remove_notification(position))

        notification_action.addAction(configure_notification_action)
        notification_action.addAction(remove_notification_action)

        priority_action.addAction(green_action)
        priority_action.addAction(orange_action)
        priority_action.addAction(red_action)
        priority_action.addAction(blue_action)

        edit_action.triggered.connect(lambda: self.edit_activity(position))
        delete_action.triggered.connect(lambda: self.delete_activity(position))

        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addMenu(notification_action)
        menu.addMenu(priority_action)

        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def configure_notification(self, position):
        dialog = NotificationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            notification_time = dialog.get_selected_time()
            row = self.table.indexAt(position).row()
            column = self.table.indexAt(position).column()
            widget = self.table.cellWidget(row, column)
            if widget:
                widget.setStyleSheet("background-color: yellow; font-weight: bold; text-align: center;")
                widget.findChild(QLabel).setText(f"{widget.findChild(QLabel).text()} (Notif. {notification_time})")
                logging.info(f'Notificación configurada para fila {row}, columna {column} a las {notification_time}')
                self.save_to_excel()
    
    def remove_notification(self, position):
        row = self.table.indexAt(position).row()
        column = self.table.indexAt(position).column()
        widget = self.table.cellWidget(row, column)
        if widget:
            widget.setStyleSheet("background-color: #cce5ff; font-weight: normal; text-align: left;")
            text = widget.findChild(QLabel).text()
            if "Notif." in text:
                widget.findChild(QLabel).setText(text.split(" (Notif.")[0])
            logging.info(f'Notificación eliminada para fila {row} y columna {column}')
            self.save_to_excel()
    
    def set_priority_color(self, position, color):
        row = self.table.indexAt(position).row()
        column = self.table.indexAt(position).column()
        widget = self.table.cellWidget(row, column)
        
        if widget:
            widget.setStyleSheet(f"background-color: {color.name()}; font-weight: bold; text-align: center;")
            logging.info(f'Color de prioridad establecido en {color.name()} para fila {row} y columna {column}')
            self.save_to_excel()
    
    def edit_activity(self, position):
        row = self.table.indexAt(position).row()
        column = self.table.indexAt(position).column()
        widget = self.table.cellWidget(row, column)
        
        if widget:
            label = widget.findChild(QLabel)
            text, ok = QInputDialog.getText(self, 'Editar Actividad', 'Modificar actividad:', text=label.text())
            if ok and text:
                label.setText(text)
                logging.info(f'Actividad editada: {text} en fila {row} y columna {column}')
                self.save_to_excel()

    def delete_activity(self, position):
        row = self.table.indexAt(position).row()
        column = self.table.indexAt(position).column()
        self.table.removeCellWidget(row, column)
        logging.info(f'Actividad eliminada en fila {row} y columna {column}')
        self.save_to_excel()

    def save_to_excel(self):
        data = []
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                widget = self.table.cellWidget(row, column)
                if widget:
                    text = widget.findChild(QLabel).text()
                    completed = widget.findChild(QCheckBox).isChecked()
                    day = self.table.horizontalHeaderItem(column).text()
                    time = self.table.verticalHeaderItem(row).text()
                    color = widget.palette().color(widget.backgroundRole()).name()
                    data.append([day, time, text, completed, color])

        df = pd.DataFrame(data, columns=['Día', 'Hora', 'Actividad', 'Completada', 'Color'])
        df.to_excel('planificador.xlsx', index=False)
        logging.info('Datos guardados en planificador.xlsx')

    def check_activities(self):
        now = datetime.now().strftime('%H:%M')
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                widget = self.table.cellWidget(row, column)
                if widget:
                    text = widget.findChild(QLabel).text()
                    checkbox = widget.findChild(QCheckBox)
                    if "Notif." in text and not checkbox.isChecked():
                        notification_time = text.split("Notif. ")[1].split(")")[0]
                        if now == notification_time:
                            self.show_popup_notification(text, row, column)
    
    def show_popup_notification(self, text, row, column):
        notification_text = text.split(" (Notif.")[0]
        day = self.table.horizontalHeaderItem(column).text()
        pygame.mixer.music.load('Source/sound.mp3')
        pygame.mixer.music.play()
        QMessageBox.information(self, "Recordatorio de Actividad", f'Tienes una actividad programada: {notification_text} para {day}')
        logging.info(f'Notificación emergente mostrada para actividad: {notification_text} en {day}')
    
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()

    def closeEvent(self, event):
        self.hide()
        self.tray_icon.showMessage(
            "Planificador Semanal",
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
        QTableWidget {
            background-color: #f5f5f5;
        }
        QTableWidgetItem {
            background-color: #e6f7ff;
            border: 1px solid #ddd;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin: 5px;
        }
        QLabel {
            color: #333333;
        }
    """)
    
    window = WeeklyPlanner()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
