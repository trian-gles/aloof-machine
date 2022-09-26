import torch
from models import LSTMMemory
from collections import deque

from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient


IP = "127.0.0.1"
PORT = 9004

model = torch.load("./vel.pt")
model.reset_live()

class LiveFilter:
    def __init__(self, kernel_size):
        self.past_inputs = deque()
        self.kernel_size = kernel_size

    def input(self, input):
        self.past_inputs.append(input)
        while len(self.past_inputs) > self.kernel_size:
            self.past_inputs.popleft()

        return sum(self.past_inputs) / len(self.past_inputs)

class Controller:
    def __init__(self, model_names, input_names, filters, output_names):
        self.models = [torch.load(name) for name in model_names]


class ModelWrapper:
    def __init__(self, name, input_names, filter, output_name):
        self.model = torch.load(name)

