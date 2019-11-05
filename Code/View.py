import Model
import Constants
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QMenu, QFileDialog, QTextEdit, QLabel, QGridLayout, \
    QDesktopWidget, QHBoxLayout, QTabWidget, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtCore import QPoint


class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        _widget = QWidget()
        self.init_menu()
        h_box = QHBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        h_box.addWidget(self.tabs)
        _widget.setLayout(h_box)
        # понадобится если будем делать заезд на браузер ыыы
        # self.prefs = QWidget()
        #
        # formLayout = QFormLayout()
        # self.browserLineEdit = QLineEdit()
        # self.browserLineEdit.setReadOnly(True)
        #
        # self.browserButton = QPushButton("&Select")
        #
        # rowLayout = QHBoxLayout()
        #
        # rowLayout.addWidget(QLabel("Preview browser"))
        # rowLayout.addWidget(self.browserLineEdit)
        # rowLayout.addWidget(self.browserButton)
        #
        # formLayout.addRow(rowLayout)
        #
        # self.prefs.setLayout(formLayout)

        self.setCentralWidget(_widget)
        self.pos_center()
        self.enable()

    def init_menu(self):
        # menu_bar
        _menu_bar = self.menuBar()
        # creating file menu
        _file_menu = _menu_bar.addMenu("Файл")
        self._new_action = QAction("Создать файл", self)
        self._open_action = QAction("Открыть файл", self)
        self._save_action = QAction("Сохранить", self)
        self._save_AS_action = QAction("Сохранить как", self)
        self._export_HTML = QAction("Экспорт в HTML", self)
        _file_menu.addActions([self._new_action, self._open_action, self._save_action, self._save_AS_action,
                               self._export_HTML])
        # creating editing menu
        _editing_menu = _menu_bar.addMenu("Изменить")
        _inner_menu = QMenu("Добавить", self)
        self._add_image_action = QAction("Изображение", self)
        self._add_reference_action = QAction("Ссылку", self)
        _inner_menu.addActions([self._add_image_action, self._add_reference_action])
        _editing_menu.addMenu(_inner_menu)
        # creating view menu
        _view_menu = _menu_bar.addMenu("Просмотр")
        self._markdown_action = QAction("Только редактор markdown", self)
        self._all_editors_action = QAction("Показать markdown + html", self)
        self._HTML_action = QAction("Показать только HTML", self)
        _view_menu.addActions([self._markdown_action, self._all_editors_action, self._HTML_action])

    def pos_center(self):
        q_r = self.frameGeometry()
        central_pos = QDesktopWidget().availableGeometry().center()
        q_r.moveCenter(central_pos)
        self.move(q_r.topLeft())

    def enable(self):
        self.resize(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        #self.showMaximized()
        self.setWindowTitle(Constants.PROGRAM_TITLE)
        self.show()

    def add_tab(self, title):
        tab = QWidget()
        input_edit = TextEditor()
        preview = TextEditor()
        preview.setReadOnly(True)
        self.tabs.addTab(tab, title)
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(input_edit)
        tab_h_box.addWidget(preview)
        tab.setLayout(tab_h_box)

    def get_active_input(self):
        return self.tabs.currentWidget().layout().itemAt(0).widget()# эта херота вернет input_edit которая для маркдауна
        # индекс 0 потому что мы его первым добавляли в лэйаут для таба

    def get_active_preview(self):
        return self.tabs.currentWidget().layout().itemAt(1).widget()# эта херота вернет preview которая для маркдауна
        # индекс 1 потому что мы его вторым добавляли в лэйаут для таба

    def change_active_tab(self, index):
        self.tabs.setCurrentIndex(index)
