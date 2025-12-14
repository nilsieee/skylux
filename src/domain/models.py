from dataclasses import dataclass


@dataclass
class Dome:
    """
    Domeinobject voor onze lichtkoepel.
    Komt overeen met een rij in de tabel domes.
    """
    id: int
    code: str
    location: str


@dataclass
class Intervention:
    """
    Domeinobject voor een interventie.
    Komt overeen met een rij in de tabel interventions.
    """
    id: int
    dome_code: str
    date: str
    kind: str
    note: str
