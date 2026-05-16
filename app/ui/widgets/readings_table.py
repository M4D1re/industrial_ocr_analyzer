from PySide6.QtWidgets import (
    QTableWidget,
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

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "ROI ID",
                "Value",
                "Raw Text",
                "Confidence",
                "Created At",
            ]
        )

        layout = QVBoxLayout()

        layout.addWidget(self.table)

        self.setLayout(layout)