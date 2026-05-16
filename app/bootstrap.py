from app.ui.app import AnalyzerApplication
from app.ui.main_window import MainWindow
from app.ui.themes import DARK_THEME
from app.utils.paths import ensure_directories


class Bootstrap:
    """
    Application bootstrapper.
    """

    def __init__(self) -> None:
        ensure_directories()

        self.app = AnalyzerApplication()

        self.app.setStyleSheet(DARK_THEME)

        self.main_window = MainWindow()

    def run(self) -> int:
        """
        Starts application.
        """

        self.main_window.show()

        return self.app.exec()