from datetime import date
from src.data.repositories import list_all_interventions
from src.services.exporter import export_interventions_to_csv
from src.data.db import get_connection
from src.data.repositories import (
    add_dome,
    list_domes,
    add_intervention,
    list_interventions_for_dome,
)


def toon_menu() -> None:
    print("\n=== Koepelbeheer Skylux ===")
    print("1) Koepel toevoegen")
    print("2) Koepels tonen")
    print("3) Interventie toevoegen")
    print("4) Interventies tonen voor koepels")
    print("5) Export interventies naar CSV")
    print("0) Stop")


def vraag_input(prompt: str) -> str:
    return input(prompt).strip()


def run_cli(db_path: str) -> None:
    """
    Hoofdloop van de CLI.
    We maken per actie een connectie naar de DB en voeren een repository-functie uit.
    """
    while True:
        toon_menu()
        keuze = vraag_input("Kies een optie: ")

        if keuze == "0":
            print("Tot ziens")
            break

        elif keuze == "1":
            code = vraag_input("Koepel code (bv KPL-0001): ")
            location = vraag_input("Locatie: ")

            with get_connection(db_path) as conn:
                try:
                    new_id = add_dome(conn, code, location)
                    print(f"Koepel toegevoegd met id {new_id}")
                except Exception as ex:
                    print(f"Kon koepel niet toevoegen: {ex}")

        elif keuze == "2":
            with get_connection(db_path) as conn:
                domes = list_domes(conn)

            if not domes:
                print("Geen koepels gevonden.")
            else:
                print("\nID | CODE | LOCATIE")
                for dome in domes:
                    print(f"{dome.id} | {dome.code} | {dome.location}")

        elif keuze == "3":
            dome_code = vraag_input("Koepel code: ")
            datum = vraag_input("Datum (YYYY-MM-DD): ")
            kind = vraag_input("Soort (install/repair/maintenance): ")
            note = vraag_input("Opmerking (mag leeg): ")

            with get_connection(db_path) as conn:
                try:
                    new_id = add_intervention(conn, dome_code, datum, kind, note)
                    print(f"Interventie toegevoegd met id {new_id}")
                except Exception as ex:
                    print(f"Kon interventie niet toevoegen: {ex}")

        elif keuze == "4":
            dome_code = vraag_input("Koepel code: ")
            with get_connection(db_path) as conn:
                items = list_interventions_for_dome(conn, dome_code)
            if not items:
                print("Geen interventies gevonden of koepel bestaat niet.")
            else:
                print("\nID | DATUM | SOORT | OPMERKING")
                for interventie in items:
                    print(
                        f"{interventie.id} | "
                        f"{interventie.date} | "
                        f"{interventie.kind} | "
                        f"{interventie.note}"
                    )
        elif keuze == "5":
            bestandsnaam = vraag_input("CSV bestandsnaam (enter = default): ")

            if bestandsnaam == "":
                vandaag = date.today().isoformat()
                bestandsnaam = f"reports/interventies_{vandaag}.csv"

            with get_connection(db_path) as conn:
                rows = list_all_interventions(conn)
            export_interventions_to_csv(rows, bestandsnaam)
            print(f"Export klaar -> {bestandsnaam}")
        else:
            print("Ongeldige keuze. Probeer opnieuw.")


