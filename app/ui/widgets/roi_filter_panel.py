from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ROISelectionPanel(QWidget):
    """
    ROI selection and filtering panel.
    """

    roi_selected = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self.list_widget = QListWidget()

        self.list_widget.currentItemChanged.connect(
            self._on_selection_changed
        )

        layout = QVBoxLayout()

        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def set_readings(self, readings: list[dict]) -> None:
        """
        Loads unique ROI list.
        """

        self.list_widget.clear()

        roi_map = {}

        for reading in readings:
            roi_id = reading.get("roi_id")

            roi_name = reading.get("roi_name")

            if roi_id is None:
                continue

            roi_map[roi_id] = roi_name

        for roi_id, roi_name in sorted(roi_map.items()):
            item = QListWidgetItem(
                f"ROI {roi_id}: {roi_name}"
            )

            item.setData(
                1,
                roi_id,
            )

            self.list_widget.addItem(item)

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

        roi_id = current.data(1)

        self.roi_selected.emit(roi_id)