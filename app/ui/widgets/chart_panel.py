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

    def set_readings(self, readings: list[dict]) -> None:
        """
        Displays readings chart.
        """

        self.plot_widget.clear()

        values = [
            float(reading["value"])
            for reading in readings
            if reading.get("value") is not None
        ]

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