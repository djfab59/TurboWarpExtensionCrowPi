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
        present : booléen (carte détectée ou non)
        uid     : chaîne UID "xx:xx:xx:xx" ou "" si aucune carte
        event   : "insert", "remove" ou None
    """

    def __init__(self, debounce_s=0.05):
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

        # Petit délai d'anti-rebond lors d'un changement d'état.
        self.debounce_s = debounce_s

        # État précédent (None = non initialisé)
        self._last_present = None
        self._last_uid = ""

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
        Met à jour l'état de présence et détecte les événements insert/remove.
        Un petit anti-rebond temporel est appliqué lorsqu'on détecte un
        changement de présence pour filtrer les micro-coupures.
        """
        present, uid = self._read_raw()

        # Premier appel : on initialise simplement l'état
        if self._last_present is None:
            self._last_present = present
            self._last_uid = uid or ""
            return present, self._last_uid, None

        event = None

        # Changement de présence détecté -> on confirme après un court délai
        if present != self._last_present:
            time.sleep(self.debounce_s)
            present2, uid2 = self._read_raw()
            # Si finalement l'état n'a pas réellement changé, on ignore
            if present2 != present:
                return self._last_present, self._last_uid or "", None

            # Changement confirmé
            present = present2
            if present:
                uid = uid2

            if present and not self._last_present:
                event = "insert"
            elif not present and self._last_present:
                event = "remove"

            self._last_present = present

        # Gestion du changement de carte (UID différent alors que la carte est présente)
        if self._last_present and present and uid:
            if self._last_uid and uid != self._last_uid:
                # Nouvelle carte : on signale un "insert" avec le nouvel UID
                if event is None:
                    event = "insert"
            self._last_uid = uid
        elif not present:
            # Plus de carte présente
            self._last_uid = ""

        return self._last_present, self._last_uid if self._last_uid else "", event


nfcsensor = NFCSensor()
