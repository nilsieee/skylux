import csv
from pathlib import Path
from typing import Iterable, Tuple


def export_interventions_to_csv(rows: Iterable[Tuple], csv_path: str) -> None:
    """
    schrijven naar CSV bestand
    Verwacht rijen in formaat: (date, dome_code, location, kind, note)
    """
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["date", "dome_code", "location", "kind", "note"])
        writer.writerows(rows)
