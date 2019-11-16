from PyQt5.QtGui import QSyntaxHighlighter


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__highlighting_rules__ = []

    def _add_rule(self, rule):
        self.__highlighting_rules__.append(rule)

    def highlightBlock(self, text):
        for expression, text_format in self.__highlighting_rules__:
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, text_format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


