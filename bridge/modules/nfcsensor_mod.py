import time

try:
    from mfrc522 import SimpleMFRC522
except Exception:
    # Permet d'importer le module sur une machine sans NFC
    SimpleMFRC522 = None


class NFCSensor:
    """
    Gestion du lecteur NFC (MFRC522) du CrowPi.

    On fournit une API simple orientée présence de carte :
    - step() retourne (present, uid, event) où :
        present : booléen (carte détectée ou non, état "stabilisé")
        uid     : chaîne UID "xx:xx:xx:xx" ou "" si aucune carte
        event   : "insert", "remove" ou None
    """

    def __init__(self, consecutive_required=5):
        if SimpleMFRC522 is not None:
            try:
                self.reader = SimpleMFRC522()
                # On utilise l'objet bas niveau interne pour lire sans bloquer.
                self._mfrc = self.reader.READER
            except Exception:
                self.reader = None
                self._mfrc = None
        else:
            self.reader = None
            self._mfrc = None

        # Nombre de lectures consécutives nécessaires avant de valider
        # un changement d'état (anti-bruit).
        self._consecutive_required = max(1, int(consecutive_required))

        # État "stabilisé"
        self._last_present = False
        self._last_uid = ""

        # Compteurs pour lisser les lectures instables
        self._present_count = 0
        self._absent_count = 0
        self._initialized = False

    def _read_raw(self):
        """
        Lecture "non bloquante" simplifiée :
        - si aucune carte / erreur : (False, "")
        - sinon : (True, uid_str)
        """
        if self._mfrc is None:
            return False, ""

        try:
            # Requête de présence
            error, data = self._mfrc.MFRC522_Request(self._mfrc.PICC_REQIDL)
            if error:
                return False, ""

            # Anti-collision pour récupérer l'UID
            error, uid = self._mfrc.MFRC522_Anticoll()
            if error:
                return False, ""

            # UID sous forme de chaîne lisible
            if isinstance(uid, (list, tuple)) and len(uid) >= 4:
                uid_str = "%02X:%02X:%02X:%02X" % (
                    int(uid[0]),
                    int(uid[1]),
                    int(uid[2]),
                    int(uid[3]),
                )
            else:
                uid_str = ""

            return True, uid_str
        except Exception:
            return False, ""

    def step(self):
        """
        Met à jour l'état de présence et détecte les événements insert/remove
        avec un peu d'anti-rebond pour éviter les boucles insert/remove
        dues aux lectues instables du MFRC522.
        """
        present, uid = self._read_raw()

        # Premier appel : on initialise simplement l'état
        if not self._initialized:
            self._initialized = True
            self._last_present = bool(present)
            self._last_uid = uid or ""
            if present:
                self._present_count = 1
                self._absent_count = 0
            else:
                self._present_count = 0
                self._absent_count = 1
            return self._last_present, self._last_uid, None

        # Mise à jour des compteurs de présence/absence consécutives
        if present:
            self._present_count += 1
            self._absent_count = 0
        else:
            self._absent_count += 1
            self._present_count = 0

        event = None

        # Validation d'une insertion après plusieurs lectures consécutives "présent"
        if present and not self._last_present and self._present_count >= self._consecutive_required:
            self._last_present = True
            if uid:
                self._last_uid = uid
            event = "insert"

        # Validation d'un retrait après plusieurs lectures consécutives "absent"
        elif not present and self._last_present and self._absent_count >= self._consecutive_required:
            self._last_present = False
            self._last_uid = ""
            event = "remove"

        # Carte considérée comme présente, mais UID qui change (on a changé de carte)
        elif present and self._last_present and uid and uid != self._last_uid:
            # On exige aussi quelques lectures cohérentes pour éviter les glitches
            if self._present_count >= self._consecutive_required:
                self._last_uid = uid
                event = "insert"

        # Si la carte est stablement présente, on met à jour l'UID dès qu'on a une lecture valide
        if self._last_present and uid:
            self._last_uid = uid

        return self._last_present, self._last_uid if self._last_uid else "", event


nfcsensor = NFCSensor()
