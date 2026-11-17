"""Multivariate LSTM forecasting example in PyTorch with sliding-window DataLoader."""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


class MultivariateLSTM(nn.Module):
    """Multi-layer LSTM for multivariate-to-univariate next-step forecasting."""

    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, output_dim: int = 1) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=0.1 if num_layers > 1 else 0.0,
        )
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


def create_windows(arr: np.ndarray, seq_len: int) -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(len(arr) - seq_len):
        X.append(arr[i : i + seq_len])
        y.append(arr[i + seq_len, 0])
    return np.array(X), np.array(y)[:, None]


def run_lstm_experiment(epochs: int = 25) -> tuple[float, float]:
    np.random.seed(42)
    torch.manual_seed(42)

    T = 400
    t = np.arange(T)
    f1 = np.sin(0.1 * t) + 0.05 * np.random.randn(T)
    f2 = np.cos(0.1 * t) + 0.05 * np.random.randn(T)
    f3 = 0.5 * f1 + 0.3 * f2 + 0.05 * np.random.randn(T)
    data = np.stack([f1, f2, f3], axis=1).astype(np.float32)

    seq_len = 24
    X, y = create_windows(data, seq_len)
    split = int(0.8 * len(X))

    train_ds = TensorDataset(torch.from_numpy(X[:split]), torch.from_numpy(y[:split]))
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

    model = MultivariateLSTM(input_dim=3, hidden_dim=64, num_layers=2, output_dim=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    train_mse = 0.0
    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(xb)
        train_mse = total_loss / len(train_ds)
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch + 1:02d} | Train MSE: {train_mse:.5f}")

    model.eval()
    with torch.no_grad():
        preds = model(torch.from_numpy(X[split:]))
        test_mse = criterion(preds, torch.from_numpy(y[split:])).item()
    return train_mse, test_mse


def main() -> None:
    _, test_mse = run_lstm_experiment()
    print(f"Test MSE: {test_mse:.5f}")


if __name__ == "__main__":
    main()
