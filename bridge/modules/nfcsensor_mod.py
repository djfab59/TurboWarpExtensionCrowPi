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

    def __init__(self, debounce_s=0.2):
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

        # Durée minimale pendant laquelle un changement doit être
        # observé avant d'être confirmé (anti-bruit).
        self.debounce_s = debounce_s

        # État "stabilisé" (celui qu'on expose)
        self._last_stable_present = False

        # État candidat en cours de validation
        self._candidate_present = None
        self._candidate_since = time.time()

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

        # Initialisation du candidat
        if self._candidate_present is None:
            self._candidate_present = present
            self._candidate_since = now

        # Si l'état lu diffère de l'état stabilisé,
        # on attend qu'il reste stable pendant debounce_s.
        if present != self._last_stable_present:
            if present != self._candidate_present:
                # Nouveau candidat : on repart le chrono
                self._candidate_present = present
                self._candidate_since = now
            else:
                # Même candidat que précédemment : on regarde si ça dure assez longtemps
                if now - self._candidate_since >= self.debounce_s:
                    # On confirme le changement
                    self._last_stable_present = present
                    if present:
                        event = "insert"
                    else:
                        event = "remove"
        else:
            # L'état lu correspond à l'état stabilisé : on reset le candidat
            self._candidate_present = present
            self._candidate_since = now

        # On ne gère pas l'UID pour l'instant (toujours chaîne vide)
        return self._last_stable_present, "", event


nfcsensor = NFCSensor()
