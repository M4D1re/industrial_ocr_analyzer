import sys

from PySide6.QtWidgets import QApplication


class AnalyzerApplication(QApplication):
    """
    Analyzer Qt application.
    """

    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.setApplicationName("Industrial OCR Analyzer")