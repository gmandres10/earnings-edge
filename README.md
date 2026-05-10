<<<<<<< HEAD
# Earnings Edge

Earnings Edge is a Streamlit app that analyzes a stock's historical earnings surprises and gives a simple probability-style signal for whether the company may beat earnings next quarter.

It pulls market data from Yahoo Finance (`yfinance`), computes earnings surprise metrics, visualizes recent quarters, and estimates implied move using near-term options data.

## What the project does

- Fetches earnings history for a ticker (e.g., `AAPL`, `MSFT`, `GOOGL`).
- Cleans and transforms earnings data into analysis-ready metrics.
- Calculates:
  - Beat rate
  - Average EPS surprise
  - Best and worst quarter by surprise %
- Visualizes up to the last 12 quarters of surprise performance.
- Produces a lightweight "beat probability" score with a recency-weighted method.
- Attempts to estimate implied move from the first available options expiration.
- Lets you save favorite tickers and personal notes locally in JSON.

## How it works

### 1) Data retrieval

- The app uses `yfinance.Ticker` to fetch:
  - `earnings_dates` (historical + upcoming earnings dates when available)
  - `info` fields like company name and current price
  - options chain data for implied move calculation

### 2) Earnings analysis

`EarningsAnalyzer`:
- Removes rows with missing EPS estimate/reported EPS.
- Computes surprise:
  - `Surprise % = (Reported EPS - EPS Estimate) / abs(EPS Estimate) * 100`
- Labels each quarter as:
  - `✅ Beat` if surprise > 0
  - `❌ Miss` otherwise
- Exposes summary methods used in the dashboard metrics.

### 3) Prediction logic

`Predictor`:
- Uses the analyzer output and applies a weighted beat-rate approach:
  - Last 4 quarters get double weight.
  - Older quarters get normal weight.
- Converts weighted result into:
  - beat probability percentage
  - qualitative label:
    - `🟢 High Probability of Beat` (>= 70%)
    - `🟡 Coin Flip` (>= 45% and < 70%)
    - `🔴 Likely Miss` (< 45%)
- Estimates implied move as:
  - ATM call last price + ATM put last price (straddle)
  - divided by current stock price

### 4) Favorites and notes

`FavoritesManager` writes JSON next to the entrypoint package you launch. **`src/data` and `dist/data` are independent** (separate files; nothing is synced automatically):

| Command | Favorites path |
|---------|----------------|
| `streamlit run src/main.py` | `src/data/favorites.json` |
| `streamlit run dist/main.py` | `dist/data/favorites.json` |

Each ticker entry can store metadata plus a serialized earnings snapshot (`data` rows). Older examples may only have a note field.

## Project structure

```text
earnings-edge/
  src/
    main.py               # Streamlit app entrypoint (playground)
    earnings_analyzer.py  # Earnings transformation and metrics
    predictor.py          # Beat probability + implied move logic
    favorites_manager.py  # Local favorites persistence
    get_data.py           # Helper class for yfinance access
    data/
      favorites.json      # Persistence when running src
  dist/
    main.py               # Documented parity copy of src
    ...                   # Same modules + docstrings as src
    data/
      favorites.json      # Persistence when running dist (independent from src/data)
  Demo.mp4                # Demo video asset
```

## Setup

No dependency manifest is currently included (`requirements.txt`/`pyproject.toml`), so install packages manually:

```bash
pip install streamlit yfinance pandas matplotlib
```

## Run the app

From the project root:

```bash
streamlit run src/main.py
```

If you specifically want the runtime copy:

```bash
streamlit run dist/main.py
```

## Usage

1. Enter a ticker in the sidebar.
2. Click **Analyze Earnings**.
3. Review:
   - surprise chart
   - earnings history table
   - prediction panel (probability, verdict, implied move)
4. Add a note and save to favorites.
5. Re-open favorites from the sidebar for quick reload.

## Notes and limitations

- Data quality/availability depends on Yahoo Finance (`yfinance`).
- "Beat probability" is heuristic, not a statistical model or financial advice.
- Implied move can be unavailable if options or price fields are missing.
- Favorites are stored locally in JSON (not synced/cloud-backed).

## Future improvements

