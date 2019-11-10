import Constants
import json

class Model:
    # Active tabs
    def __init__(self):
        self.ACTIVE_TAB = 0
        self.FILE_PATH = Constants.EMPTY_PATH
        self.TABS = []
        self.RECENT_DOCUMENTS = self.get_recent_documents()

    def get_recent_documents(self):
        #result = self.get_file_content(Constants.CONFIG_FILE)
        db = open(Constants.CONFIG_FILE)
        data = json.load(db)
        if "recent_documents" in data and type(data) is not None:
           return data["recent_documents"]
        else:
            return[]

    def get_file_name(self):
        splitted = self.FILE_PATH.split('/')
        return splitted[-1]

    def append_document(self, file_path):
        self.TABS.append({"path": file_path})
        self.ACTIVE_TAB = len(self.TABS) - 1
        self.set_document_path(file_path)

    def set_document_path(self, file_path):
        self.FILE_PATH = file_path

    def save_document_path(self, file_path):
        self.TABS[self.ACTIVE_TAB]["path"] = file_path

    def add_recent_document(self, path):
        #if self.RECENT_DOCUMENTS is None:
        #   self.RECENT_DOCUMENTS = []
        l = len(self.RECENT_DOCUMENTS)
        t = self.RECENT_DOCUMENTS[:l]
        for ix in range(len(t)):
            if t[ix] == path:
                t.pop(ix)
                break
        self.RECENT_DOCUMENTS = []
        self.RECENT_DOCUMENTS.append(str(path))
        self.RECENT_DOCUMENTS.extend(t)
        if len(self.RECENT_DOCUMENTS) > 11:
            self.RECENT_DOCUMENTS.pop()

        result = self.get_file_content(Constants.CONFIG_FILE)
        data = json.loads(result)
        data['recent_documents'] = self.RECENT_DOCUMENTS

        self.write_file_content(Constants.CONFIG_FILE, json.dumps(data))

    def remove_tab(self, index):
        self.TABS.pop(index)

    def write_file_content(self, file_path, content):
        f = open(file_path, 'w')
        f.write(content)
        f.close()

    # Попытка прочитать файл
    def get_file_content(self, filename):
        try:
            # f = open(filename, 'r')
            with open(filename, "r") as f:
                return f.read()
        except Exception as e:
            print ("get_file_content_utf8")
            print (str(e))
            return False

    # Открыт ли документ (есть ли в табах)
    def is_document_present(self, file_path):
        for ix in range(len(self.TABS)):
            if self.TABS[ix]["path"] == file_path:
                return ix
        return -1