import Constants
import MarkdownHighlighter
import HtmlHighlighter
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QMenu, QFileDialog, QTextEdit, QDesktopWidget, QHBoxLayout,\
    QTabWidget, QLineEdit, QInputDialog
from PyQt5.QtCore import QSignalMapper


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
        self._export_html = QAction("Экспорт в HTML", self)
        self._recent_menu = QMenu("Недавние файлы", self)
        _file_menu.addActions([self._new_action, self._open_action, self._save_action, self._save_AS_action,
                               self._export_html])
        _file_menu.addMenu(self._recent_menu)
        # creating editing menu
        _editing_menu = _menu_bar.addMenu("Изменить")
        _inner_menu = QMenu("Добавить", self)
        self._add_image_action = QAction("Изображение", self)
        self._add_reference_action = QAction("Ссылку", self)
        _inner_menu.addActions([self._add_image_action, self._add_reference_action])
        _editing_menu.addMenu(_inner_menu)
        # creating view menu
        _view_menu = _menu_bar.addMenu("Просмотр")
        self._markdown_action = QAction("Показать/Скрыть markdown", self)
        self._html_editor_action = QAction("Показать/Скрыть html markup", self)
        self._preview_action = QAction("Показать/Скрыть html превью", self)
        _view_menu.addActions([self._markdown_action, self._html_editor_action, self._preview_action])

        self.mapper = QSignalMapper(self)

    def add_recent_document(self, file_path):
        recentFileAction = QAction(str(file_path), self)
        self.mapper.setMapping(recentFileAction, str(file_path))
        self._recent_menu.addAction(recentFileAction)
        return recentFileAction

    def pos_center(self):
        q_r = self.frameGeometry()
        central_pos = QDesktopWidget().availableGeometry().center()
        q_r.moveCenter(central_pos)
        self.move(q_r.topLeft())

    def enable(self):
        self.resize(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        self.showMaximized()
        self.setWindowTitle(Constants.PROGRAM_TITLE)
        self.show()

    def add_tab(self, title):
        tab = QWidget()
        input_edit = TextEditor()
        MarkdownHighlighter.MarkdownHighlighter(input_edit)
        html_edit = TextEditor()
        HtmlHighlighter.HtmlHighlighter(html_edit)
        html_edit.setReadOnly(True)
        preview = TextEditor()
        preview.setReadOnly(True)
        self.tabs.addTab(tab, title)
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(input_edit)
        tab_h_box.addWidget(html_edit)
        tab_h_box.addWidget(preview)
        tab.setLayout(tab_h_box)

    def remove_tab(self, index):
        self.tabs.removeTab(index)

    def get_active_input(self):
        return self.tabs.currentWidget().layout().itemAt(0).widget()# эта херота вернет input_edit которая для маркдауна
        # индекс 0 потому что мы его первым добавляли в лэйаут для таба

    def get_active_html_edit(self):
        return self.tabs.currentWidget().layout().itemAt(1).widget()# эта херота вернет html_edit которая для html
        # индекс 1 потому что мы его первым добавляли в лэйаут для таба

    def get_active_preview(self):
        return self.tabs.currentWidget().layout().itemAt(2).widget()# эта херота вернет preview которая для preview
        # индекс 2 потому что мы его вторым добавляли в лэйаут для таба

    def change_active_tab(self, index):
        self.tabs.setCurrentIndex(index)

    def get_current_document_content(self):
        input_edit = self.get_active_input()
        content = input_edit.toPlainText()
        return content

    def get_current_document_html(self):
        html_edit = self.get_active_html_edit()
        content = html_edit.toPlainText()
        return content

    def save_file_picker(self, type_file="*.md"):
        fname, _ = QFileDialog.getSaveFileName(self, "File name", "", type_file)
        print("Selected file: " + fname)
        if fname:
            return fname
        else:
            return False

    def select_file(self, type_file="*.md"):
        fname, type = QFileDialog.getOpenFileName(self, 'Select file', "", type_file)
        print("Selected file: " + fname)
        if fname:
            return (fname, type)
        else:
            return False

    def get_input_dialog_text(self):
        text, ok_pressed = QInputDialog.getText(self, "Добавление ссылки", "Введите URL для ссылки:", QLineEdit.Normal, "")
        return str(text)

    def show_input_dialog(self):
        self.input_dialog.show()

    def append_string(self, str):
        inputText = self.get_active_input()
        inputText.insertPlainText(str)

    def set_document(self, document):
        inputEdit = self.get_active_input()
        inputEdit.setText(document)

    def set_html_editor(self, text):
        html_editor = self.get_active_html_edit()
        html_editor.setPlainText(text)

    def set_preview(self, text):
        previewEdit = self.get_active_preview()
        previewEdit.setText(text)
