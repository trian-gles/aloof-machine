import matplotlib.pyplot as plt
import time
from typing import List, Union
from collections import deque
import random

class LiveMultiPlot:
    DEFAULT_YLIM = [-3, 3]

    def __init__(self, rows: int, cols: int, size = 10, ylim: List[float] = DEFAULT_YLIM, titles: Union[None, List[List[str]]] = None):
        plt.ion()
        self.fig = plt.figure(constrained_layout=True)
        self.axs = self.fig.subplots(rows, cols, sharex=True, sharey=True)
        self._rows = rows
        self._cols = cols
        self.queues: List[List[deque]] = []
        self.lines = []
        empty_list = [0 for _ in range(size)]
        for i in range(rows):
            queue_row = []
            line_row = []
            for j in range(cols):
                queue = deque(empty_list)
                queue_row.append(queue)
                line_row.append(self.axs[i][j].plot(queue))
                self.axs[i][j].set_ylim(ylim)
                if titles:
                    self.axs[i][j].set_title(titles[i][j])

            self.queues.append(queue_row)
            self.lines.append(line_row)
        
        self.draw_all()



    def update_all(self, data: List[List[float]]):
        for i in range(self._rows):
            for j in range(self._cols):
                self.queues[i][j].append(data[i][j])
                self.queues[i][j].popleft()
        self.draw_all()

    def update(self, row: int, col: int, num: float):
        self.queues[row][col].append(num)
        self.queues[row][col].popleft()
        # self.draw_all()

    def draw_all(self):
        for i in range(self._rows):
            for j in range(self._cols):
                self.lines[i][j][0].set_ydata(self.queues[i][j])
        self.fig.canvas.draw()

    def close(self):
        plt.pause(0.01)
        plt.close()
                


if __name__ == "__main__":
    
    rows = 3
    cols = 4
    size = 10
    plot = LiveMultiPlot(rows, cols, size)

    for _ in range(200):
        i = random.randrange(0, rows)
        j = random.randrange(0, cols)
        num = random.uniform(-4, 4)
        plot.update(i, j, num)
        time.sleep(1)

    plot.close()


