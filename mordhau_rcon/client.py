"""Synchronous client."""

from socket import socket
from typing import Optional
import threading

from mordhau_rcon.exceptions import RequestIdMismatch, WrongPassword
from mordhau_rcon.proto import Packet, Type


__all__ = ['Client']


class Client:
    """An RCON client."""

    __slots__ = ('_socket', 'host', 'port', 'passwd')
    queue = []

    def __init__(self, host: str, port: int, *,
                 timeout: Optional[float] = None,
                 passwd: Optional[str] = None):
        """Initializes the base client with the SOCK_STREAM socket type."""
        self._socket = socket()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.passwd = passwd

    def __enter__(self):
        """Attempts an auto-login if a password is set."""
        self._socket.__enter__()
        self.connect(login=True)
        return self

    def __exit__(self, typ, value, traceback):
        """Delegates to the underlying socket's exit method."""
        return self._socket.__exit__(typ, value, traceback)

    @property
    def timeout(self) -> float:
        """Returns the socket timeout."""
        return self._socket.gettimeout()

    @timeout.setter
    def timeout(self, timeout: float):
        """Sets the socket timeout."""
        self._socket.settimeout(timeout)

    def connect(self, login: bool = False) -> None:
        """Connects the socket and attempts a
        login if wanted and a password is set.
        """
        self._socket.connect((self.host, self.port))

        if self.passwd is not None:
            self.login(self.passwd)

    def close(self) -> None:
        """Closes the socket connection."""
        self._socket.close()

    def communicate(self, packet: Packet) -> Packet:
        """Sends and receives a packet."""
        with self._socket.makefile('wb') as file:
            file.write(bytes(packet))

        return self.read()

    def listen(self) -> Packet:
        """Reads a packet."""
        while True:
            with self._socket.makefile('rb') as file:
                self.queue.append(Packet.read(file))

    def startListen(self) -> Packet:
        x = threading.Thread(target=self.listen)
        x.start()

    def read(self) -> Packet:
        """Reads a packet."""
        with self._socket.makefile('rb') as file:
            return Packet.read(file)

    def login(self, passwd: str) -> bool:
        """Performs a login."""
        response = self.communicate(Packet.make_login(passwd))

        # Wait for SERVERDATA_AUTH_RESPONSE according to:
        # https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
        while response.type != Type.SERVERDATA_AUTH_RESPONSE:
            response = self.read()

        if response.id == -1:
            raise WrongPassword()

        return True

    def run(self, command: str, *arguments: str, raw: bool = False) -> str:
        """Runs a command."""
        request = Packet.make_command(command, *arguments)
        response = self.communicate(request)

        #if response.id != request.id:
            #print(request.id, response.id, "ERROR")

        return response if raw else response.payload

    def run_noresp(self, command: str, *arguments: str, raw: bool = False) -> str:
        request = Packet.make_command(command, *arguments)
        with self._socket.makefile('wb') as file:
            file.write(bytes(request))
