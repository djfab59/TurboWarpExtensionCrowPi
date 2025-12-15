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

    def __init__(self, hold_s=0.5, uid_poll_s=0.25, uid_retries=3, uid_retry_sleep_s=0.01):
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
        self._uid = ""
        self._last_uid_attempt_at = 0.0

        # Lecture UID (optionnelle) : on limite la fréquence et on retente
        # quelques fois sans impacter la détection de présence.
        self.uid_poll_s = float(uid_poll_s)
        self.uid_retries = max(1, int(uid_retries))
        self.uid_retry_sleep_s = float(uid_retry_sleep_s)

    def _read_raw(self, read_uid=False):
        """
        Lecture "non bloquante" simplifiée :
        - si aucune carte / erreur : (False, "")
        - sinon : (True, uid_str) ; l'UID peut être "" si la lecture UID échoue
          (sans impacter la présence).
        """
        if self._mfrc is None:
            return False, ""

        try:
            # Requête de présence
            error, _data = self._mfrc.MFRC522_Request(self._mfrc.PICC_REQIDL)
            if error:
                return False, ""

            if not read_uid:
                return True, ""

            uid_str = ""
            for attempt in range(self.uid_retries):
                error, uid = self._mfrc.MFRC522_Anticoll()
                if not error and isinstance(uid, (list, tuple)) and len(uid) >= 4:
                    uid_str = "%02X:%02X:%02X:%02X" % (
                        int(uid[0]),
                        int(uid[1]),
                        int(uid[2]),
                        int(uid[3]),
                    )
                    break
                if attempt < self.uid_retries - 1:
                    time.sleep(self.uid_retry_sleep_s)

            return True, uid_str
        except Exception:
            return False, ""

    def step(self):
        """
        Met à jour l'état de présence et détecte les événements insert/remove.
        """
        now = time.time()
        event = None

        # On tente de lire l'UID au moment de l'insert, puis périodiquement
        # tant qu'on n'a pas d'UID (sans spammer).
        want_uid = (not self._stable_present) or (
            self._stable_present
            and not self._uid
            and (now - self._last_uid_attempt_at) >= self.uid_poll_s
        )

        present, uid = self._read_raw(read_uid=want_uid)
        if want_uid and present:
            self._last_uid_attempt_at = now

        prev_uid = self._uid
        if uid:
            self._uid = uid

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
                    self._uid = ""
                    event = "remove"

        # UID obtenu après l'insert : on envoie une mise à jour sans retrigger le chapeau Scratch
        if self._stable_present and self._uid and self._uid != prev_uid and event is None:
            event = "update"

        return self._stable_present, self._uid if self._stable_present else "", event


nfcsensor = NFCSensor()
