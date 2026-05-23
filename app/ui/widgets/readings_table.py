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

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Session ID",
                "ROI ID",
                "ROI Name",
                "Value",
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

            self.table.setItem(row, 0, QTableWidgetItem(str(reading.get("id"))))
            self.table.setItem(row, 1, QTableWidgetItem(str(reading.get("session_id"))))
            self.table.setItem(row, 2, QTableWidgetItem(str(reading.get("roi_id"))))
            self.table.setItem(row, 3, QTableWidgetItem(str(reading.get("roi_name"))))
            self.table.setItem(row, 4, QTableWidgetItem(str(reading.get("value"))))
            self.table.setItem(row, 5, QTableWidgetItem(str(reading.get("confidence"))))
            self.table.setItem(row, 6, QTableWidgetItem(str(reading.get("created_at"))))

        self.table.resizeColumnsToContents()