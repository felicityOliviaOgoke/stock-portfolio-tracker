# Stock Portfolio Tracker

A real-time stock price monitoring dashboard built with Python. It polls live data using **yfinance**, stores it in **PostgreSQL**, and visualizes it via **Streamlit** + **Plotly**.

---

##  Goals
- Polls live stock prices every minute  
- Persists time-series data in PostgreSQL  
- Interactive dashboard (line chart, price delta, last update)  
-  Fully configurable through `.env`  
-  Clean, single-page UI  

---

## Tech Stack
| Layer      | Tools / Libraries                          |
|------------|--------------------------------------------|
| Backend    | Python · yfinance · SQLAlchemy · psycopg2 |
| Database   | PostgreSQL                                 |
| Frontend   | Streamlit · Plotly · Pandas                |

---

##  Quick Start

### 1 Clone
```bash
git clone https://github.com/felicityOliviaOgoke/stock-portfolio-tracker.git
cd stock-portfolio-tracker
```

### 2 Create & Activate venv
```bash
python -m venv .venv

```

### 3 Install deps
```bash
pip install -r requirements.txt
```

### 4 Configure .env
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
```

### 5 Start Poller
```bash
python scripts/poll_live_prices.py
```

### 6 Launch Dashboard
```bash
streamlit run scripts/dashboard.py
```

---

## Project Structure
```
stock-portfolio-tracker/
├── scripts/
│   ├── poll_live_prices.py   # Polls & inserts data
│   └── dashboard.py          # Streamlit app
├── .env                      # DB credentials (local)
├── requirements.txt          # Python dependencies
└── README.md                 # You’re reading it!
```

---
<img width="824" height="272" alt="image" src="https://github.com/user-attachments/assets/9e7b844a-faac-48e8-ae20-7865da570273" />



*Happy tracking!*
