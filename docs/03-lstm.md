# LSTMs (PyTorch & TensorFlow)

**Long Short-Term Memory (LSTM)** networks are gated Recurrent Neural Networks (RNNs) designed to learn sequential dependencies while mitigating vanishing gradients via input, forget, and output gates.

Unlike classical univariate models, LSTMs naturally ingest **multivariate sequences** as 3D tensors:

$$\text{Input Shape} = (\text{Batch Size},\ \text{Sequence Length / Lookback},\ \text{Number of Features})$$

---

## Real-World Use Cases

- **Energy & Smart Grids:** Multi-step solar, wind, and grid load forecasting from historical load + multi-variable weather forecasts.
- **Industrial IoT & Predictive Maintenance:** Forecasting equipment degradation from multivariate telemetry (vibration, temperature, pressure, RPM).
- **Smart Cities & Traffic:** Predicting congestion and transit delays from loop detectors, weather, and event calendars.
- **Financial Markets:** Modeling order-book or multi-asset dynamics (prices, volume, volatility, sentiment).

---

## TensorFlow / Keras Equivalent Pattern

While the runnable sample uses **PyTorch**, the equivalent **TensorFlow / Keras** architecture is:

```python
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.models import Sequential

model = Sequential([
    Input(shape=(24, 3)),  # (seq_len, num_features)
    LSTM(64, return_sequences=False),
    Dense(1),
])
model.compile(optimizer="adam", loss="mse")
```

---

## Limitations

- **Sequential Training Bottleneck:** Step $t$ depends on $t-1$, preventing time-axis parallelization (unlike Transformers or TCNs).
- **Over-Smoothing & Lagging:** Minimizing MSE under uncertainty often pushes predictions toward the conditional mean or a 1-step lag.
- **Hyperparameter & Scaling Sensitivity:** Requires careful normalization (fit scalers on train split only to avoid leakage).
- **Low Interpretability:** Requires post-hoc attribution (e.g., SHAP, Integrated Gradients) for feature explanations.

---

## Runnable Sample

See [03_lstm_multivariate.py](file:///c:/Users/naini/time-series/examples/03_lstm_multivariate.py) for a complete PyTorch sliding-window multivariate LSTM training and evaluation script:

```powershell
.\.venv\Scripts\python.exe examples/03_lstm_multivariate.py
```
