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
            "pixels_by_color": [
                {
                    "color": (255, 255, 0),
                    "indices": [
                        2, 3, 4, 5,
                        9, 10, 11, 12, 13, 14,
                        16, 17, 19, 20, 22, 23,
                        24, 25, 27, 28, 30, 31, 
                        32, 33, 34, 35, 36, 37, 38, 39, 
                        40, 41, 43, 44, 46, 47, 
                        49, 50, 53, 54,
                        58, 59, 60, 61,
                    ],
                }
            ]
        },
    ],
    # Smiley triste multi‑couleur
    "sad": [
        {
            "pixels_by_color": [
                {
                    "color": (255, 255, 0),
                    "indices": [
                        2, 3, 4, 5,
                        9, 10, 11, 12, 13, 14,
                        16, 17, 19, 20, 22, 23,
                        24, 25, 27, 28, 30, 31, 
                        32, 33, 34, 35, 36, 37, 38, 39, 
                        40, 41, 42, 45, 46, 47, 
                        49, 51, 52, 54,
                        58, 59, 60, 61,
                    ],
                }
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

    # # Smiley triste multi‑couleur
    # "sad": [
    #     {
    #         "pixels_by_color": [
    #             {
    #                 "color": (255, 255, 0),
    #                 "indices": [
    #                     0, 1, 2, 3, 4, 5, 6, 7,
    #                     8, 9, 10, 11, 12, 13, 14, 15,
    #                     16, 17, 18, 19, 20, 21, 22, 23,
    #                     24, 25, 26, 27, 28, 29, 30, 31, 
    #                     32, 33, 34, 35, 36, 37, 38, 39, 
    #                     40, 41, 42, 43, 44, 45, 46, 47, 
    #                     48, 49, 50, 51, 52, 53, 54, 55, 
    #                     56, 57, 58, 59, 60, 61, 62, 63
    #                 ],
    #             }
    #         ]
    #     },
    # ],