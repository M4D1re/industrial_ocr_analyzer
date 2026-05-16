from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QDockWidget,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

from app.ui.widgets.chart_panel import ChartPanel
from app.ui.widgets.readings_table import ReadingsTable
from app.ui.widgets.session_info_panel import SessionInfoPanel
from app.ui.widgets.statistics_panel import StatisticsPanel


class MainWindow(QMainWindow):
    """
    Main analyzer window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Industrial OCR Analyzer")

        self.resize(1600, 900)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Initializes UI.
        """

        self._create_toolbar()

        self._create_statusbar()

        self._create_central_chart()

        self._create_docks()

    def _create_toolbar(self) -> None:
        """
        Creates toolbar.
        """

        toolbar = QToolBar("Main Toolbar")

        toolbar.setMovable(False)

        open_action = toolbar.addAction("Open Session")

        export_action = toolbar.addAction("Export Excel")

        self.addToolBar(toolbar)

    def _create_statusbar(self) -> None:
        """
        Creates status bar.
        """

        statusbar = QStatusBar()

        statusbar.showMessage("Analyzer ready")

        self.setStatusBar(statusbar)

    def _create_central_chart(self) -> None:
        """
        Creates central chart panel.
        """

        self.chart_panel = ChartPanel()

        self.setCentralWidget(self.chart_panel)

    def _create_docks(self) -> None:
        """
        Creates dock panels.
        """

        self._create_session_info_dock()

        self._create_statistics_dock()

        self._create_readings_dock()

    def _create_session_info_dock(self) -> None:
        """
        Creates session info dock.
        """

        dock = QDockWidget("Session Info", self)

        self.session_info_panel = SessionInfoPanel()

        dock.setWidget(self.session_info_panel)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _create_statistics_dock(self) -> None:
        """
        Creates statistics dock.
        """

        dock = QDockWidget("Statistics", self)

        self.statistics_panel = StatisticsPanel()

        dock.setWidget(self.statistics_panel)

        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def _create_readings_dock(self) -> None:
        """
        Creates readings table dock.
        """

        dock = QDockWidget("Readings", self)

        self.readings_table = ReadingsTable()

        dock.setWidget(self.readings_table)

        self.addDockWidget(Qt.BottomDockWidgetArea, dock)