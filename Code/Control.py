import Constants


class Controller:
    def __init__(self, model, view):
        self.MODEL = model
        self.VIEW = view
        self.set_triggers()

    def set_triggers(self):
        #file action
        self.VIEW._new_action.triggered.connect(self.new_file)
        self.VIEW._open_action.triggered.connect(self.open_file)
        self.VIEW._save_action.triggered.connect(self.save_file)
        self.VIEW._save_AS_action.triggered.connect(self.save_AS_file)

        #web_action
        self.VIEW._markdown_action.triggered.connect(self.markdown_show)
        self.VIEW._all_editors_action.triggered.connect(self.all_edits_show)
        self.VIEW._HTML_action.triggered.connect(self.html_show)

        self.VIEW._add_image_action.triggered.connect(self.add_image)

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
        #file action
        self.VIEW._save_action.setDisabled(value)
        self.VIEW._save_AS_action.setDisabled(value)

        #web_action
        self.VIEW._markdown_action.setDisabled(value)
        self.VIEW._all_editors_action.setDisabled(value)
        self.VIEW._HTML_action.setDisabled(value)

        self.VIEW._add_image_action.setDisabled(value)

    def new_file(self):
        self.MODEL.append_document("")
        self.VIEW.add_tab(Constants.EMPTY_TITLE)
        self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)
        if self.MODEL.ACTIVE_TAB == 0:
            self.dangerous_actions_set_disabled(False)


    def open_file(self):
        file_path = self.VIEW.select_file()
        if file_path != False:
            self.open_file_path(file_path)
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
        pass

    def add_image(self):
        if self.MODEL.TABS:
            file_path = self.VIEW.select_file("*.png")
            if file_path != False:
                str = "![setNamePlease]" + "(" + file_path + ")"
                self.VIEW.append_string(str)

    def add_reference(self):
        pass

    def markdown_show(self):
        markdown = self.VIEW.get_active_input()
        html = self.VIEW.get_active_preview()
        markdown.show()
        html.hide()

    def html_show(self):
        markdown = self.VIEW.get_active_input()
        html = self.VIEW.get_active_preview()
        markdown.hide()
        html.show()

    def all_edits_show(self):
        markdown = self.VIEW.get_active_input()
        html = self.VIEW.get_active_preview()
        markdown.show()
        html.show()

    def open_file_path(self, file_path):
        file_content = self.MODEL.get_file_content_utf8(file_path)

        if file_content is False:
            #self.VIEW.no_file_alert()
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
