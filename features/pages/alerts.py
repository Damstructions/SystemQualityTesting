class Alerts:
    """Records and accepts the native alert() boxes Demoblaze uses for feedback.

    Playwright only delivers dialog events while a Playwright call is running,
    so waiting is done with page.wait_for_timeout (which pumps the event loop),
    not time.sleep.
    """

    def __init__(self, page):
        self.page = page
        self.messages = []
        page.on("dialog", self._on_dialog)

    def _on_dialog(self, dialog):
        self.messages.append(dialog.message)
        dialog.accept()

    def mark(self):
        """Position to pass to wait_for so only newer alerts count."""
        return len(self.messages)

    def wait_for(self, text, mark=0, timeout=8000):
        waited = 0
        while waited <= timeout:
            if any(text.lower() in m.lower() for m in self.messages[mark:]):
                return True
            self.page.wait_for_timeout(100)
            waited += 100
        return False
