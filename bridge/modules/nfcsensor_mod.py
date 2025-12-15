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

    def __init__(self, hold_s=0.5):
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

        # Anti-bruit : une fois une carte détectée, on la considère présente
        # tant qu'on en re-détecte une au moins toutes les hold_s secondes.
        self.hold_s = float(hold_s)
        self._stable_present = False
        self._last_seen_present_at = None

    def _read_raw(self):
        """
        Lecture "non bloquante" simplifiée :
        - si aucune carte / erreur : (False, "")
        - sinon : (True, uid_str) — dans la version simplifiée actuelle,
          on ne lit plus l'UID pour éviter les instabilités, donc uid_str
          sera systématiquement "".
        """
        if self._mfrc is None:
            return False, ""

        try:
            # Requête de présence uniquement (on ne lit plus l'UID ici)
            error, data = self._mfrc.MFRC522_Request(self._mfrc.PICC_REQIDL)
            if error:
                return False, ""

            # On considère simplement qu'une carte est présente si la requête réussit
            return True, ""
        except Exception:
            return False, ""

    def step(self):
        """
        Met à jour l'état de présence et détecte les événements insert/remove.
        """
        present, _ = self._read_raw()

        now = time.time()
        event = None

        if present:
            # On a vu une carte récemment
            self._last_seen_present_at = now
            if not self._stable_present:
                self._stable_present = True
                event = "insert"
        else:
            # Pas de carte vue à cet instant : on ne confirme "remove"
            # que si ça dure plus longtemps que hold_s.
            if self._stable_present:
                last = self._last_seen_present_at
                if last is None or (now - last) >= self.hold_s:
                    self._stable_present = False
                    self._last_seen_present_at = None
                    event = "remove"

        # On ne gère pas l'UID pour l'instant (toujours chaîne vide)
        return self._stable_present, "", event


nfcsensor = NFCSensor()
