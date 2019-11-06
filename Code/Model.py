import Constants


class Model:
    # Active tabs
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

    # Попытка прочитать файл
    def get_file_content_utf8(self, filename):
        try:
            # f = open(filename, 'r')
            with open(filename, "r") as f:
                return f.read()
        except:
            # print ("get_file_content_utf8")
            # print (str(e))
            return False

    # Открыт ли документ (есть ли в табах)
    def is_document_present(self, file_path):
        for ix in range(len(self.TABS)):
            if self.TABS[ix]["path"] == file_path:
                return ix
        return -1
