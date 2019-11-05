import Constants


class Model:
    def __init__(self):
        self.ACTIVE_TAB = 0
        self.FILE_PATH = Constants.EMPTY_PATH
        self.TABS = [{"path": ""}]

    def get_file_name(self):
        splitted = self.FILE_PATH.split('/')
        return splitted[-1]

    def append_document(self, file_path):
        self.TABS.append({"path": file_path})
        self.ACTIVE_TAB = len(self.TABS) - 1
        self.set_document_path(file_path)

    def set_document_path(self, file_path):
        self.FILE_PATH = file_path
