import Constants


class Controller:
    def __init__(self, model, view):
        self.MODEL = model
        self.VIEW = view
        self.set_triggers()

    def set_triggers(self):
        self.VIEW._new_action.triggered.connect(self.new_file)
        self.VIEW._save_action.triggered.connect(self.save_file)
        self.VIEW._save_AS_action.triggered.connect(self.save_AS_file)
        self.VIEW._markdown_action.triggered.connect(self.markdown_show)
        self.VIEW._all_editors_action.triggered.connect(self.all_edits_show)
        self.VIEW._HTML_action.triggered.connect(self.html_show)

    def new_file(self):
        self.MODEL.append_document("")
        self.VIEW.add_tab(Constants.EMPTY_TITLE)
        self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)

    def open_file(self):
        pass

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

    def export_HTML(self):
        pass

    def add_image(self):
        pass

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
