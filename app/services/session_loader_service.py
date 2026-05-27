import json
import shutil
import sqlite3
import zipfile
from pathlib import Path

from app.analytics.value_parser import AnalyzerValueParser

from app.utils.paths import DATA_DIR


class SessionLoaderService:
    """
    Loads .session.zip archives exported by Industrial OCR Recorder.
    """

    def __init__(self) -> None:
        self.extract_dir = DATA_DIR / "loaded_session"

    def load_archive(self, archive_path: str) -> tuple[dict, list[dict]]:
        """
        Extracts session archive and returns metadata and readings.
        """

        self._clear_extract_dir()

        self.extract_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(self.extract_dir)

        metadata = self._load_metadata()

        readings = self._load_readings()

        return metadata, readings

    def _clear_extract_dir(self) -> None:
        """
        Removes previously loaded session.
        """

        if self.extract_dir.exists():
            shutil.rmtree(self.extract_dir)

    def _load_metadata(self) -> dict:
        """
        Loads metadata.json.
        """

        metadata_path = self.extract_dir / "metadata.json"

        if not metadata_path.exists():
            raise FileNotFoundError("metadata.json not found in archive")

        return json.loads(
            metadata_path.read_text(encoding="utf-8")
        )

    def _load_readings(self) -> list[dict]:
        """
        Loads readings from session.db.
        """

        database_path = self.extract_dir / "session.db"

        if not database_path.exists():
            raise FileNotFoundError("session.db not found in archive")

        connection = sqlite3.connect(database_path)

        connection.row_factory = sqlite3.Row

        query = """
        SELECT
            readings.id,
            readings.session_id,
            readings.roi_id,
            roi_regions.name AS roi_name,
            readings.value,
            readings.raw_text,
            readings.confidence,
            readings.created_at
        FROM readings
        LEFT JOIN roi_regions ON roi_regions.id = readings.roi_id
        ORDER BY readings.created_at ASC
        """

        rows = connection.execute(query).fetchall()

        connection.close()

        readings = []

        for row in rows:
            reading = dict(row)

            parsed_from_raw = AnalyzerValueParser.parse(
                str(reading.get("raw_text") or "")
            )

            reading["normalized_value"] = parsed_from_raw

            readings.append(reading)

        return readings