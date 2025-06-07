import os
import pandas as pd, torch, joblib
from sklearn.ensemble import RandomForestRegressor
from torch import nn
from sklearn.model_selection import train_test_split

# TODO: implement periodic retraining pipeline

DB_URL = os.getenv("DB_URL", "postgresql://invest:invest@postgres/invest")
df = pd.read_sql("select * from features", DB_URL)
X = df.filter(regex="^feat_").to_numpy()
y = df["target"].to_numpy()

# ----- RF -----
rf = RandomForestRegressor(n_estimators=200, n_jobs=-1).fit(X, y)
joblib.dump(rf, "rf.pkl")

# ----- DNN -----
class Net(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, 128), nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.net(x)

net = Net(X.shape[1])
opt = torch.optim.Adam(net.parameters(), 1e-3)
loss_fn = nn.MSELoss()
Xt, Xv, yt, yv = train_test_split(X, y, test_size=.2, random_state=42)
Xt = torch.tensor(Xt).float(); yt = torch.tensor(yt).float().unsqueeze(1)
for epoch in range(20):
    net.train(); opt.zero_grad()
    pred = net(Xt); loss = loss_fn(pred, yt)
    loss.backward(); opt.step()

torch.save(net.state_dict(), "dnn.pt")
