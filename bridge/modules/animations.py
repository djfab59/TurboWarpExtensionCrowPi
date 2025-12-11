import typing as _t

# Animations pré-définies pour la matrice 8x8.
# Chaque animation est une liste de "frames".
# Une frame est un dict :
#   - "pixels": liste d'indices (0-63) à allumer
#   - "color": tuple (r, g, b)
#   - "duration": durée en millisecondes

ANIMATIONS: _t.Dict[str, _t.List[_t.Dict[str, _t.Any]]] = {
    # Smiley simple vert
    "smiley": [
        {
            "pixels": [
                10, 13,         # yeux
                34, 35, 36, 37  # bouche
            ],
            "color": (0, 255, 0),
            "duration": 800,
        }
    ],
    # Smiley triste rouge
    "sad": [
        {
            "pixels": [
                10, 13,         # yeux
                26, 27, 28, 29  # bouche inversée
            ],
            "color": (255, 0, 0),
            "duration": 800,
        }
    ],
    # Cœur rouge
    "heart": [
        {
            "pixels": [
                9, 10, 13, 14,
                17, 18, 19, 20,
                24, 25, 26, 27,
                32, 33, 34,
                40, 41,
                48,
            ],
            "color": (255, 0, 0),
            "duration": 800,
        }
    ],
    # Clignotement blanc
    "blink": [
        {
            "pixels": list(range(64)),
            "color": (255, 255, 255),
            "duration": 200,
        },
        {
            "pixels": [],
            "color": (0, 0, 0),
            "duration": 200,
        },
        {
            "pixels": list(range(64)),
            "color": (255, 255, 255),
            "duration": 200,
        },
        {
            "pixels": [],
            "color": (0, 0, 0),
            "duration": 200,
        },
    ],
}

