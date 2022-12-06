from pythonosc.udp_client import SimpleUDPClient


IP = "127.0.0.1"
PORT = 9006
client = SimpleUDPClient(IP, PORT)

client.send_message("/test/8", 123)

