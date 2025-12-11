import typing as _t

# Mélodies pré-définies pour le buzzer.
# Chaque mélodie est une liste de tuples (note, durée_ms).
# - note : str ou nombre (ex: "C4", "A5", 440) ou "-" / "REST" pour un silence
# - durée_ms : int, durée de la note en millisecondes

MELODIES: _t.Dict[str, _t.List[_t.Tuple[_t.Optional[_t.Any], int]]] = {
    # Exemple de mélodie "alerte" simple
    "alerte": [
        ("C5", 150),
        ("-", 50),
        ("C5", 150),
        ("-", 50),
        ("C5", 300),
    ],
    # Exemple de mélodie "victoire"
    "victoire": [
        ("E5", 150),
        ("G5", 150),
        ("C6", 300),
        ("G5", 150),
        ("C6", 400),
    ],
    # Exemple de mélodie "echec"
    "echec": [
        ("E4", 250),
        ("D4", 250),
        ("C4", 400),
    ],
    # Thèmes inspirés de Mario
    "mario_tuyau": [
        ("E5", 150),
        ("G5", 150),
        ("C6", 150),
        ("E6", 150),
        ("G6", 150),
        ("C7", 300),
    ],
    "mario_victoire": [
        ("G5", 150),
        ("C6", 150),
        ("E6", 150),
        ("G6", 250),
        ("E6", 150),
        ("G6", 400),
    ],
    "mario_mort": [
        ("C5", 300),
        ("-", 50),
        ("G4", 300),
        ("-", 50),
        ("E4", 300),
        ("A4", 300),
        ("B4", 300),
        ("A#4", 300),
        ("A4", 500),
    ],
    # Placeholder pour "marion" à personnaliser
    "marion": [
        ("C5", 200),
        ("D5", 200),
        ("E5", 200),
        ("F5", 200),
    ],
}
