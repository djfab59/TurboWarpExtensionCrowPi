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

    def __init__(self):
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

        self._last_present = None
        self._last_uid = ""

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
        present, uid = self._read_raw()

        # Premier appel : on initialise simplement l'état
        if self._last_present is None:
            self._last_present = present
            self._last_uid = uid
            return present, uid, None

        event = None

        # Changement d'état de présence
        if present and not self._last_present:
            event = "insert"
        elif not present and self._last_present:
            event = "remove"
        # Carte toujours présente mais UID qui change (changement de carte)
        elif present and self._last_present and uid and uid != self._last_uid:
            event = "insert"

        self._last_present = present
        if present and uid:
            self._last_uid = uid
        elif not present:
            uid = ""

        return present, self._last_uid if self._last_uid else "", event


nfcsensor = NFCSensor()
