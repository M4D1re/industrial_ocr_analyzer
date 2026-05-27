from pathlib import Path

import pandas as pd


class ExcelExportService:
    """
    Exports readings and statistics to Excel.
    """

    def export(
        self,
        readings: list[dict],
        output_path: str,
    ) -> None:
        """
        Exports readings to Excel file.
        """

        if not readings:
            raise ValueError("No readings to export")

        output_file = Path(output_path)

        rows = []

        for reading in readings:
            rows.append(
                {
                    "ID": reading.get("id"),
                    "Session ID": reading.get("session_id"),
                    "ROI ID": reading.get("roi_id"),
                    "ROI Name": reading.get("roi_name"),
                    "DB Value": reading.get("value"),
                    "Normalized Value": reading.get("normalized_value"),
                    "Raw Text": reading.get("raw_text"),
                    "Confidence": reading.get("confidence"),
                    "Created At": reading.get("created_at"),
                }
            )

        dataframe = pd.DataFrame(rows)

        values = pd.to_numeric(
            dataframe["Normalized Value"],
            errors="coerce",
        ).dropna()

        statistics = pd.DataFrame(
            [
                {
                    "Metric": "Count",
                    "Value": int(values.count()),
                },
                {
                    "Metric": "Min",
                    "Value": values.min() if not values.empty else None,
                },
                {
                    "Metric": "Max",
                    "Value": values.max() if not values.empty else None,
                },
                {
                    "Metric": "Average",
                    "Value": values.mean() if not values.empty else None,
                },
            ]
        )

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            dataframe.to_excel(
                writer,
                sheet_name="Readings",
                index=False,
            )

            statistics.to_excel(
                writer,
                sheet_name="Statistics",
                index=False,
            )