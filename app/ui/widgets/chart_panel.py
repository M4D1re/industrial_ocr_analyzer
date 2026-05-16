import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class ChartPanel(QWidget):
    """
    Central chart panel.
    """

    def __init__(self) -> None:
        super().__init__()

        self.plot_widget = pg.PlotWidget()

        self.plot_widget.setBackground("#20242b")

        self.plot_widget.showGrid(x=True, y=True)

        self.plot_widget.setLabel("left", "Value")

        self.plot_widget.setLabel("bottom", "Reading index")

        layout = QVBoxLayout()

        layout.addWidget(self.plot_widget)

        self.setLayout(layout)