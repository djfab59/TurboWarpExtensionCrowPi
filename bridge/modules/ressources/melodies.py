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
        ("E5", 150), ("G5", 150), ("C6", 150),
        ("E6", 150), ("G6", 150), ("C7", 300),
    ],
    "mario_victoire": [
        ("G5", 150), ("C6", 150), ("E6", 150),
        ("G6", 250), ("E6", 150), ("G6", 400),
    ],
    "mario_mort": [
        ("C5", 300), ("-", 50), ("G4", 300), ("-", 50),
        ("E4", 300), ("A4", 300), ("B4", 300),
        ("A#4", 300), ("A4", 500),
    ],
    "mario_start_level": [
        ("E5", 150), ("-", 50), ("E5", 150), ("-", 50),
        ("E5", 150), ("C5", 150),
        ("E5", 150), ("G5", 300),
        ("G4", 300),
    ],
    "mario_coin": [
        ("B5", 120),
        ("E6", 150),
    ],
    "mario_1up": [
        ("E5", 120), ("G5", 120), ("E6", 120),
        ("C6", 120), ("D6", 120), ("G6", 200),
    ],
    "mario_powerup": [
        ("C5", 120), ("D5", 120), ("E5", 120), ("G5", 120), ("E6", 180),
    ],
    "mario_game_over": [
        ("C5", 300), ("G4", 300), ("E4", 300),
        ("A4", 300), ("B4", 300), ("A#4", 300),
        ("A4", 500),
    ],
    "mario_star": [
        ("C6", 150), ("D6", 150), ("E6", 150), ("G6", 150),
        ("E6", 150), ("G6", 150), ("A6", 150), ("B6", 150),
    ],
    "mario_bowser": [
        ("G4", 200), ("C5", 200), ("F4", 200), ("B4", 200),
        ("G4", 200), ("C5", 200), ("F4", 200), ("B4", 200),
    ],
    # Placeholder pour "marion" à personnaliser
    "marion": [
        ("C5", 200),
        ("D5", 200),
        ("E5", 200),
        ("F5", 200),
    ],
}
