import Constants


class Controller:
    def __init__(self, model, view):
        self.MODEL = model
        self.VIEW = view
        self.set_triggers()

    def set_triggers(self):
        #fileWorking

        self.VIEW._new_action.triggered.connect(self.new_file)
        self.VIEW._open_action.triggered.connect(self.open_file)


        self.VIEW._markdown_action.triggered.connect(self.markdown_show)
        self.VIEW._all_editors_action.triggered.connect(self.all_edits_show)
        self.VIEW._HTML_action.triggered.connect(self.html_show)


    def new_file(self):
        self.MODEL.append_document("")
        self.VIEW.add_tab(Constants.EMPTY_TITLE)
        self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)

    def open_file(self):
        file_path = self.VIEW.select_file()
        if file_path != False:
            self.open_file_path(file_path)

    def save_file(self):
        pass

    def save_AS_file(self):
        pass

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

            self.VIEW.add_tab(self.MODEL.get_file_name(file_path))
            self.VIEW.change_active_tab(self.MODEL.ACTIVE_TAB)
            self.VIEW.set_document(file_content)