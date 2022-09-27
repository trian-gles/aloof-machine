from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any


class IDK:
    def __init__(self) -> None:
        IP = "127.0.0.1"
        PORT = 9004
        client = SimpleUDPClient(IP, PORT + 1)

        dispatcher = Dispatcher()

        server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)

        def handle_test1(address: str, *args: List[Any]):
            print(address)
            print(args)

        def handle_test2(address: str, *args: List[Any]):
            print("calling handle test 2")
            client.send_message("/modulator-freq", 123)

        dispatcher.map("/test/*", handle_test1)
        dispatcher.map("/test/*", handle_test2)

        client.send_message("/test/8", 123)

        server.serve_forever()

IDK()