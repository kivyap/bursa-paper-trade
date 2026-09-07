import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

MYT = ZoneInfo("Asia/Kuala_Lumpur")

# =========================================================
# CONFIG
# =========================================================
STARTING_CAPITAL = 700_000.00
QUOTE_TTL_SECONDS = 900  # 15-minute delayed quotes are fine -> also used as cache lifetime
FEE_RATE = 0.002  # 0.2% brokerage/other cost, applied on both BUY and SELL trade value

# =========================================================
# 1. EMBEDDED BURSA STOCK POOL (160+ STOCKS)
# =========================================================
STOCK_POOL = [
    {'Ticker': '1155.KL', 'Name': 'MAYBANK'}, {'Ticker': '1295.KL', 'Name': 'PBBANK'},
    {'Ticker': '1023.KL', 'Name': 'CIMB'}, {'Ticker': '5347.KL', 'Name': 'TENAGA'},
    {'Ticker': '5225.KL', 'Name': 'IHH'}, {'Ticker': '8869.KL', 'Name': 'PMETAL'},
    {'Ticker': '5819.KL', 'Name': 'HLBANK'}, {'Ticker': '5183.KL', 'Name': 'PCHEM'},
    {'Ticker': '5285.KL', 'Name': 'SDG'}, {'Ticker': '5211.KL', 'Name': 'SUNWAY'},
    {'Ticker': '6742.KL', 'Name': 'YTLPOWR'}, {'Ticker': '3816.KL', 'Name': 'MISC'},
    {'Ticker': '1066.KL', 'Name': 'RHBBANK'}, {'Ticker': '6033.KL', 'Name': 'PETGAS'},
    {'Ticker': '6947.KL', 'Name': 'CDB'}, {'Ticker': '4863.KL', 'Name': 'TM'},
    {'Ticker': '6012.KL', 'Name': 'MAXIS'}, {'Ticker': '5326.KL', 'Name': '99SMART'},
    {'Ticker': '4677.KL', 'Name': 'YTL'}, {'Ticker': '1961.KL', 'Name': 'IOICORP'},
    {'Ticker': '5398.KL', 'Name': 'GAMUDA'}, {'Ticker': '5249.KL', 'Name': 'IOIPG'},
    {'Ticker': '4707.KL', 'Name': 'NESTLE'}, {'Ticker': '2445.KL', 'Name': 'KLK'},
    {'Ticker': '1082.KL', 'Name': 'HLFG'}, {'Ticker': '1015.KL', 'Name': 'AMBANK'},
    {'Ticker': '6888.KL', 'Name': 'AXIATA'}, {'Ticker': '5681.KL', 'Name': 'PETDAG'},
    {'Ticker': '5246.KL', 'Name': 'WPRTS'}, {'Ticker': '2089.KL', 'Name': 'UTDPLT'},
    {'Ticker': '4065.KL', 'Name': 'PPB'}, {'Ticker': '5296.KL', 'Name': 'MRDIY'},
    {'Ticker': '5878.KL', 'Name': 'KPJ'}, {'Ticker': '4197.KL', 'Name': 'SIME'},
    {'Ticker': '7084.KL', 'Name': 'QL'}, {'Ticker': '5227.KL', 'Name': 'IGBREIT'},
    {'Ticker': '7277.KL', 'Name': 'DIALOG'}, {'Ticker': '5031.KL', 'Name': 'TIMECOM'},
    {'Ticker': '4715.KL', 'Name': 'GENM'}, {'Ticker': '0097.KL', 'Name': 'VITROX'},
    {'Ticker': '3689.KL', 'Name': 'F&N'}, {'Ticker': '5288.KL', 'Name': 'SIMEPROP'},
    {'Ticker': '3794.KL', 'Name': 'MCEMENT'}, {'Ticker': '3182.KL', 'Name': 'GENTING'},
    {'Ticker': '5263.KL', 'Name': 'SUNCON'}, {'Ticker': '3867.KL', 'Name': 'MPI'},
    {'Ticker': '5176.KL', 'Name': 'SUNREIT'}, {'Ticker': '1899.KL', 'Name': 'BKAWAN'},
    {'Ticker': '2488.KL', 'Name': 'ABMB'}, {'Ticker': '3336.KL', 'Name': 'IJM'},
    {'Ticker': '0128.KL', 'Name': 'FRONTKN'}, {'Ticker': '5212.KL', 'Name': 'PAVREIT'},
    {'Ticker': '0166.KL', 'Name': 'INARI'}, {'Ticker': '5340.KL', 'Name': 'UMSINT'},
    {'Ticker': '5337.KL', 'Name': 'ECOSHOP'}, {'Ticker': '3034.KL', 'Name': 'HAPSENG'},
    {'Ticker': '1818.KL', 'Name': 'BURSA'}, {'Ticker': '8206.KL', 'Name': 'ECOWLD'},
    {'Ticker': '7113.KL', 'Name': 'TOPGLOV'}, {'Ticker': '3255.KL', 'Name': 'HEIM'},
    {'Ticker': '5209.KL', 'Name': 'GASMSIA'}, {'Ticker': '0208.KL', 'Name': 'GREATEC'},
    {'Ticker': '7293.KL', 'Name': 'YINSON'}, {'Ticker': '5005.KL', 'Name': 'UNISEM'},
    {'Ticker': '3301.KL', 'Name': 'HLIND'}, {'Ticker': '5185.KL', 'Name': 'AFFIN'},
    {'Ticker': '5292.KL', 'Name': 'UWC'}, {'Ticker': '5053.KL', 'Name': 'OSK'},
    {'Ticker': '8621.KL', 'Name': 'LPI'}, {'Ticker': '8664.KL', 'Name': 'SPSETIA'},
    {'Ticker': '4731.KL', 'Name': 'SCIENTX'}, {'Ticker': '1171.KL', 'Name': 'MBSB'},
    {'Ticker': '0151.KL', 'Name': 'KGB'}, {'Ticker': '5258.KL', 'Name': 'BIMB'},
    {'Ticker': '2836.KL', 'Name': 'CARLSBG'}, {'Ticker': '5200.KL', 'Name': 'UOADEV'},
    {'Ticker': '5309.KL', 'Name': 'ITMAX'}, {'Ticker': '5606.KL', 'Name': 'IGBB'},
    {'Ticker': '2291.KL', 'Name': 'GENP'}, {'Ticker': '5323.KL', 'Name': 'JPG'},
    {'Ticker': '5264.KL', 'Name': 'MALAKOF'}, {'Ticker': '5168.KL', 'Name': 'HARTA'},
    {'Ticker': '4006.KL', 'Name': 'ORIENT'}, {'Ticker': '5306.KL', 'Name': 'FFB'},
    {'Ticker': '5106.KL', 'Name': 'AXREIT'}, {'Ticker': '5126.KL', 'Name': 'SOP'},
    {'Ticker': '1163.KL', 'Name': 'ALLIANZ'}, {'Ticker': '7172.KL', 'Name': 'PMBTECH'},
    {'Ticker': '5038.KL', 'Name': 'KSL'}, {'Ticker': '5286.KL', 'Name': 'MI'},
    {'Ticker': '5148.KL', 'Name': 'UEMS'}, {'Ticker': '7153.KL', 'Name': 'KOSSAN'},
    {'Ticker': '3069.KL', 'Name': 'MFCB'}, {'Ticker': '7160.KL', 'Name': 'PENTA'},
    {'Ticker': '5139.KL', 'Name': 'AEONCR'}, {'Ticker': '9822.KL', 'Name': 'SAM'},
    {'Ticker': '6139.KL', 'Name': 'TAKAFUL'}, {'Ticker': '7161.KL', 'Name': 'KERJAYA'},
    {'Ticker': '5401.KL', 'Name': 'TROP'}, {'Ticker': '8583.KL', 'Name': 'MAHSING'},
    {'Ticker': '6633.KL', 'Name': 'LHI'}, {'Ticker': '5243.KL', 'Name': 'VELESTO'},
    {'Ticker': '5032.KL', 'Name': 'BIPORT'}, {'Ticker': '5027.KL', 'Name': 'KMLOONG'},
    {'Ticker': '5236.KL', 'Name': 'MATRIX'}, {'Ticker': '5272.KL', 'Name': 'RANHILL'},
    {'Ticker': '5012.KL', 'Name': 'TAANN'}, {'Ticker': '5000.KL', 'Name': 'HUMEIND'},
    {'Ticker': '5250.KL', 'Name': 'SEM'}, {'Ticker': '5102.KL', 'Name': 'GCB'},
    {'Ticker': '0225.KL', 'Name': 'SCGBHD'}, {'Ticker': '3565.KL', 'Name': 'WCEHB'},
    {'Ticker': '0338.KL', 'Name': 'KOPI'}, {'Ticker': '5141.KL', 'Name': 'DAYANG'},
    {'Ticker': '5180.KL', 'Name': 'CLMT'}, {'Ticker': '5210.KL', 'Name': 'ARMADA'},
    {'Ticker': '6459.KL', 'Name': 'MNRB'}, {'Ticker': '3026.KL', 'Name': 'DLADY'},
    {'Ticker': '7195.KL', 'Name': 'BNASTRA'}, {'Ticker': '5983.KL', 'Name': 'MBMR'},
    {'Ticker': '3417.KL', 'Name': 'E&O'}, {'Ticker': '5255.KL', 'Name': 'LFG'},
    {'Ticker': '5162.KL', 'Name': 'VSTECS'}, {'Ticker': '3859.KL', 'Name': 'MAGNUM'},
    {'Ticker': '4162.KL', 'Name': 'BAT'}, {'Ticker': '5109.KL', 'Name': 'YTLREIT'},
    {'Ticker': '1562.KL', 'Name': 'SPTOTO'}, {'Ticker': '5138.KL', 'Name': 'HSPLANT'},
    {'Ticker': '5313.KL', 'Name': 'RADIUM'}, {'Ticker': '9296.KL', 'Name': 'RCECAP'},
    {'Ticker': '5330.KL', 'Name': 'TMK'}, {'Ticker': '1651.KL', 'Name': 'MRCB'},
    {'Ticker': '7081.KL', 'Name': 'PHARMA'}, {'Ticker': '9059.KL', 'Name': 'TSH'},
    {'Ticker': '6599.KL', 'Name': 'AEON'}, {'Ticker': '7103.KL', 'Name': 'SPRITZER'},
    {'Ticker': '5301.KL', 'Name': 'CTOS'}, {'Ticker': '5338.KL', 'Name': 'PARADIGM'},
    {'Ticker': '5199.KL', 'Name': 'HIBICUS'}, {'Ticker': '0351.KL', 'Name': 'LSH'},
    {'Ticker': '5299.KL', 'Name': 'IGBCR'}, {'Ticker': '0245.KL', 'Name': 'MNHLDG'},
    {'Ticker': '7052.KL', 'Name': 'PADINI'}, {'Ticker': '7100.KL', 'Name': 'UCHITEC'},
    {'Ticker': '5321.KL', 'Name': 'KEYFIELD'}, {'Ticker': '0303.KL', 'Name': 'ALPHA'},
    {'Ticker': '5327.KL', 'Name': 'MEGAFB'}, {'Ticker': '0045.KL', 'Name': 'SSB8'},
    {'Ticker': '5335.KL', 'Name': 'HI'}, {'Ticker': '7148.KL', 'Name': 'DPHARMA'},
    {'Ticker': '7179.KL', 'Name': 'LAGENDA'}, {'Ticker': '0056.KL', 'Name': 'NCT'},
    {'Ticker': '2593.KL', 'Name': 'UMCCA'}, {'Ticker': '3042.KL', 'Name': 'PETRONM'},
    {'Ticker': '8907.KL', 'Name': 'EG'}, {'Ticker': '5248.KL', 'Name': 'BAUTO'},
    {'Ticker': '0233.KL', 'Name': 'PEKAT'}, {'Ticker': '0339.KL', 'Name': 'CBHB'},
    {'Ticker': '5271.KL', 'Name': 'PECCA'}, {'Ticker': '4383.KL', 'Name': 'JTIASA'},
    {'Ticker': '5135.KL', 'Name': 'SWKPLNT'}, {'Ticker': '6718.KL', 'Name': 'CRESNDO'},
    {'Ticker': '4758.KL', 'Name': 'ANCOMNY'}, {'Ticker': '6262.KL', 'Name': 'INNO'},
    {'Ticker': '5302.KL', 'Name': 'ATECH'}, {'Ticker': '1929.KL', 'Name': 'CHINTEK'},
    {'Ticker': '7233.KL', 'Name': 'DUFU'}, {'Ticker': '5293.KL', 'Name': 'AME'},
    {'Ticker': '5348.KL', 'Name': 'ORKIM'}, {'Ticker': '5352.KL', 'Name': 'MTTSL'},
    {'Ticker': '5351.KL', 'Name': 'EMPIRE'}, {'Ticker': '5357.KL', 'Name': 'SKYECHIP'},
    {'Ticker': '0375.KL', 'Name': 'THMY'}, {'Ticker': '5307.KL', 'Name': 'AMEREIT'},
    {'Ticker': '0168.KL', 'Name': 'BMGREEN'}, {'Ticker': '5356.KL', 'Name': 'STRATUS'},
]

