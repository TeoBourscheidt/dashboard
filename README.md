# Python, Git, Linux for Finance - Dashboard Project

## Project Overview
This project is part of a quantitative research assignment at an asset management company.  
The goal is to build a **professional interactive dashboard** to:

- Retrieve and display financial data in real-time.
- Implement quantitative strategies and portfolio simulations.
- Provide clear metrics and visualizations for single assets and multi-asset portfolios.
- Run continuously on a Linux server with automated daily reporting.

The platform is developed in Python and deployed on a Linux VM. The project workflow simulates a professional environment using **Git/GitHub** for collaboration.

---

## Project Structure

### Modules
- **Quant A - Single Asset Analysis**
  - Focus on one main asset (e.g., ENGI, EUR/USD, gold).
  - Implements at least two backtesting strategies (e.g., buy-and-hold, momentum).
  - Displays metrics: max drawdown, Sharpe ratio, cumulative strategy value.
  - Interactive controls for strategy parameters and periodicity.
  - Optional: predictive model (ARIMA, regression, ML).

- **Quant B - Multi-Asset Portfolio**
  - Extends the dashboard to at least 3 assets simultaneously.
  - Portfolio simulation with custom weights and rebalancing.
  - Displays portfolio metrics: correlation matrix, volatility, returns, diversification effects.
  - Main chart shows multiple asset prices with cumulative portfolio value.

### Data
- Data is retrieved from **Yahoo Finance** (or other public APIs) every 5 minutes.
- Daily reports (volatility, open/close price, max drawdown) are automatically generated at 8 PM via **cron jobs**.

### Files
- `data/prices.csv` — historical prices for assets.
- `quant_a/` — single asset module code.
- `quant_b/` — multi-asset portfolio module code.
- `cron/` — scripts and configuration for automated reporting.
- `README.md` — this file.

---
## Web Interface

To access : https://dashboard-projet-cours-if.streamlit.app/

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TeoBourscheidt/dashboard.git
cd finance-dashboard

