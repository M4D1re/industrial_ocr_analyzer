from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDateTimeEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DateFilterPanel(QWidget):
    """
    Date and time range filter panel.
    """

    filter_applied = Signal(object, object)
    filter_reset_requested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.start_input = QDateTimeEdit()
        self.start_input.setCalendarPopup(True)

        self.end_input = QDateTimeEdit()
        self.end_input.setCalendarPopup(True)

        self.apply_button = QPushButton("Apply Date Filter")
        self.reset_button = QPushButton("Reset Date Filter")

        self.apply_button.clicked.connect(self._apply_filter)
        self.reset_button.clicked.connect(
            self.filter_reset_requested.emit
        )

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Start datetime:"))
        layout.addWidget(self.start_input)
        layout.addWidget(QLabel("End datetime:"))
        layout.addWidget(self.end_input)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.reset_button)
        layout.addStretch()

        self.setLayout(layout)

    def set_range_from_readings(
        self,
        readings: list[dict],
    ) -> None:
        """
        Sets default datetime range from loaded readings.
        """

        datetimes = [
            reading.get("created_at")
            for reading in readings
            if reading.get("created_at")
        ]

        if not datetimes:
            return

        self.start_input.setDateTime(
            self.start_input.dateTime().fromString(
                min(datetimes),
                "yyyy-MM-dd HH:mm:ss",
            )
        )

        self.end_input.setDateTime(
            self.end_input.dateTime().fromString(
                max(datetimes),
                "yyyy-MM-dd HH:mm:ss",
            )
        )

    def _apply_filter(self) -> None:
        """
        Emits selected datetime range.
        """

        self.filter_applied.emit(
            self.start_input.dateTime(),
            self.end_input.dateTime(),
        )