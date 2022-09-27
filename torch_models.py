import torch
from sklearn.preprocessing import StandardScaler
import numpy as np


class LSTMMemory(torch.nn.Module):

  def __init__(self, hidden_size, input_size=1, output_size=1):
    super().__init__()
    self._scaler = StandardScaler()
    self._hidden_state = None
    self.lstm = torch.nn.LSTM(
        input_size = input_size,
        hidden_size = hidden_size,
        batch_first = True
    )
    self.linear = torch.nn.Linear(
            in_features=hidden_size,
            out_features=output_size
        )

  def forward(self, x):
    h = self.lstm(x)[0]

    return self.linear(h)

  def forward_live(self, x):
    x = torch.tensor(self._scaler.transform(x).reshape((1, 1)).astype(np.float32))
    if self._hidden_state:
      h, self._hidden_state = self.lstm(x, self._hidden_state)
    else:
      h, self._hidden_state = self.lstm(x)

    return self.linear(h)
  
  def reset_live(self):
    self._hidden_state = None

  def fit(self, data):
    self._scaler.fit(data)

  def transform(self, data):
    return self._scaler.transform(data)

  def fit_transform(self, data):
    return self._scaler.fit_transform(data)

