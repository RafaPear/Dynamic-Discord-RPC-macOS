import os
from pypresence import Presence
from pypresence.types import ActivityType

class DiscordRPC:
    def __init__(self, client_id: str):
        self.rpc = Presence(client_id)
        self.rpc.connect()
        self.pid = os.getpid()
        self.connected = True

    def disconnect(self):
        if self.connected:
            try:
                self.rpc.clear(self.pid)
                self.rpc.close()
            except Exception:
                pass
            self.connected = False

    def reconnect(self):
        if not self.connected:
            self.rpc.connect()
            self.connected = True

    def update(self, app):
        payload = {
            "name": app.app_name[:128],
            
            "pid": self.pid,

            "details": app.app_name[:128],

            "state": app.window_title[:128],

            "large_image": app.process_name.lower(),
            "large_text": f"Processo: {app.process_name}"[:128],

            "small_image": "clock",
            "small_text": f"Tempo em foco: {int(app.total_focused_time())}s"[:128],

            "start": int(app.open_time),
            "buttons": [
                    {
                        "label": "ME",
                        "url": "https://github.com/rafapear"
                    }
                ],
        }

        self.rpc.update(**payload)
        return payload

    def clear(self):
        self.rpc.clear(self.pid)
