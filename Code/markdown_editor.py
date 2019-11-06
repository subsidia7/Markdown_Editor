import sys
import Model
import View
import Control
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    model = Model.Model()
    view = View.View()
    controller = Control.Controller(model, view)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