SEARCH_MAP = {f"{item['Ticker']} - {item['Name']}": item['Ticker'] for item in STOCK_POOL}
NAME_MAP = {item['Ticker']: item['Name'] for item in STOCK_POOL}
SORTED_DISPLAY_LABELS = sorted(SEARCH_MAP.keys())


# =========================================================
# 2. DATABASE LAYER (Turso — hosted, SQLite-compatible, free tier)
# =========================================================
import turso_serverless

try:
    TURSO_URL = st.secrets["TURSO_DATABASE_URL"]
    TURSO_TOKEN = st.secrets["TURSO_AUTH_TOKEN"]
except Exception:
    st.error(
        "Turso credentials not found. Add TURSO_DATABASE_URL and TURSO_AUTH_TOKEN "
        "under Settings → Secrets in the Streamlit Cloud dashboard (or in a local "
        ".streamlit/secrets.toml for local testing)."
    )
    st.stop()


@st.cache_resource(show_spinner=False)
def get_conn():
    return turso_serverless.connect(TURSO_URL, auth_token=TURSO_TOKEN)


def init_db():
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            cash_balance REAL NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS holdings (
            ticker TEXT PRIMARY KEY,
            units INTEGER NOT NULL,
            avg_cost REAL NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ticker TEXT NOT NULL,
            action TEXT NOT NULL,
            price REAL NOT NULL,
            units INTEGER NOT NULL,
            amount REAL NOT NULL,
            fee REAL DEFAULT 0,
            realized_pnl REAL
        )
    ''')
    # Migration: older DBs created before the fee column existed
    try:
        conn.execute("ALTER TABLE trades ADD COLUMN fee REAL DEFAULT 0")
    except Exception:
        pass  # column already exists
    row = conn.execute("SELECT COUNT(*) FROM account").fetchone()
    if row[0] == 0:
        conn.execute("INSERT INTO account (id, cash_balance) VALUES (1, ?)", (STARTING_CAPITAL,))
    conn.commit()


def get_cash():
    conn = get_conn()
    row = conn.execute("SELECT cash_balance FROM account WHERE id = 1").fetchone()
    return float(row[0])


def set_cash(new_balance):
    conn = get_conn()
    conn.execute("UPDATE account SET cash_balance = ? WHERE id = 1", (new_balance,))
    conn.commit()


def get_holdings_df():
    conn = get_conn()
    rows = conn.execute("SELECT ticker, units, avg_cost FROM holdings").fetchall()
    return pd.DataFrame(rows, columns=["ticker", "units", "avg_cost"])


def get_holding(ticker):
    conn = get_conn()
    row = conn.execute(
        "SELECT ticker, units, avg_cost FROM holdings WHERE ticker = ?", (ticker,)
    ).fetchone()
    if row is None:
        return None
    return {"ticker": row[0], "units": row[1], "avg_cost": row[2]}


def upsert_holding(ticker, units, avg_cost):
    conn = get_conn()
    existing = conn.execute("SELECT ticker FROM holdings WHERE ticker = ?", (ticker,)).fetchone()
    if existing is None:
        conn.execute("INSERT INTO holdings (ticker, units, avg_cost) VALUES (?, ?, ?)", (ticker, units, avg_cost))
    else:
        conn.execute("UPDATE holdings SET units = ?, avg_cost = ? WHERE ticker = ?", (units, avg_cost, ticker))
    conn.commit()


def remove_holding(ticker):
    conn = get_conn()
    conn.execute("DELETE FROM holdings WHERE ticker = ?", (ticker,))
    conn.commit()


def log_trade(ticker, action, price, units, amount, fee=0.0, realized_pnl=None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO trades (timestamp, ticker, action, price, units, amount, fee, realized_pnl) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (datetime.now(MYT).strftime("%Y-%m-%d %H:%M:%S"), ticker, action, price, units, amount, fee, realized_pnl)
    )
    conn.commit()


def get_trades_df():
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, timestamp, ticker, action, price, units, amount, fee, realized_pnl "
        "FROM trades ORDER BY id DESC"
    ).fetchall()
    return pd.DataFrame(rows, columns=[
        "id", "timestamp", "ticker", "action", "price", "units", "amount", "fee", "realized_pnl"
    ])


def reset_portfolio():
    conn = get_conn()
    conn.execute("DELETE FROM holdings")
    conn.execute("DELETE FROM trades")
    conn.execute("UPDATE account SET cash_balance = ? WHERE id = 1", (STARTING_CAPITAL,))
    conn.commit()
    fetch_prices.clear()


init_db()


# =========================================================
# 3. TRADE EXECUTION (BUY / SELL move cash + holdings together)
# =========================================================
def execute_buy(ticker, price, units):
    gross = round(price * units, 2)
    fee = round(gross * FEE_RATE, 2)
    total_cost = round(gross + fee, 2)
    cash = get_cash()
    if total_cost > cash:
        return False, (f"Insufficient cash. Need MYR {total_cost:,.2f} "
                        f"(incl. MYR {fee:,.2f} fee), available MYR {cash:,.2f}.")

    existing = get_holding(ticker)
    if existing is not None:
        new_units = int(existing['units']) + units
        # fee is folded into cost basis, same as a real brokerage fill
        new_avg_cost = (existing['units'] * existing['avg_cost'] + total_cost) / new_units
    else:
        new_units = units
        new_avg_cost = total_cost / units

    upsert_holding(ticker, new_units, new_avg_cost)
    set_cash(cash - total_cost)
    log_trade(ticker, "BUY", price, units, gross, fee=fee)
    return True, (f"Bought {units:,} units of {ticker} @ MYR {price:,.3f} "
                  f"(gross MYR {gross:,.2f} + fee MYR {fee:,.2f} = MYR {total_cost:,.2f})")


def execute_sell(ticker, price, units):
    existing = get_holding(ticker)
    held = 0 if existing is None else int(existing['units'])
    if units > held:
        return False, f"Cannot sell {units:,} units — only {held:,} held."

    gross = round(price * units, 2)
    fee = round(gross * FEE_RATE, 2)
    net_proceeds = round(gross - fee, 2)
    realized_pnl = round(net_proceeds - (existing['avg_cost'] * units), 2)
    remaining_units = held - units

    if remaining_units == 0:
        remove_holding(ticker)
    else:
        upsert_holding(ticker, remaining_units, existing['avg_cost'])  # avg cost of remainder is unchanged

    set_cash(get_cash() + net_proceeds)
    log_trade(ticker, "SELL", price, units, gross, fee=fee, realized_pnl=realized_pnl)
    pnl_word = "profit" if realized_pnl >= 0 else "loss"
    return True, (f"Sold {units:,} units of {ticker} @ MYR {price:,.3f} "
                  f"(gross MYR {gross:,.2f} − fee MYR {fee:,.2f} = MYR {net_proceeds:,.2f} net) "
                  f"— realized {pnl_word} MYR {abs(realized_pnl):,.2f}")


# =========================================================
# 4. LIVE / DELAYED QUOTES (cached 15 min — one button refreshes all)
# =========================================================
@st.cache_data(ttl=QUOTE_TTL_SECONDS, show_spinner="Fetching latest quotes...")
def fetch_prices(tickers: tuple):
    prices = {}
    for t in tickers:
        try:
            hist = yf.Ticker(t).history(period="1d")
            prices[t] = float(hist["Close"].iloc[-1]) if not hist.empty else None
        except Exception:
            prices[t] = None
    return prices


@st.cache_data(ttl=QUOTE_TTL_SECONDS, show_spinner=False)
def fetch_single_price(ticker: str):
    try:
        hist = yf.Ticker(ticker).history(period="1d")
        return float(hist["Close"].iloc[-1]) if not hist.empty else None
    except Exception:
        return None


# =========================================================
# 5. STREAMLIT APP
# =========================================================
st.set_page_config(page_title="Bursa Paper Trading Tracker", layout="wide")
st.title("💼 Bursa Malaysia Paper Trading Tracker")
st.caption(
    f"Virtual capital: MYR {STARTING_CAPITAL:,.2f} · "
    f"Quotes may be delayed up to {QUOTE_TTL_SECONDS // 60} min · "
    f"Brokerage/other cost: {FEE_RATE * 100:.2f}% per trade (buy & sell)"
)

if "trade_msg" not in st.session_state:
    st.session_state.trade_msg = None
if "fetched_price" not in st.session_state:
    st.session_state.fetched_price = None

# --- Sidebar: place a trade ---
st.sidebar.header("📝 Place a Trade")

# Visible confirmation that the app is actually talking to Turso, not a local file
try:
    get_conn().execute("SELECT 1").fetchone()
    db_host = TURSO_URL.replace("libsql://", "").split(".turso.io")[0]
    st.sidebar.caption(f"🟢 Connected to Turso: `{db_host}`")
except Exception as e:
    st.sidebar.caption(f"🔴 Turso connection failed: {e}")

selected_display = st.sidebar.selectbox(
    "Search Stock (Code or Name):",
    options=SORTED_DISPLAY_LABELS,
    index=0,
    key="ticker_select",
)
selected_ticker = SEARCH_MAP[selected_display]
stock_name = NAME_MAP[selected_ticker]

current_holding = get_holding(selected_ticker)
held_units = 0 if current_holding is None else int(current_holding['units'])
if current_holding is not None:
    st.sidebar.caption(
        f"Currently holding: {held_units:,} units @ avg MYR {current_holding['avg_cost']:,.3f} "
        f"(fee-inclusive cost basis)"
    )
else:
    st.sidebar.caption("No current position in this stock.")

if st.sidebar.button("📡 Fetch current quote"):
    st.session_state.fetched_price = fetch_single_price(selected_ticker)
    if st.session_state.fetched_price is None:
        st.sidebar.warning("Could not fetch a quote — enter price manually.")

default_price = st.session_state.fetched_price if st.session_state.fetched_price else 5.00

trade_action = st.sidebar.radio("Action", ["BUY", "SELL"], horizontal=True)
price = st.sidebar.number_input(
    f"Price for {stock_name} (MYR):", min_value=0.001, value=float(default_price), step=0.005, format="%.3f"
)
units = st.sidebar.number_input("Units:", min_value=1, value=100, step=100)
st.sidebar.caption(f"= {units:,} units")

# --- Live order preview (gross value, fee, net cost/proceeds) before committing ---
gross_value = price * units
fee_value = gross_value * FEE_RATE

preview_lines = [f"**Gross Value:** MYR {gross_value:,.2f}", f"**Est. Fee ({FEE_RATE * 100:.2f}%):** MYR {fee_value:,.2f}"]
if trade_action == "BUY":
    total_cost_preview = gross_value + fee_value
    preview_lines.append(f"**Total Cost:** MYR {total_cost_preview:,.2f}")
    if total_cost_preview > get_cash():
        preview_lines.append(f":red[Exceeds available cash of MYR {get_cash():,.2f}]")
else:
    net_proceeds_preview = gross_value - fee_value
    preview_lines.append(f"**Net Proceeds:** MYR {net_proceeds_preview:,.2f}")
    if current_holding is not None:
        est_pnl = net_proceeds_preview - (current_holding['avg_cost'] * units)
        pnl_tag = "green" if est_pnl >= 0 else "red"
        preview_lines.append(f"**Est. Realized P&L:** :{pnl_tag}[MYR {est_pnl:,.2f}]")
    if units > held_units:
        preview_lines.append(f":red[Exceeds units held ({held_units:,})]")

st.sidebar.markdown("  \n".join(preview_lines))

if st.sidebar.button("✅ Execute Trade", type="primary"):
    if trade_action == "BUY":
        ok, msg = execute_buy(selected_ticker, price, units)
    else:
        ok, msg = execute_sell(selected_ticker, price, units)
    st.session_state.trade_msg = (ok, msg)
    st.rerun()

if st.session_state.trade_msg:
    ok, msg = st.session_state.trade_msg
    (st.sidebar.success if ok else st.sidebar.error)(msg)
    st.session_state.trade_msg = None

with st.sidebar.expander("⚠️ Danger Zone"):
    confirm_reset = st.checkbox("I understand this deletes all trades and holdings")
    if st.button("Reset Portfolio to MYR 700,000") and confirm_reset:
        reset_portfolio()
        st.sidebar.success("Portfolio reset.")
        st.rerun()

# --- Main: refresh + summary ---
top_left, top_right = st.columns([3, 1])
with top_right:
    if st.button("🔄 Refresh Quotes & Performance", use_container_width=True):
        fetch_prices.clear()
        st.rerun()

df_holdings = get_holdings_df()
df_trades = get_trades_df()
cash_balance = get_cash()
realized_total = df_trades["realized_pnl"].dropna().sum() if not df_trades.empty else 0.0

if not df_holdings.empty:
    unique_tickers = tuple(sorted(df_holdings["ticker"].unique()))
    live_prices = fetch_prices(unique_tickers)

    df_holdings["Stock Name"] = df_holdings["ticker"].map(NAME_MAP)
    df_holdings["Current Price (MYR)"] = df_holdings["ticker"].map(live_prices)
    df_holdings["Current Price (MYR)"] = df_holdings["Current Price (MYR)"].fillna(df_holdings["avg_cost"])
    df_holdings["Cost Basis (MYR)"] = df_holdings["avg_cost"] * df_holdings["units"]
    df_holdings["Market Value (MYR)"] = df_holdings["Current Price (MYR)"] * df_holdings["units"]
    df_holdings["Unrealized P&L (MYR)"] = df_holdings["Market Value (MYR)"] - df_holdings["Cost Basis (MYR)"]
    df_holdings["ROI (%)"] = (df_holdings["Unrealized P&L (MYR)"] / df_holdings["Cost Basis (MYR)"]) * 100

    market_value_total = df_holdings["Market Value (MYR)"].sum()
    unrealized_total = df_holdings["Unrealized P&L (MYR)"].sum()
else:
    market_value_total = 0.0
    unrealized_total = 0.0

total_portfolio_value = cash_balance + market_value_total
total_pnl = total_portfolio_value - STARTING_CAPITAL
total_roi = (total_pnl / STARTING_CAPITAL) * 100

st.subheader("Portfolio Performance")


def render_metric_card(col, label, value, delta=None, delta_color="#4caf50"):
    delta_html = f'<div style="font-size:0.8rem;color:{delta_color};margin-top:2px;">{delta}</div>' if delta else ""
    col.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:10px 12px;">
            <div style="font-size:0.78rem;color:#9aa0a6;margin-bottom:4px;">{label}</div>
            <div style="font-size:1.25rem;font-weight:600;line-height:1.25;
                        white-space:normal;word-break:break-word;">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


roi_color = "#4caf50" if total_roi >= 0 else "#e05252"
row1_col1, row1_col2 = st.columns(2)
render_metric_card(row1_col1, "Total Portfolio Value", f"MYR {total_portfolio_value:,.2f}",
                    f"{total_roi:+.2f}%", roi_color)
render_metric_card(row1_col2, "Cash Balance", f"MYR {cash_balance:,.2f}")

row2_col1, row2_col2 = st.columns(2)
render_metric_card(row2_col1, "Unrealized P&L", f"MYR {unrealized_total:,.2f}")
render_metric_card(row2_col2, "Realized P&L", f"MYR {realized_total:,.2f}")

st.divider()
st.subheader("Current Holdings")
if not df_holdings.empty:
    display_holdings = df_holdings[[
        "ticker", "Stock Name", "units", "avg_cost", "Current Price (MYR)",
        "Market Value (MYR)", "Unrealized P&L (MYR)", "ROI (%)"
    ]].rename(columns={"ticker": "Ticker", "units": "Units", "avg_cost": "Avg Cost (MYR)"}).copy()

    display_holdings["Units"] = display_holdings["Units"].map(lambda x: f"{int(x):,}")
    display_holdings["Avg Cost (MYR)"] = display_holdings["Avg Cost (MYR)"].map(lambda x: f"{x:,.3f}")
    display_holdings["Current Price (MYR)"] = display_holdings["Current Price (MYR)"].map(lambda x: f"{x:,.3f}")
    display_holdings["Market Value (MYR)"] = display_holdings["Market Value (MYR)"].map(lambda x: f"{x:,.2f}")
    display_holdings["Unrealized P&L (MYR)"] = display_holdings["Unrealized P&L (MYR)"].map(lambda x: f"{x:,.2f}")
    display_holdings["ROI (%)"] = display_holdings["ROI (%)"].map(lambda x: f"{x:,.2f}%")

    st.dataframe(display_holdings, use_container_width=True, hide_index=True)
else:
    st.info("No open positions yet. Use the sidebar to place your first BUY trade.")

st.divider()
st.subheader("Trade History")
if not df_trades.empty:
    trades_with_name = df_trades.copy()
    trades_with_name["stock_name"] = trades_with_name["ticker"].map(NAME_MAP)

    display_trades = trades_with_name[[
        "timestamp", "ticker", "stock_name", "action", "price", "units", "amount", "fee", "realized_pnl"
    ]].rename(columns={
        "timestamp": "Time (MYT)", "ticker": "Ticker", "stock_name": "Stock Name",
        "action": "Action", "price": "Price (MYR)",
        "units": "Units", "amount": "Gross Amount (MYR)", "fee": "Fee (MYR)",
        "realized_pnl": "Realized P&L (MYR)"
    }).copy()

    display_trades["Price (MYR)"] = display_trades["Price (MYR)"].map(lambda x: f"{x:,.3f}")
    display_trades["Units"] = display_trades["Units"].map(lambda x: f"{int(x):,}")
    display_trades["Gross Amount (MYR)"] = display_trades["Gross Amount (MYR)"].map(lambda x: f"{x:,.2f}")
    display_trades["Fee (MYR)"] = display_trades["Fee (MYR)"].map(lambda x: f"{x:,.2f}")
    display_trades["Realized P&L (MYR)"] = display_trades["Realized P&L (MYR)"].map(
        lambda x: "-" if pd.isna(x) else f"{x:,.2f}"
    )

    st.dataframe(display_trades, use_container_width=True, hide_index=True)
else:
    st.info("No trades recorded yet.")
