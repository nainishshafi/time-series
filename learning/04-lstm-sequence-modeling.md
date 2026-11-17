# Module 4: Multivariate LSTMs for Time Series

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md) · Runnable Script: [03_lstm_multivariate.py](file:///c:/Users/naini/time-series/examples/03_lstm_multivariate.py)

## Table of Contents

- [1. Sliding-Window Framing & 3D Tensors](#1-sliding-window-framing--3d-tensors)
- [2. Inside an LSTM Cell](#2-inside-an-lstm-cell)
- [3. PyTorch Model & Training Loop](#3-pytorch-model--training-loop)
- [4. Avoiding Scaling Leakage](#4-avoiding-scaling-leakage)
- [5. Common Failure Modes](#5-common-failure-modes)
- [6. Hands-On Exercises](#6-hands-on-exercises)

---

## 1. Sliding-Window Framing & 3D Tensors

To train a neural network on sequences, convert a 2D matrix of shape `(T, num_features)` into overlapping lookback windows of length `seq_len`:

$$\text{X shape} = (\text{Batch Size},\ \text{seq\_len},\ \text{num\_features}), \qquad \text{y shape} = (\text{Batch Size},\ 1)$$

In [03_lstm_multivariate.py](file:///c:/Users/naini/time-series/examples/03_lstm_multivariate.py), `create_windows(data, seq_len=24)` pairs each 24-step window of 3 features with the next-step value of feature 0.

---

## 2. Inside an LSTM Cell

Standard RNNs suffer from vanishing gradients over long windows. An LSTM maintains a **cell state** $c_t$ alongside a **hidden state** $h_t$, regulated by three gates:

1. **Forget gate:** Decides what fraction of $c_{t-1}$ to discard.
2. **Input gate:** Decides what new candidate information to write into $c_t$.
3. **Output gate:** Filters $c_t$ to produce $h_t$.

---

## 3. PyTorch Model & Training Loop

In `MultivariateLSTM`:
- `nn.LSTM(..., batch_first=True)` processes `(batch, seq_len, input_dim)` and outputs `(batch, seq_len, hidden_dim)`.
- `out[:, -1, :]` extracts the final hidden representation at the end of the lookback window.
- `nn.Linear(hidden_dim, 1)` projects that representation to the scalar forecast.

---

## 4. Avoiding Scaling Leakage

When features have different scales (e.g., temperature vs. kilowatt load), fit `StandardScaler` or `MinMaxScaler` **only on the training split**, then call `.transform()` on validation/test splits. Fitting on the full dataset leaks future min/max or mean/variance into training.

---

## 5. Common Failure Modes

- **1-Step Lagging under MSE:** When a series is noisy, minimizing MSE often rewards predicting something close to $y_{t-1}$ (a naive persistence lag).
- **Over-Smoothing on Multi-Step Horizons:** Direct or recursive multi-step forecasts tend to flatten toward the conditional mean.
- **Sequential Training Speed:** Steps $1 \dots L$ are computed sequentially, making LSTMs slower to train than TCNs or Transformers.

---

## 6. Hands-On Exercises

1. Run `.\.venv\Scripts\python.exe examples/03_lstm_multivariate.py` and observe `Train MSE` vs. `Test MSE`.
2. Experiment with `seq_len=12` vs. `seq_len=48` and `hidden_dim=32` vs. `128`.
3. Modify `create_windows` and `output_dim=3` to predict a 3-step horizon `[t, t+1, t+2]` simultaneously.
