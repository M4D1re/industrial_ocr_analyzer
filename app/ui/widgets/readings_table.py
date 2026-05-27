from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ReadingsTable(QWidget):
    """
    Table with session readings.
    """

    def __init__(self) -> None:
        super().__init__()

        self.table = QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Session ID",
                "ROI ID",
                "ROI Name",
                "DB Value",
                "Normalized Value",
                "Raw Text",
                "Confidence",
                "Created At",
            ]
        )

        layout = QVBoxLayout()

        layout.addWidget(self.table)

        self.setLayout(layout)

    def set_readings(self, readings: list[dict]) -> None:
        """
        Displays readings.
        """

        self.table.setRowCount(0)

        for reading in readings:
            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                reading.get("id"),
                reading.get("session_id"),
                reading.get("roi_id"),
                reading.get("roi_name"),
                reading.get("value"),
                reading.get("normalized_value"),
                reading.get("raw_text"),
                reading.get("confidence"),
                reading.get("created_at"),
            ]

            for column, value in enumerate(values):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

        self.table.resizeColumnsToContents()