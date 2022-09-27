from live_unit import Controller, LiveFilter
from torch_models import LSTMMemory

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

if __name__ == "__main__":
    controller = Controller(MODEL_NAMES, INPUT_NAMES, FILTERS, OUTPUT_NAMES)
    controller.run()


