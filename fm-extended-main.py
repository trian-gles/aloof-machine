from live_unit import Controller, LiveFilter
from torch_models import LSTMMemory

MODEL_NAMES = [
    "max-pitch-1.pt",
    "max-pitch-2.pt",
    "max-time-1.pt",
    "max-time-2.pt",
    "pitch-time-1.pt",
    "pitch-time-2.pt"
]

INPUT_NAMES = [
    ["/max", "/pitch"],
    ["/max", "/pitch"],
    ["/max", "/time"],
    ["/max", "/time"],
    ["/pitch", "/time"],
    ["/pitch", "/time"]
]

OUTPUT_NAMES = [
    "/carrier-freq",
    "/modulator-freq",
    "/modulator-amp",
    "/attack",
    "/chaos",
    "/release"
]

FILTERS = [
    [LiveFilter(4), LiveFilter(4)],
    [LiveFilter(4), LiveFilter(4)],
    [LiveFilter(4), LiveFilter(4)],
    [LiveFilter(4), LiveFilter(4)],
    [LiveFilter(4), LiveFilter(4)],
    [LiveFilter(4), LiveFilter(4)]
]


def main():
    controller = Controller(MODEL_NAMES, INPUT_NAMES, FILTERS, OUTPUT_NAMES, visual=False)
    controller.run()

if __name__ == '__main__':
    main()