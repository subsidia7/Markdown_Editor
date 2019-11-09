import Constants
import markdown

class Controller:
    def __init__(self, model, view):
        self.MODEL = model
        self.VIEW = view
        self.set_triggers()
        self.dangerous_actions_set_disabled(True)

    def set_triggers(self):
        # file actions
        self.VIEW._new_action.triggered.connect(self.new_file)
        self.VIEW._open_action.triggered.connect(self.open_file)
        self.VIEW._save_action.triggered.connect(self.save_file)
        self.VIEW._save_AS_action.triggered.connect(self.save_AS_file)
        self.VIEW._export_html.triggered.connect(self.export_HTML)
        # visual_actions
        self.VIEW._markdown_action.triggered.connect(self.markdown_show_hide)
        self.VIEW._html_editor_action.triggered.connect(self.html_edit_show_hide)
        self.VIEW._preview_action.triggered.connect(self.preview_show_hide)

        # insert actions
        self.VIEW._add_image_action.triggered.connect(self.add_image)
        self.VIEW._add_reference_action.triggered.connect(self.add_reference)

        # ссылка на обработчик переключения вкладки
        self.VIEW.tabs.currentChanged.connect(self.tabChangedSlot)
        # ссылка на обработчик закрытия вкладки
        self.VIEW.tabs.tabCloseRequested.connect(self.tabCloseRequestedSlot)
        self.dangerous_actions_set_disabled(True)

    def tabCloseRequestedSlot(self, argTabIndex):
        self.MODEL.remove_tab(argTabIndex)
        self.VIEW.remove_tab(argTabIndex)
        if len(self.MODEL.TABS) == 0:
            self.dangerous_actions_set_disabled(True)

    def tabChangedSlot(self, argTabIndex):
        self.MODEL.ACTIVE_TAB = argTabIndex

    def dangerous_actions_set_disabled(self, value):
        # file actions
        self.VIEW._save_action.setDisabled(value)
        self.VIEW._save_AS_action.setDisabled(value)
        self.VIEW._export_html.setDisabled(value)

        # view actions
        self.VIEW._markdown_action.setDisabled(value)
        self.VIEW._html_editor_action.setDisabled(value)
        self.VIEW._preview_action.setDisabled(value)

        # insert actions
        self.VIEW._add_image_action.setDisabled(value)
        self.VIEW._add_reference_action.setDisabled(value)

    def new_file(self):
        self.MODEL.append_document("")
        self.VIEW.add_tab(Constants.EMPTY_TITLE)
        self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)
        if self.MODEL.ACTIVE_TAB == 0:
            self.dangerous_actions_set_disabled(False)
        # setting trigger to Text Editor
        inputEdit = self.VIEW.get_active_input()
        inputEdit.textChanged.connect(self.change_html_preview)

    def open_file(self):
        file_path = self.VIEW.select_file()
        if file_path != False:
            self.open_file_path(file_path)
            inputEdit = self.VIEW.get_active_input()
            inputEdit.textChanged.connect(self.change_html_edit)
            inputEdit.textChanged.connect(self.change_preview)
            if self.MODEL.ACTIVE_TAB == 0:
                self.dangerous_actions_set_disabled(False)

    def save_file(self):
        if self.MODEL.FILE_PATH == Constants.EMPTY_PATH:
            self.save_AS_file()
        else:
            content = self.VIEW.get_current_document_content()
            self.MODEL.write_file_content(self.MODEL.FILE_PATH, content)

    def save_AS_file(self):
        content = self.VIEW.get_current_document_content()
        file_path = self.VIEW.save_file_picker()
        if file_path != False:
            self.MODEL.FILE_PATH = file_path
            self.MODEL.save_document_path(file_path)
            self.MODEL.write_file_content(self.MODEL.FILE_PATH, content)
            self.MODEL.add_recent_document(file_path)
            self.VIEW.tabs.setTabText(self.MODEL.ACTIVE_TAB, self.MODEL.get_file_name())

    def export_HTML(self):
        content = self.VIEW.get_current_document_html()
        file_path = self.VIEW.save_file_picker("*.html")
        if file_path != False:
            content = Constants.BEFORE_BODY_CONTENT + content + Constants.AFTER_BODY_CONTENT
            self.MODEL.write_file_content(file_path, content)

    def add_image(self):
        file_path = self.VIEW.select_file("*.jpg")
        if file_path != False:
            str = "![setNamePlease]" + "(" + file_path + ")\n"
            self.VIEW.append_string(str)

    def add_reference(self):
        url = self.VIEW.get_input_dialog_text()
        if url == "":
            return
        str = "[setNamePlease]" + "(" + url + ")\n"
        self.VIEW.append_string(str)

    def markdown_show_hide(self):
        markdown = self.VIEW.get_active_input()
        self.show_hide_widget(markdown)

    def html_edit_show_hide(self):
        html_edit = self.VIEW.get_active_html_edit()
        self.show_hide_widget(html_edit)

    def preview_show_hide(self):
        preview = self.VIEW.get_active_preview()
        self.show_hide_widget(preview)

    def show_hide_widget(self, widget):
        if widget.isHidden():
            widget.show()
        else:
            widget.hide()

    def open_file_path(self, file_path):
        file_content = self.MODEL.get_file_content_utf8(file_path)
        if file_content is False:
            return False
        doc_ix = self.MODEL.is_document_present(file_path)
        if doc_ix != -1:
            self.MODEL.ACTIVE_TAB = doc_ix
            self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)
        else:
            self.MODEL.append_document(file_path)
            self.VIEW.add_tab(self.MODEL.get_file_name())
            self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)
            self.VIEW.set_document(file_content)

    def change_html_preview(self):
        plainText = self.VIEW.get_active_input().toPlainText()
        html = markdown.markdown(plainText)
        self.VIEW.set_html_editor(html)
        self.VIEW.set_preview(html)