- Add `requirements.txt` and pinned dependency versions.
- Add tests for analyzer/predictor behavior.
- Add confidence intervals or model-based forecasting.
- Add export/share options for analysis snapshots.

## Disclaimer

=======
# Earnings Edge

Earnings Edge is a Streamlit app that analyzes a stock's historical earnings surprises and gives a simple probability-style signal for whether the company may beat earnings next quarter.

It pulls market data from Yahoo Finance (`yfinance`), computes earnings surprise metrics, visualizes recent quarters, and estimates implied move using near-term options data.

## What the project does

- Fetches earnings history for a ticker (e.g., `AAPL`, `MSFT`, `GOOGL`).
- Cleans and transforms earnings data into analysis-ready metrics.
- Calculates:
  - Beat rate
  - Average EPS surprise
  - Best and worst quarter by surprise %
- Visualizes up to the last 12 quarters of surprise performance.
- Produces a lightweight "beat probability" score with a recency-weighted method.
- Attempts to estimate implied move from the first available options expiration.
- Lets you save favorite tickers and personal notes locally in JSON.

## How it works

### 1) Data retrieval

- The app uses `yfinance.Ticker` to fetch:
  - `earnings_dates` (historical + upcoming earnings dates when available)
  - `info` fields like company name and current price
  - options chain data for implied move calculation

### 2) Earnings analysis

`EarningsAnalyzer`:
- Removes rows with missing EPS estimate/reported EPS.
- Computes surprise:
  - `Surprise % = (Reported EPS - EPS Estimate) / abs(EPS Estimate) * 100`
- Labels each quarter as:
  - `✅ Beat` if surprise > 0
  - `❌ Miss` otherwise
- Exposes summary methods used in the dashboard metrics.

### 3) Prediction logic

`Predictor`:
- Uses the analyzer output and applies a weighted beat-rate approach:
  - Last 4 quarters get double weight.
  - Older quarters get normal weight.
- Converts weighted result into:
  - beat probability percentage
  - qualitative label:
    - `🟢 High Probability of Beat` (>= 70%)
    - `🟡 Coin Flip` (>= 45% and < 70%)
    - `🔴 Likely Miss` (< 45%)
- Estimates implied move as:
  - ATM call last price + ATM put last price (straddle)
  - divided by current stock price

### 4) Favorites and notes

`FavoritesManager` stores favorites in JSON (`data/favorites.json`) with schema:

```json
{
  "AAPL": {
    "note": "My thesis for next earnings..."
  }
}
```

## Project structure

```text
earnings-edge/
  src/
    main.py               # Streamlit app entrypoint (source version)
    earnings_analyzer.py  # Earnings transformation and metrics
    predictor.py          # Beat probability + implied move logic
    favorites_manager.py  # Local favorites/note persistence
    get_data.py           # Helper class for yfinance access
    data/
      favorites.json
  dist/
    ...                   # Runtime copy/build output of the app modules
  Demo.mp4                # Demo video asset
```

## Setup

No dependency manifest is currently included (`requirements.txt`/`pyproject.toml`), so install packages manually:

```bash
pip install streamlit yfinance pandas matplotlib
```

## Run the app

From the project root:

```bash
streamlit run src/main.py
```

If you specifically want the runtime copy:

```bash
streamlit run dist/main.py
```

## Usage

1. Enter a ticker in the sidebar.
2. Click **Analyze Earnings**.
3. Review:
   - surprise chart
   - earnings history table
   - prediction panel (probability, verdict, implied move)
4. Add a note and save to favorites.
5. Re-open favorites from the sidebar for quick reload.

## Notes and limitations

- Data quality/availability depends on Yahoo Finance (`yfinance`).
- "Beat probability" is heuristic, not a statistical model or financial advice.
- Implied move can be unavailable if options or price fields are missing.
- Favorites are stored locally in JSON (not synced/cloud-backed).

## Future improvements

- Add `requirements.txt` and pinned dependency versions.
- Add tests for analyzer/predictor behavior.
- Add confidence intervals or model-based forecasting.
- Add export/share options for analysis snapshots.

## Disclaimer

>>>>>>> 449af2c2f31310d488cb86aad0bc5996cce4b4f2
This project is for educational and informational purposes only. It is not investment advice.