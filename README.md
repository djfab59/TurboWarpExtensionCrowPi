# CrowPi TurboWarp Hardware Bridge

🇫🇷 / 🇬🇧 — README bilingue  
A modular hardware bridge to control CrowPi modules from **TurboWarp**.

---

## 🇫🇷 Français

### 🧩 Présentation

**CrowPi TurboWarp Hardware Bridge** est un projet permettant de piloter les modules matériels du **CrowPi**  
(LCD, capteurs, boutons, LEDs, etc.) depuis **TurboWarp**, **sans modifier TurboWarp**.

Le principe est volontairement simple et robuste :

- **TurboWarp** reste un environnement visuel et rapide
- Un **serveur Python local** est l’unique composant autorisé à accéder au matériel
- TurboWarp communique avec ce serveur via **HTTP en localhost**

✅ Stable  
✅ Extensible  
✅ Pédagogique  
✅ Compatible TurboWarp Web et **TurboWarp Desktop (offline)**

---

### 🏗️ Architecture générale

```
TurboWarp
    │
    │ HTTP (localhost)
    ▼
Python Flask Bridge
    │
    ▼
Modules matériels CrowPi
(LCD, DHT11, Keypad, LED Matrix…)
```

🔒 Un seul processus accède au matériel  
🕒 Le timing et la sécurité sont gérés côté Python  
🧠 TurboWarp reste simple et réactif

---

### 📁 Structure du projet

```
crowpi/
├── run.py                 # Point d’entrée du bridge Python
├── bridge/
│   ├── app.py             # Initialisation Flask + CORS
│   ├── routes/            # API HTTP par module
│   │   └── lcd.py
│   ├── modules/           # Drivers matériels
│   │   └── lcd_mod.py
│   └── shared/            # Verrous & état partagé
│       └── locks.py
└── extension/             # Extensions TurboWarp
    ├── index.js
    └── lcd.js
```

👉 **Un module matériel =**
- 1 driver matériel (`modules/`)
- 1 API HTTP (`routes/`)
- 1 extension TurboWarp (`extension/`)

---

### ▶️ Prérequis

- CrowPi (ou Raspberry Pi avec modules équivalents)
- Python 3
- Bibliothèques matérielles CrowPi installées
- **TurboWarp** (recommandé : **TurboWarp Desktop**)

---

### 🚀 Lancer le bridge Python

```bash
python3 run.py
```

Le serveur démarre sur :

```
http://127.0.0.1:3232
```

---

### 🧪 Tester sans TurboWarp (recommandé)

```bash
curl -X POST http://127.0.0.1:3232/lcd/line \
  -H "Content-Type: application/json" \
  -d '{"line":1,"text":"Hello CrowPi"}'
```

Si cela fonctionne, TurboWarp fonctionnera aussi.

---

### 🎮 Utilisation avec TurboWarp

1. Ouvrir **TurboWarp** (Web ou Desktop)
2. Charger l’extension JavaScript depuis le dossier `extension/`
3. Utiliser les blocs LCD :
   - afficher texte ligne 1 / ligne 2
   - défilement horizontal
   - clear / on / off

Exemple :

```
when green flag clicked
    display "Temp: 23°C" on line 1
    scroll "System ready" line 2 speed 250
```

---

### 🧠 Pourquoi TurboWarp et pas Scratch ?

- Scratch Desktop officiel est verrouillé et non extensible
- TurboWarp permet :
  - extensions personnalisées
  - fonctionnement offline
  - meilleures performances
- Le matériel CrowPi nécessite :
  - gestion du timing
  - sérialisation des accès
  - protection matérielle

👉 Toute la complexité est gérée côté Python  
👉 TurboWarp reste fluide et lisible

---

### 📦 Modules actuels et prévus

- ✅ LCD 16×2 (lignes, clear, scroll horizontal)
- 🔜 Keypad 4×4
- 🔜 Matrice LED 8×8
- 🔜 DHT11 / DHT22
- 🔜 Buzzer

---

### ⚠️ Notes importantes

- TurboWarp peut envoyer plusieurs commandes très rapidement
- Le bridge protège le matériel via :
  - 🔒 verrous (mutex)
  - ⏱ délais contrôlés
- **Ne jamais accéder directement au matériel depuis TurboWarp**

---

## 🇬🇧 English

### 🧩 Overview

**CrowPi TurboWarp Hardware Bridge** allows you to control **CrowPi hardware modules**
(LCD, sensors, buttons, LEDs, etc.) from **TurboWarp**, **without modifying TurboWarp itself**.

Design goals:

- **TurboWarp** stays fast and visual
- A **local Python server** exclusively accesses hardware
- TurboWarp communicates via **HTTP on localhost**

✅ Stable  
✅ Extensible  
✅ Educational  
✅ Works with TurboWarp Web and **TurboWarp Desktop (offline)**

---

### 🏗️ Architecture

```
TurboWarp
    │
    │ HTTP (localhost)
    ▼
Python Flask Bridge
    │
    ▼
CrowPi Hardware Modules
(LCD, DHT11, Keypad, LED Matrix…)
```

---

### 📁 Project structure

```
crowpi/
├── run.py
├── bridge/
│   ├── app.py
│   ├── routes/
│   │   └── lcd.py
│   ├── modules/
│   │   └── lcd_mod.py
│   └── shared/
│       └── locks.py
└── extension/
    ├── index.js
    └── lcd.js
```

One hardware module = one driver + one HTTP API + one TurboWarp extension.

---

### ▶️ Requirements

- CrowPi or compatible Raspberry Pi setup
- Python 3
- CrowPi hardware libraries installed
- **TurboWarp** (recommended: **TurboWarp Desktop**)

---

### 🚀 Start the Python bridge

```bash
python3 run.py
```

Server address:

```
http://127.0.0.1:3232
```

---

### 🧪 Test without TurboWarp

```bash
curl -X POST http://127.0.0.1:3232/lcd/line \
  -H "Content-Type: application/json" \
  -d '{"line":1,"text":"Hello CrowPi"}'
```

---

### 🎮 Use with TurboWarp

1. Open TurboWarp (Web or Desktop)
2. Load the JavaScript extension from `extension/`
3. Use LCD blocks:
   - write line 1 / line 2
   - horizontal scrolling
   - clear / on / off

---

### 🧠 Design rationale

- Scratch Desktop is locked and not extensible
- TurboWarp allows custom extensions and offline usage
- Hardware modules require:
  - timing control
  - serialized access
  - hardware safety

👉 Python handles hardware complexity  
👉 TurboWarp stays clean and beginner-friendly

---

### ✅ License

Personal / educational use.  
Feel free to extend and adapt.

Happy hacking 🚀
