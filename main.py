import torch
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
import random
from models import LSTMMemory

IP = "127.0.0.1"
PORT = 9004

client = SimpleUDPClient(IP, PORT + 1)

model = torch.load("./vel.pt")
model.reset_live()

def handle_velocity(address, args):
    print(f"Receiving message at {address} : {args}")
    output = model.forward_live(torch.tensor([args]).reshape((1, 1)))
    client.send_message("/freq", output.item())

def test_model():
    with torch.no_grad():
        output = [model.forward_live(torch.rand((1, 1))).item() for _ in range(150)]
        print(output)

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/vel", handle_velocity)

server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)


def main():
    print("RUNNING LIVE")
    server.serve_forever()



if __name__ == '__main__':
    main()