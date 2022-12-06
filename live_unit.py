from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import time

import torch
from torch_models import LSTMMemory
from collections import deque
from typing import List, Any, Union
import random
import numpy as np

from visual.live_plot import LiveMultiPlot




DEBUG = True

def debug(msg: str):
    if DEBUG:
        print(msg)


IP = "127.0.0.1"
PORT = 9004
OUTPORT = 9006

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
    def __init__(self, model_names, input_names, filters, output_names, visual=False):
        

        self.dispatcher = Dispatcher()
        self.client = SimpleUDPClient(IP, OUTPORT)
        self.server = osc_server.ThreadingOSCUDPServer((IP, PORT), self.dispatcher)

        self.plot = None
        self.visual = visual
        if visual:
            rows = 2
            
            all_inputs = set()

            for inputs in input_names:
                all_inputs.update(inputs)

            all_inputs = list(all_inputs)
            cols = max(len(all_inputs), len(output_names))

            for i, input in enumerate(all_inputs):
                self.dispatcher.map(input, self.handle_plot, i)
            self.plot = LiveMultiPlot(rows, cols, 10, [-4, 4], [all_inputs, output_names])

        self.model_wrappers = []
        for i in range(len(model_names)):
            model_wrap = ModelWrapper(i, model_names[i], input_names[i], filters[i], output_names[i], self.dispatcher, self.client, self.plot)
            self.model_wrappers.append(model_wrap)
                
    
    def handle_plot(self, address, index, *data):
        debug(f"Handling plot for {address} at index {index} with data {data}")
        self.plot.update(0, index[0], data[0])

    def run(self):
        debug("RUNNING SERVER")
        
        self.server.serve_forever()


class ModelWrapper:
    def __init__(self, index: int, name: str, input_names: List[str], filters: List[Union[LiveFilter, None]], 
    output_name: str, dispatcher: Dispatcher, client: SimpleUDPClient, plot: Union[LiveMultiPlot, None]):
        self.index = index
        self.plot = plot
        self.model: LSTMMemory = torch.load("models/" + name)
        self.input_names = input_names
        self.output_name = output_name
        self.stored_vals = {}
        self.client = client
        self.filters = {}

        debug(f"Creating handler for inputs {self.input_names} and outputs {self.output_name} with model {name} and filter {filter}")

        for i, input in enumerate(input_names):
            if filters[i]:
                self.filters[input] = filters[i]
            dispatcher.map(input, self.handle)

    def handle(self, address: str, *args: List[Any]):
        inp = args[0]
        if address in self.filters:
            inp = self.filters[address].input(inp)

        debug(f"Received {address} : {inp} for handler for inputs {self.input_names} and outputs {self.output_name}")

        self.stored_vals[address] = inp

        self.check_vals_full()

    def check_vals_full(self):
        '''If all values are populated, we send out an OSC response'''

        if set(self.input_names) == set(self.stored_vals.keys()):

            inp_list = [self.stored_vals[inp] for inp in self.input_names]
            out = self.model.forward_live(np.array(inp_list).reshape(1, len(self.input_names))).item()

            if self.plot:
                self.plot.update(1, self.index, out)
                self.plot.draw_all()
            self.client.send_message(self.output_name, out * 3)
            self.stored_vals.clear()
            debug(f"Values populated, sending output for {self.output_name}")



