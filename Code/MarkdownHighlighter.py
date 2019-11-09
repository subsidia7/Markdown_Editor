from PyQt5.QtGui import *
from PyQt5.QtCore import QRegExp
import TextHighlighter


class MarkdownHighlighter(TextHighlighter.Highlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        h1_color               = '#6C78C4'
        h2_color               = '#6C78C4'
        h3_color               = '#6C78C4'
        h4_color               = '#268BD2'
        h5_color               = '#268BD2'
        h6_color               = '#268BD2'
        bold_color             = '#DC322F'
        italic_color           = '#CB4B16'
        link_color             = '#4E27A6'
        code_color             = '#008C3F'
        anchor_color           = '#BF6211'
        block_quotes_color     = '#93A1A1'

        # italic
        italic_format = QTextCharFormat()
        italic_format.setForeground(QColor(italic_color))
        italic_format.setFontItalic(True)
        self._add_rule((QRegExp("\*.*\*"), italic_format))

        # bold
        bold_format = QTextCharFormat()
        bold_format.setForeground(QColor(bold_color))
        bold_format.setFontWeight(99)
        self._add_rule((QRegExp("\*\*.*\*\*"), bold_format))

        # h1
        h1_format = QTextCharFormat()
        h1_format.setForeground(QColor(h1_color))
        h1_format.setFontWeight(99)
        h1_format.setFontPointSize(18)
        self._add_rule((QRegExp("^#.*$"), h1_format))

        # h2
        h2_format = QTextCharFormat()
        h2_format.setForeground(QColor(h2_color))
        h2_format.setFontWeight(99)
        h2_format.setFontPointSize(16)
        self._add_rule((QRegExp("^##.*$"), h2_format))

        # h3
        h3_format = QTextCharFormat()
        h3_format.setForeground(QColor(h3_color))
        h3_format.setFontWeight(99)
        h3_format.setFontPointSize(14)
        self._add_rule((QRegExp("^###.*$"), h3_format))

        # h4
        h4_format = QTextCharFormat()
        h4_format.setForeground(QColor(h4_color))
        h4_format.setFontWeight(99)
        h4_format.setFontPointSize(12)
        self._add_rule((QRegExp("^####.*$"), h4_format))

        # h5
        h5_format = QTextCharFormat()
        h5_format.setForeground(QColor(h5_color))
        h5_format.setFontWeight(99)
        h5_format.setFontPointSize(10)
        self._add_rule((QRegExp("^#####.*$"), h5_format))

        # h6
        h6_format = QTextCharFormat()
        h6_format.setForeground(QColor(h6_color))
        h6_format.setFontWeight(99)
        h6_format.setFontPointSize(10)
        self._add_rule((QRegExp("^######.*$"), h6_format))

        # link
        link_format = QTextCharFormat()
        link_format.setForeground(QColor(link_color))
        self._add_rule((QRegExp("<.*>"), link_format))

        # anchor
        anchor_format = QTextCharFormat()
        anchor_format.setForeground(QColor(anchor_color))
        self._add_rule((QRegExp("\[.*\]\(.*\)"), anchor_format))

        #code
        code_format = QTextCharFormat()
        code_format.setForeground(QColor(code_color))
        code_format.setFontPointSize(10)
        code_format.setFontWeight(75)
        self._add_rule((QRegExp("`.*`"), code_format))

        code_format2 = QTextCharFormat()
        code_format2.setForeground(QColor(code_color))
        code_format2.setFontPointSize(10)
        code_format2.setFontWeight(75)
        self._add_rule((QRegExp("\t.*$"), code_format2))

        # block quotes
        block_quotes_format = QTextCharFormat()
        block_quotes_format.setForeground(QColor(block_quotes_color))
        self._add_rule((QRegExp("^> "), block_quotes_format))
