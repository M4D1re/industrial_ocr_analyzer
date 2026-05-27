from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QDockWidget,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QToolBar,
)

from app.services.excel_export_service import ExcelExportService

from app.ui.widgets.roi_filter_panel import ROISelectionPanel

from app.ui.widgets.date_filter_panel import DateFilterPanel

from app.services.session_loader_service import SessionLoaderService
from app.ui.widgets.chart_panel import ChartPanel
from app.ui.widgets.readings_table import ReadingsTable
from app.ui.widgets.session_info_panel import SessionInfoPanel
from app.ui.widgets.statistics_panel import StatisticsPanel

from app.ui.widgets.roi_filter_panel import ROISelectionPanel

class MainWindow(QMainWindow):
    """
    Main analyzer window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.session_loader = SessionLoaderService()

        self.excel_export_service = ExcelExportService()

        self.current_metadata: dict | None = None

        self.current_readings: list[dict] = []

        self.active_roi_id: int | None = None
        self.active_start_datetime = None
        self.active_end_datetime = None

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

        open_action.triggered.connect(
            self._open_session_archive
        )

        export_action = toolbar.addAction("Export Excel")

        export_action.triggered.connect(
            self._export_excel
        )

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
        self._create_roi_selection_dock()
        self._create_date_filter_dock()
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

    def _open_session_archive(self) -> None:
        """
        Opens .session.zip archive.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open session archive",
            "",
            "Session Archive (*.session.zip *.zip)",
        )

        if not file_path:
            return

        try:
            metadata, readings = self.session_loader.load_archive(
                file_path
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Load session failed",
                str(error),
            )
            return

        self.current_metadata = metadata

        self.current_readings = readings

        self.session_info_panel.set_metadata(metadata)

        self.readings_table.set_readings(readings)

        self.statistics_panel.set_statistics(readings)

        self.chart_panel.set_readings(readings)

        self.roi_selection_panel.set_readings(readings)

        self.date_filter_panel.set_range_from_readings(readings)
        self.active_roi_id = None
        self.active_start_datetime = None
        self.active_end_datetime = None

        self._refresh_views()

        self.statusBar().showMessage(
            f"Loaded session: {len(readings)} readings"
        )

    def _create_roi_selection_dock(self) -> None:
        """
        Creates ROI selection dock.
        """

        dock = QDockWidget("ROI Filter", self)

        self.roi_selection_panel = ROISelectionPanel()

        self.roi_selection_panel.roi_selected.connect(
            self._on_roi_selected
        )

        dock.setWidget(self.roi_selection_panel)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock,
        )

    def _on_roi_selected(
            self,
            roi_id: int,
    ) -> None:
        """
        Applies ROI filter.
        """

        self.active_roi_id = roi_id

        self._refresh_views()

        self.statusBar().showMessage(
            f"ROI filter applied: {roi_id}"
        )

    def _create_roi_selection_dock(self) -> None:
        """
        Creates ROI selection dock.
        """

        dock = QDockWidget("ROI Filter", self)

        self.roi_selection_panel = ROISelectionPanel()

        self.roi_selection_panel.roi_selected.connect(
            self._on_roi_selected
        )

        self.roi_selection_panel.filter_reset_requested.connect(
            self._reset_roi_filter
        )

        dock.setWidget(self.roi_selection_panel)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _on_roi_selected(
            self,
            roi_id: int,
    ) -> None:
        """
        Applies ROI filter.
        """

        filtered = [
            reading
            for reading in self.current_readings
            if reading.get("roi_id") == roi_id
        ]

        self.readings_table.set_readings(filtered)

        self.statistics_panel.set_statistics(
            self.current_readings,
            roi_id,
        )

        self.chart_panel.set_readings(
            self.current_readings,
            roi_id,
        )

        self.statusBar().showMessage(
            f"ROI filter applied: {roi_id}"
        )

    def _reset_roi_filter(self) -> None:
        """
        Resets ROI filter.
        """

        self.active_roi_id = None

        self.roi_selection_panel.clear_selection()

        self._refresh_views()

        self.statusBar().showMessage(
            "ROI filter reset"
        )

    def _export_excel(self) -> None:
        """
        Exports current readings to Excel.
        """

        if not self.current_readings:
            QMessageBox.warning(
                self,
                "No data",
                "Нет загруженных данных для экспорта.",
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Excel",
            "session_analytics.xlsx",
            "Excel Workbook (*.xlsx)",
        )

        if not file_path:
            return

        if not file_path.endswith(".xlsx"):
            file_path = f"{file_path}.xlsx"

        try:
            self.excel_export_service.export(
                readings=self.current_readings,
                output_path=file_path,
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Export failed",
                str(error),
            )
            return

        QMessageBox.information(
            self,
            "Export completed",
            f"Excel-файл сохранён:\n{file_path}",
        )

        self.statusBar().showMessage(
            f"Excel exported: {file_path}"
        )

    def _create_date_filter_dock(self) -> None:
        """
        Creates date filter dock.
        """

        dock = QDockWidget("Date Filter", self)

        self.date_filter_panel = DateFilterPanel()

        self.date_filter_panel.filter_applied.connect(
            self._apply_date_filter
        )

        self.date_filter_panel.filter_reset_requested.connect(
            self._reset_date_filter
        )

        dock.setWidget(self.date_filter_panel)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def _get_filtered_readings(self) -> list[dict]:
        """
        Applies active ROI and datetime filters.
        """

        filtered = self.current_readings

        if self.active_roi_id is not None:
            filtered = [
                reading
                for reading in filtered
                if reading.get("roi_id") == self.active_roi_id
            ]

        if (
                self.active_start_datetime is not None
                and self.active_end_datetime is not None
        ):
            start = self.active_start_datetime.toString(
                "yyyy-MM-dd HH:mm:ss"
            )

            end = self.active_end_datetime.toString(
                "yyyy-MM-dd HH:mm:ss"
            )

            filtered = [
                reading
                for reading in filtered
                if start <= str(reading.get("created_at")) <= end
            ]

        return filtered

    def _refresh_views(self) -> None:
        """
        Refreshes table, chart and statistics using active filters.
        """

        filtered = self._get_filtered_readings()

        self.readings_table.set_readings(filtered)

        self.statistics_panel.set_statistics(filtered)

        self.chart_panel.set_readings(filtered)

        self.statusBar().showMessage(
            f"Displayed readings: {len(filtered)}"
        )

    def _apply_date_filter(
            self,
            start_datetime,
            end_datetime,
    ) -> None:
        """
        Applies datetime filter.
        """

        self.active_start_datetime = start_datetime
        self.active_end_datetime = end_datetime

        self._refresh_views()

        self.statusBar().showMessage(
            "Date filter applied"
        )

    def _reset_date_filter(self) -> None:
        """
        Resets datetime filter.
        """

        self.active_start_datetime = None
        self.active_end_datetime = None

        self._refresh_views()

        self.statusBar().showMessage(
            "Date filter reset"
        )