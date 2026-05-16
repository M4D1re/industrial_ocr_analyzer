from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class StatisticsPanel(QWidget):
    """
    Displays calculated statistics.
    """

    def __init__(self) -> None:
        super().__init__()

        self.min_label = QLabel("Min: -")

        self.max_label = QLabel("Max: -")

        self.avg_label = QLabel("Avg: -")

        self.count_label = QLabel("Count: -")

        layout = QVBoxLayout()

        layout.addWidget(self.min_label)

        layout.addWidget(self.max_label)

        layout.addWidget(self.avg_label)

        layout.addWidget(self.count_label)

        layout.addStretch()

        self.setLayout(layout)