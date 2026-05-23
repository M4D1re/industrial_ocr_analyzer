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

    def set_statistics(self, readings: list[dict]) -> None:
        """
        Calculates and displays basic statistics.
        """

        values = [
            float(reading["value"])
            for reading in readings
            if reading.get("value") is not None
        ]

        if not values:
            self.min_label.setText("Min: -")
            self.max_label.setText("Max: -")
            self.avg_label.setText("Avg: -")
            self.count_label.setText("Count: 0")
            return

        self.min_label.setText(f"Min: {min(values):.2f}")
        self.max_label.setText(f"Max: {max(values):.2f}")
        self.avg_label.setText(f"Avg: {sum(values) / len(values):.2f}")
        self.count_label.setText(f"Count: {len(values)}")