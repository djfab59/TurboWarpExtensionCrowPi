import typing as _t

# Emojis / pictogrammes pré-définis pour la matrice 8x8.
# Chaque "emoji" est une liste de "frames".
# Une frame est un dict :
#   - "pixels":
#       - soit liste d'indices (0-63) → couleur unique (clé "color")
#       - soit liste de dicts {"index": int, "color": (r, g, b)} → multi‑couleur
#   - "pixels_by_color": liste facultative de groupes
#       [{"color": (r, g, b), "indices": [int, ...]}, ...]
#   - "color": tuple (r, g, b) optionnel (mode simple)

EMOJIS: _t.Dict[str, _t.List[_t.Dict[str, _t.Any]]] = {
    # Smiley multi‑couleur : yeux verts, bouche jaune
    "smiley": [
        {
            "pixels": [
                {"index": 10, "color": (0, 255, 0)},   # œil gauche vert
                {"index": 13, "color": (0, 255, 0)},   # œil droit vert
                {"index": 34, "color": (255, 255, 0)}, # bouche jaune
                {"index": 35, "color": (255, 255, 0)},
                {"index": 36, "color": (255, 255, 0)},
                {"index": 37, "color": (255, 255, 0)},
            ]
        },
    ],
    # Smiley triste multi‑couleur : yeux bleus, bouche rouge
    "sad": [
        {
            "pixels": [
                {"index": 10, "color": (0, 0, 255)},   # yeux bleus
                {"index": 13, "color": (0, 0, 255)},
                {"index": 26, "color": (255, 0, 0)},   # bouche rouge inversée
                {"index": 27, "color": (255, 0, 0)},
                {"index": 28, "color": (255, 0, 0)},
                {"index": 29, "color": (255, 0, 0)},
            ]
        },
    ],
    # Cœur rose
    "heart": [
        {
            "pixels_by_color": [
                {
                    "color": (255, 105, 180),
                    "indices": [
                        9, 10, 13, 14,
                        17, 18, 19, 20,
                        24, 25, 26, 27,
                        32, 33, 34,
                        40, 41,
                        48,
                    ],
                }
            ]
        },
    ],
    # Clignotement multi‑couleur
    "blink": [
        {
            "pixels": [
                {"index": i, "color": ((i * 40) % 256, (i * 80) % 256, (i * 120) % 256)}
                for i in range(64)
            ]
        },
        {
            "pixels": []
        },
        {
            "pixels": [
                {"index": i, "color": ((i * 80) % 256, (i * 40) % 256, (i * 160) % 256)}
                for i in range(64)
            ]
        },
        {
            "pixels": []
        },
    ],
}
