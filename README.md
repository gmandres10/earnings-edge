# Earnings Edge

Earnings Edge is a Streamlit app for exploring a stock's earnings history, calculating EPS surprise metrics, and estimating a simple "beat probability" signal for upcoming earnings.

## Features

- Analyze historical earnings results for any supported ticker (for example: `AAPL`, `MSFT`, `GOOGL`).
- View beat rate, average EPS surprise, best quarter, and worst quarter.
- Visualize quarterly EPS surprises in a chart.
- See a basic prediction panel (beat probability, verdict label, implied move, next earnings date).
- Save favorites and personal notes per ticker.

## Requirements

- Python 3.10+ recommended.
- Internet access (the app fetches market data from Yahoo Finance via `yfinance`).

## Installation

From the project root:

1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   - `pip install -r requirements.txt`

If you do not have a `requirements.txt`, install the main packages manually:

- `pip install streamlit yfinance pandas matplotlib`

## How To Run

Run from the project root folder.

- Development version (`src`):
  - `streamlit run src/main.py`
- Graded version (`dist`):
  - `streamlit run dist/main.py`

## User Guide (Help)

1. Enter a ticker symbol in the sidebar.
2. Click **Analyze Earnings**.
3. Review:
   - **EPS Surprise % Per Quarter** tab for charted performance.
   - **Earnings History** tab for the data table.
   - **Prediction** tab for beat probability and implied move estimate.
4. Add notes in **Personal Note for this Stock**.
5. Click **Add to Favorites** to save the ticker and note.
6. Reopen saved favorites from the sidebar list.

## Development and Grading Workflow

- `src/` is the development environment:
  - Experiment freely.
  - It is acceptable to iterate, refactor, and temporarily break behavior while testing ideas.
- `dist/` is the graded environment:
  - Keep it stable and clean.
  - Only copy code from `src/` into `dist/` after you have validated that the `src/` version works correctly.
  - `dist/` should represent your final documented and reliable implementation.

## File Structure

- `src/` - development source code.
  - `src/main.py` - Streamlit app entry point (development version).
  - `src/earnings_analyzer.py` - earnings cleaning and metric calculations.
  - `src/predictor.py` - beat probability, implied move, and next earnings date logic.
  - `src/favorites_manager.py` - save/load favorites and notes from JSON.
  - `src/get_data.py` - helper wrapper around `yfinance` data fetching.
  - `src/data/favorites.json` - persisted favorites and notes for `src`.
- `dist/` - documented and graded-ready source code.
  - `dist/main.py` - Streamlit app entry point for the graded build.
  - `dist/earnings_analyzer.py` - documented earnings analysis module.
  - `dist/predictor.py` - documented prediction module.
  - `dist/favorites_manager.py` - documented favorites persistence module.
  - `dist/get_data.py` - documented data access helper.
  - `dist/data/favorites.json` - persisted favorites and notes for `dist`.
- `README.md` - project documentation and usage instructions.

## Troubleshooting

- **No earnings data found**: the ticker may be invalid, delisted, or missing data from the provider.
- **Slow load times**: market/API responses can vary; retry after a few seconds.
- **Missing package errors**: install dependencies again in the active environment.
