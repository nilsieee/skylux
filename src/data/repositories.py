import sqlite3
from typing import Optional, List, Tuple
from src.domain.models import Dome, Intervention



# DOME (KOEPEL) FUNCTIES

def add_dome(conn: sqlite3.Connection, code: str, location: str) -> int:
    """
    Voegt een nieuwe koepel toe aan de database.
    'conn' = databaseverbinding (komt van db.py)
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO domes (code, location) VALUES (?, ?);",
        (code, location),
    )
    conn.commit()
    return cur.lastrowid


def list_domes(conn: sqlite3.Connection) -> List[Dome]:
    """
    Geeft een lijst van alle koepels terug.
    Elke rij: (id, code, locatie)
    """
    cur = conn.cursor()
    cur.execute("SELECT id, code, location FROM domes ORDER BY code;")
    rows = cur.fetchall()
    return [Dome(id=row[0], code=row[1], location=row[2]) for row in rows]


def get_dome_id_by_code(conn: sqlite3.Connection, code: str) -> Optional[int]:
    """
    Zoekt het ID van een koepel op basis van de code.
    Nodig omdat interventions met ID werken.
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM domes WHERE code = ?;", (code,))
    row = cur.fetchone()

    if row is None:
        return None
    return row[0]


# INTERVENTIE FUNCTIES

def add_intervention(
    conn: sqlite3.Connection,
    dome_code: str,
    datum: str,
    kind: str,
    note: str = "",
) -> int:
    """
    Voegt een interventie toe voor een koepel.
    De koepel wordt eerst opgezocht via de code.
    """
    dome_id = get_dome_id_by_code(conn, dome_code)

    if dome_id is None:
        raise ValueError("Koepel bestaat niet")

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO interventions (dome_id, date, kind, note)
        VALUES (?, ?, ?, ?);
        """,
        (dome_id, datum, kind, note),
    )
    conn.commit()
    return cur.lastrowid


def list_interventions_for_dome(
    conn: sqlite3.Connection, dome_code: str
) -> List[Tuple[int, str, str, str]]:
    """
    Haalt alle interventies op voor één koepel.
    """
    dome_id = get_dome_id_by_code(conn, dome_code)

    if dome_id is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, date, kind, COALESCE(note, '')
        FROM interventions
        WHERE dome_id = ?
        ORDER BY date DESC;
        """,
        (dome_id,),
    )
    rows = cur.fetchall()
    return [
        Intervention(
            id=row[0],
            dome_code=dome_code,
            date=row[1],
            kind=row[2],
            note=row[3],
        )
        for row in rows
]


def list_all_interventions(conn: sqlite3.Connection):
    """
    Haalt alle interventies op met dome code + locatie.
    Resultaat per rij: (date, dome_code, location, kind, note)
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT i.date, d.code, d.location, i.kind, COALESCE(i.note, '')
        FROM interventions i
        JOIN domes d ON d.id = i.dome_id
        ORDER BY i.date DESC, d.code ASC;
        """
    )
    return cur.fetchall()

def delete_dome_by_code(conn: sqlite3.Connection, code: str) -> bool:
    """
    Verwijdert een koepel op basis van de code.
    Verwijdert ook alle interventies die bij die koepel horen.
    """
    dome_id = get_dome_id_by_code(conn, code)
    if dome_id is None:
        return False

    cur = conn.cursor()

    # eerst interventies weg (anders faalt delete op domes als er FK-relaties zijn)
    cur.execute("DELETE FROM interventions WHERE dome_id = ?;", (dome_id,))
    cur.execute("DELETE FROM domes WHERE id = ?;", (dome_id,))

    conn.commit()
    return True

