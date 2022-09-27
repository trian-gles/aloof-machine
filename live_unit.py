from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import time

import torch
from torch_models import LSTMMemory
from collections import deque
from typing import List, Any, Union
import random




DEBUG = True

def debug(msg: str):
    if DEBUG:
        print(msg)


IP = "127.0.0.1"
PORT = 9004

class LiveFilter:
    def __init__(self, kernel_size: int):
        self.past_inputs = deque()
        self.kernel_size = kernel_size
        


    def input(self, input: float) -> float:
        self.past_inputs.append(input)
        while len(self.past_inputs) > self.kernel_size:
            self.past_inputs.popleft()

        return sum(self.past_inputs) / len(self.past_inputs)  

class Controller:
    def __init__(self, model_names, input_names, filters, output_names):

        self.dispatcher = Dispatcher()
        self.client = SimpleUDPClient(IP, PORT + 1)
        self.server = osc_server.ThreadingOSCUDPServer((IP, PORT), self.dispatcher)

        self.model_wrappers = []
        for i in range(len(model_names)):
            model_wrap = ModelWrapper(model_names[i], input_names[i], filters[i], output_names[i], self.dispatcher, self.client)
            self.model_wrappers.append(model_wrap)

    def run(self):
        time.sleep(1)
        debug("RUNNING SERVER")
        
        self.server.serve_forever()


class ModelWrapper:
    def __init__(self, name: str, input_names: List[str], filter: Union[LiveFilter, None], output_name: str, dispatcher: Dispatcher, client: SimpleUDPClient):
        self.model: LSTMMemory = torch.load("models/" + name)
        self.input_names = input_names
        self.output_name = output_name
        self.stored_vals = {}
        self.client = client
        self.filter = filter

        debug(f"Creating handler for inputs {self.input_names} and outputs {self.output_name} with model {name} and filter {filter}")

        for input in input_names:
            dispatcher.map(input, self.handle)

    def handle(self, address: str, *args: List[Any]):
        inp = args[0]
        if self.filter:
            inp = self.filter.input(inp)

        debug(f"Received {inp} for handler for inputs {self.input_names} and outputs {self.output_name}")
        self.stored_vals[address] = args[0]

    def check_vals_full(self):
        '''If all values are populated, we send out an OSC response'''

        if set(self.input_names) == set(self.stored_vals.keys()):
            # run the model here
            self.client.send_message(self.output_name, random.random())
            self.stored_vals.clear()
            debug(f"Values populated, sending output for {self.output_name}")


if __name__ == "__main__":
    MODEL_NAMES = [
        "max-pitch-1.pt",
        "max-pitch-2.pt",
        "time-max-1.pt"
    ]

    INPUT_NAMES = [
        ["/max", "/pitch"],
        ["/max", "/pitch"],
        ["/time", "/max"]
    ]

    OUTPUT_NAMES = [
        "/carrier-freq",
        "/modulator-freq",
        "/modulator-amp"
    ]

    FILTERS = [
        LiveFilter(4),
        None,
        None
    ]
    
    controller = Controller(MODEL_NAMES, INPUT_NAMES, FILTERS, OUTPUT_NAMES)
    controller.run()

