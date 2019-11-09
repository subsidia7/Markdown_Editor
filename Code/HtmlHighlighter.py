import TextHighlighter
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QRegExp


class HtmlHighlighter(TextHighlighter.Highlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        tags_color = '#DC322F'
        tags_format = QTextCharFormat()
        tags_format.setForeground(QColor(tags_color))
        tags_format.setFontWeight(99)
        self._add_rule((QRegExp("<[^<>]+>"), tags_format))
