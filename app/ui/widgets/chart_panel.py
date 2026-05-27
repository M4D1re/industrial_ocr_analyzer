import pyqtgraph as pg
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QVBoxLayout, QWidget


class ChartPanel(QWidget):
    """
    Central chart panel.
    """

    def __init__(self) -> None:
        super().__init__()

        self.plot_widget = pg.PlotWidget()

        font = QFont()
        font.setPointSize(10)

        self.plot_widget.getAxis("left").setTickFont(font)
        self.plot_widget.getAxis("bottom").setTickFont(font)

        self.plot_widget.setBackground("#20242b")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel("left", "Value")
        self.plot_widget.setLabel("bottom", "Reading index")

        layout = QVBoxLayout()

        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    def set_readings(
            self,
            readings: list[dict],
            roi_id: int | None = None,
    ) -> None:
        """
        Displays readings chart.
        """

        self.plot_widget.clear()

        filtered = readings

        if roi_id is not None:
            filtered = [
                reading
                for reading in readings
                if reading.get("roi_id") == roi_id
            ]

        values = []

        for reading in filtered:
            value = reading.get("normalized_value")

            if value is None:
                continue

            try:
                values.append(float(value))
            except Exception:
                continue

        if not values:
            return

        x_values = list(range(len(values)))

        self.plot_widget.plot(
            x_values,
            values,
            pen=pg.mkPen(width=2),
            symbol="o",
            symbolSize=5,
        )