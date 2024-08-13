""" . """
import socket
import json
from threading import Timer
from .modulive_component import ModuliveComponent

LOCAL_ADDRESS = ("127.0.0.1", 9005)
REMOTE_ADDRESS = ("127.0.0.1", 9004)


class Socket(ModuliveComponent):
    """Component that starts a"""

    def __init__(self):
        super().__init__()

        self._log("Opening Socket...")

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(0)

        self.bind()

        def parse():
            self.process()
            self.send("message", self.canonical_parent.get_state())
            self.canonical_parent.schedule_message(1, parse)

        parse()

    def bind(self):
        """Bind the socket to the LOCAL_ADDRESS port"""
        try:
            self._socket.bind(LOCAL_ADDRESS)
            self._log(
                "Starting on: "
                + str(LOCAL_ADDRESS)
                + ", remote addr: "
                + str(REMOTE_ADDRESS)
            )
        except Exception:
            msg = (
                "ERROR: Cannot bind to "
                + str(LOCAL_ADDRESS)
                + ", port in use. Trying again..."
            )
            self._error(msg)
            timer = Timer(5, self.bind)
            timer.start()

    def send(self, name, obj=None):
        """Send payload to REMOTE_ADDRESS

        Args:
            name (string): the name of the event
            obj (dict): the data to send. Defaults to None.
        """
        # self._log(obj)

        def json_replace(obj):
            return str(obj)

        try:
            self._socket.sendto(
                json.dumps(
                    {"event": name, "data": obj},
                    default=json_replace,
                    ensure_ascii=False,
                ).encode(),
                REMOTE_ADDRESS,
            )
        except Exception as e:
            self._socket.sendto(
                json.dumps(
                    {
                        "event": "error",
                        "data": str(type(e).__name__) + ": " + str(e.args),
                    },
                    default=json_replace,
                    ensure_ascii=False,
                ).encode(),
                REMOTE_ADDRESS,
            )
            self._error("Socket Error " + name + ": " + str(e))

    def process(self):
        """Check socket for received data and handle"""
        try:
            data = self._socket.recv(65536)
            if len(data):
                payload = json.loads(data)
                self.input_handler(payload)
        except socket.error:
            return
        except Exception as e:
            self._error("Error: " + str(e.args))

    def input_handler(self, payload):
        """If received payload requests state, get state from Modulive and return"""
        if payload["event"] == "get_state":
            try:
                state = self.canonical_parent.get_state()
                self.send("give_state", state)
            except Exception as e:
                self._error("Error: " + str(e.args))

    def disconnect(self):
        """Close socket upon disconnect"""
        self._log("Closing Socket...")
        try:
            self._socket.close()
            self._socket = None
        except AttributeError:
            self._error("Socket already closed")
        super().disconnect()
