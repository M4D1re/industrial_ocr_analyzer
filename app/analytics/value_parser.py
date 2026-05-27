import re


class AnalyzerValueParser:
    """
    Normalizes readings values for analytics.
    """

    @staticmethod
    def parse(raw_text: str) -> float | None:
        """
        Parses OCR raw text to numeric value.
        """

        if not raw_text:
            return None

        text = raw_text.strip()

        text = text.replace(" ", "")
        text = text.replace(",", ".")

        time_value = AnalyzerValueParser._parse_time_like_value(text)

        if time_value is not None:
            return time_value

        return AnalyzerValueParser._parse_regular_number(text)

    @staticmethod
    def _parse_time_like_value(text: str) -> float | None:
        """
        Parses values like 00:54.71 to seconds.
        """

        match = re.search(
            r"(?P<minutes>\d{1,2})[:;](?P<seconds>\d{1,2})(?:[.](?P<fraction>\d+))?",
            text,
        )

        if match is None:
            return None

        minutes = int(match.group("minutes"))
        seconds = int(match.group("seconds"))

        fraction_raw = match.group("fraction") or "0"

        fraction = float(f"0.{fraction_raw}")

        return minutes * 60 + seconds + fraction

    @staticmethod
    def _parse_regular_number(text: str) -> float | None:
        """
        Parses regular numeric value.
        """

        match = re.search(
            r"-?\d+(?:\.\d+)?",
            text,
        )

        if match is None:
            return None

        try:
            return float(match.group(0))
        except ValueError:
            return None