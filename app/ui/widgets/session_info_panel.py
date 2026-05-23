from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SessionInfoPanel(QWidget):
    """
    Displays loaded session metadata.
    """

    def __init__(self) -> None:
        super().__init__()

        self.session_label = QLabel("Session: not loaded")
        self.status_label = QLabel("Status: -")
        self.started_at_label = QLabel("Started at: -")
        self.ended_at_label = QLabel("Ended at: -")
        self.readings_count_label = QLabel("Readings: 0")
        self.exported_at_label = QLabel("Exported at: -")

        layout = QVBoxLayout()

        layout.addWidget(self.session_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.started_at_label)
        layout.addWidget(self.ended_at_label)
        layout.addWidget(self.readings_count_label)
        layout.addWidget(self.exported_at_label)
        layout.addStretch()

        self.setLayout(layout)

    def set_metadata(self, metadata: dict) -> None:
        """
        Displays metadata.
        """

        session = metadata.get("session") or {}

        self.session_label.setText(
            f"Session: {session.get('id', '-')}"
        )

        self.status_label.setText(
            f"Status: {session.get('status', '-')}"
        )

        self.started_at_label.setText(
            f"Started at: {session.get('started_at', '-')}"
        )

        self.ended_at_label.setText(
            f"Ended at: {session.get('ended_at', '-')}"
        )

        self.readings_count_label.setText(
            f"Readings: {metadata.get('readings_count', 0)}"
        )

        self.exported_at_label.setText(
            f"Exported at: {metadata.get('exported_at', '-')}"
        )