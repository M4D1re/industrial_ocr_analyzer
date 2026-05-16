from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SessionInfoPanel(QWidget):
    """
    Displays loaded session metadata.
    """

    def __init__(self) -> None:
        super().__init__()

        self.session_label = QLabel("Session: not loaded")

        self.readings_count_label = QLabel("Readings: 0")

        self.exported_at_label = QLabel("Exported at: -")

        layout = QVBoxLayout()

        layout.addWidget(self.session_label)

        layout.addWidget(self.readings_count_label)

        layout.addWidget(self.exported_at_label)

        layout.addStretch()

        self.setLayout(layout)