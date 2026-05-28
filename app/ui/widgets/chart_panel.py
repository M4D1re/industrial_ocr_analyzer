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
        self.plot_widget.setLabel("left", "Normalized Value")
        self.plot_widget.setLabel("bottom", "Reading Index")
        self.plot_widget.addLegend()

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    def set_readings(
        self,
        readings: list[dict],
    ) -> None:
        """
        Displays readings grouped by ROI.
        """

        self.plot_widget.clear()
        self.plot_widget.addLegend()

        grouped: dict[int, list[float]] = {}

        for reading in readings:
            roi_id = reading.get("roi_id")
            value = reading.get("normalized_value")

            if roi_id is None or value is None:
                continue

            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                continue

            grouped.setdefault(int(roi_id), []).append(numeric_value)

        if not grouped:
            return

        for roi_id, values in sorted(grouped.items()):
            x_values = list(range(len(values)))

            self.plot_widget.plot(
                x_values,
                values,
                pen=pg.mkPen(width=2),
                symbol="o",
                symbolSize=5,
                name=f"ROI {roi_id}",
            )