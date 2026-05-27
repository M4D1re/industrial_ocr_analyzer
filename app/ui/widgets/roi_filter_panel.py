from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ROISelectionPanel(QWidget):
    """
    ROI filter panel.
    """

    roi_selected = Signal(object)
    filter_reset_requested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.list_widget = QListWidget()

        self.reset_button = QPushButton("Show All ROI")

        self.list_widget.currentItemChanged.connect(
            self._on_selection_changed
        )

        self.reset_button.clicked.connect(
            self.filter_reset_requested.emit
        )

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def set_readings(self, readings: list[dict]) -> None:
        """
        Loads unique ROI list.
        """

        self.list_widget.clear()

        roi_map: dict[int, str] = {}

        for reading in readings:
            roi_id = reading.get("roi_id")
            roi_name = reading.get("roi_name")

            if roi_id is None:
                continue

            roi_map[int(roi_id)] = str(roi_name)

        for roi_id, roi_name in sorted(roi_map.items()):
            item = QListWidgetItem(
                f"ROI {roi_id}: {roi_name}"
            )

            item.setData(1, roi_id)

            self.list_widget.addItem(item)

    def clear_selection(self) -> None:
        """
        Clears selected ROI.
        """

        self.list_widget.clearSelection()

    def _on_selection_changed(
        self,
        current,
        previous,
    ) -> None:
        """
        Emits selected ROI id.
        """

        if current is None:
            return

        self.roi_selected.emit(
            current.data(1)
        )