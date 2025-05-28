import serial.tools.list_ports
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QTabWidget, QDockWidget
from PySide6.QtCore import QTranslator
import pyqtgraph as pg
from pyqtgraph import exporters

class ConnectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Подключение к COM-порту"))

        layout = QtWidgets.QFormLayout(self)

        # Выбор номера COM-порта
        self.combo_ports = QtWidgets.QComboBox(self)
        self.refresh_ports()
        layout.addRow(self.tr("COM-порт:"), self.combo_ports)

        # Выбор бауд рейта
        self.combo_baudrate = QtWidgets.QComboBox(self)
        self.combo_baudrate.addItems(["9600", "19200", "38400", "57600", "115200"])
        layout.addRow(self.tr("Скорость (baud rate):"), self.combo_baudrate)

        self.connect_button = QtWidgets.QPushButton(self.tr("Подключиться"), self)
        self.connect_button.clicked.connect(self.accept)
        layout.addRow(self.connect_button)

    def refresh_ports(self):
        ''''Обновляет список COM-портов'''
        self.combo_ports.clear()
        for port in serial.tools.list_ports.comports():
            self.combo_ports.addItem(port.device)


class AppUI(QtWidgets.QMainWindow):
    def __init__(self):
        """Создает окно в Windows"""
        super().__init__()
        self.setWindowTitle("MDRN_TRACER")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowIcon(QIcon("logo.png"))
        self.setDockNestingEnabled(True)  # Разрешаем сложные компоновки
        
        # Инициализация настроек
        self.current_language = "ru"  # По умолчанию русский язык
        self.current_theme = "dark"   # По умолчанию темная тема
        self.translator = QTranslator()  # Переводчик для смены языка
        self._apply_theme(self.current_theme)  # Применяем тему по умолчанию

        self._init_ui()
        self.create_menu_bar()
        self.dock_widgets = []

    def _init_ui(self):
        """Создает область с показаниями"""
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
    def create_menu_bar(self):
        """Создает верхнее меню"""
        menubar = self.menuBar()

        # Меню открытия
        connection_menu = menubar.addMenu(self.tr("Подключение"))
        self.connect_action = QAction(self.tr("Подключиться к COM-порту"), self)
        self.connect_action.triggered.connect(self.show_connect_dialog)
        connection_menu.addAction(self.connect_action)

        # Меню данных
        data_menu = menubar.addMenu(self.tr("Данные"))
        self.start_logging_action = QAction(self.tr("Начать запись"), self)
        self.stop_logging_action = QAction(self.tr("Остановить запись"), self)
        data_menu.addAction(self.start_logging_action)
        data_menu.addAction(self.stop_logging_action)

        # Меню графиков
        graph_menu = menubar.addMenu(self.tr("Графики"))

        # Подменю добавления графика
        self.add_graph_action = QAction(self.tr("Добавить график"), self)
        self.add_graph_action.triggered.connect(self.show_add_graph_dialog)
        graph_menu.addAction(self.add_graph_action)
        # Подменю экспорта графиков
        self.export_action = QAction(self.tr("Экспорт графиков"), self)
        self.export_action.triggered.connect(self.export_graphs)
        graph_menu.addAction(self.export_action)


        # Меню настроек
        settings_menu = menubar.addMenu(self.tr("Настройки"))

        # Подменю для выбора языка
        language_menu = settings_menu.addMenu(self.tr("Язык"))
        self.language_actions = {
            "ru": QAction(self.tr("Русский"), self),
            "en": QAction(self.tr("Английский"), self)
        }
        for lang, action in self.language_actions.items():
            action.setCheckable(True)
            action.triggered.connect(lambda checked, lang=lang: self.set_language(lang))
            language_menu.addAction(action)
        self.language_actions[self.current_language].setChecked(True)  # Выбранный язык по умолчанию
        # Подменю для выбора темы
        theme_menu = settings_menu.addMenu(self.tr("Тема"))
        self.theme_actions = {
            "dark": QAction(self.tr("Темная"), self),
            "light": QAction(self.tr("Светлая"), self)
        }
        for theme, action in self.theme_actions.items():
            action.setCheckable(True)
            action.triggered.connect(lambda checked, theme=theme: self.set_theme(theme))
            theme_menu.addAction(action)
        self.theme_actions[self.current_theme].setChecked(True)  # Выбранная тема по умолчанию

    def set_language(self, lang):
        """Устанавливает язык интерфейса"""
        self.current_language = lang
        for lang_code, action in self.language_actions.items():
            action.setChecked(lang_code == lang)

        # Загружаем перевод для выбранного языка
        if lang == "ru":
            self.translator.load("")  # Сбрасываем перевод (русский по умолчанию)
        else:
            self.translator.load(f":/translations/app_{lang}.qm")  # Загружаем перевод

        # Применяем перевод ко всему приложению
        QtWidgets.QApplication.instance().installTranslator(self.translator)
        self.retranslate_ui()

    def retranslate_ui(self):
        """Обновляет тексты интерфейса при смене языка"""
        self.setWindowTitle(self.tr("MDRN_LOGGER"))
        self.main_dock.setWindowTitle(self.tr("Основная область"))

        # Обновляем тексты в меню
        self.menuBar().actions()[0].setText(self.tr("Подключение"))
        self.menuBar().actions()[1].setText(self.tr("Данные"))
        self.menuBar().actions()[2].setText(self.tr("Графики"))
        self.menuBar().actions()[3].setText(self.tr("Настройки"))

        # Обновляем тексты действий
        self.connect_action.setText(self.tr("Подключиться к COM-порту"))
        self.start_logging_action.setText(self.tr("Начать запись"))
        self.stop_logging_action.setText(self.tr("Остановить запись"))
        self.add_graph_action.setText(self.tr("Добавить график"))
        self.export_action.setText(self.tr("Экспорт графиков"))

    def set_theme(self, theme):
        """Устанавливает тему интерфейса"""
        self.current_theme = theme
        for theme_code, action in self.theme_actions.items():
            action.setChecked(theme_code == theme)
        self._apply_theme(theme)

    def _apply_theme(self, theme):
        """Применяет выбранную тему"""
        palette = QtGui.QPalette()
        if theme == "dark":
            # Темная тема
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor(35, 35, 35))
            palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
            palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
        else:
            # Светлая тема
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(240, 240, 240))
            palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(0, 0, 0))
            palette.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0))
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(240, 240, 240))
            palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))
            palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
            palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))

        self.setPalette(palette)

    def show_connect_dialog(self):
        dialog = ConnectDialog(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            port = dialog.combo_ports.currentText()
            baudrate = int(dialog.combo_baudrate.currentText())
            self.parent().connect_to_port(port, baudrate)

    def show_add_graph_dialog(self):
        dialog = AddGraphDialog(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.create_graph(
                dialog.graph_name_input.text(),
                dialog.y_label_input.text(),
                dialog.y_min_input.text(),
                dialog.y_max_input.text()
            )

    def create_graph(self, name, y_label, y_min, y_max):
        # Создаем новый PlotWidget
        plot_widget = pg.PlotWidget()
        plot_widget.setLabel("bottom", self.tr("Время, сек"))
        plot_widget.setLabel("left", y_label)
        plot_widget.showGrid(x=True, y=True)
        
        # Настройка диапазона Y
        try:
            y_min = float(y_min) if y_min else None
            y_max = float(y_max) if y_max else None
            if y_min is not None and y_max is not None:
                plot_widget.setYRange(y_min, y_max)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Некорректные значения оси Y"))

        # Создаем новый док для каждого графика
        new_dock = BlenderStyleDock(name)
        new_dock.add_tab(plot_widget, name)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, new_dock)
        self.dock_widgets.append(new_dock)

    def export_graphs(self):
        for dock in self.dock_widgets:
            for i in range(dock.tab_widget.count()):
                widget = dock.tab_widget.widget(i)
                if isinstance(widget, pg.PlotWidget):
                    exporters.ImageExporter(widget.plotItem).export(f"graph_{id(widget)}.png")