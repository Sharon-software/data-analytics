import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(
    page_title="Clear Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    /* ── Main background ── */
    .main {
        background: linear-gradient(160deg, #001a1a 0%, #003333 30%, #006666 65%, #009999 100%);
        min-height: 100vh;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        background: transparent;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000d0d 0%, #001a1a 40%, #003333 100%);
        border-right: 1px solid #00666688;
    }
    [data-testid="stSidebar"] * { color: #ccf2f2; }
    [data-testid="stSidebar"] .stRadio label { color: #99e6e6 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #00ffff !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #001a1acc;
        border-radius: 10px;
        padding: 4px;
        border: 1px solid #00666655;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 13px;
        color: #80d4d4;
        border-radius: 8px;
        padding: 6px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #006666, #009999) !important;
        color: #ffffff !important;
        border-radius: 8px;
    }

    /* ── KPI metric cards ── */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #001f1f99, #00404099);
        border: 1px solid #00999966;
        border-radius: 14px;
        padding: 20px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 24px #00333344;
    }
    div[data-testid="metric-container"] label { color: #80d4d4 !important; font-size: 12px !important; }
    div[data-testid="metric-container"] div   { color: #00ffff !important; font-size: 28px !important; }

    /* ── Download button ── */
    .stDownloadButton button {
        background: linear-gradient(135deg, #006666, #00aaaa);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
        letter-spacing: 0.4px;
    }
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #008080, #00cccc);
        box-shadow: 0 0 16px #00aaaa55;
    }

    /* ── Primary buttons ── */
    .stButton button {
        background: linear-gradient(135deg, #005555, #008080);
        color: #e0ffff;
        border: 1px solid #00999966;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #006666, #00aaaa);
        box-shadow: 0 0 14px #00888855;
        border-color: #00bbbb;
    }

    /* ── Text input / search ── */
    .stTextInput input {
        background: #001a1a99;
        border: 1px solid #00777766;
        color: #e0ffff;
        border-radius: 10px;
    }
    .stTextInput input:focus {
        border-color: #00cccc;
        box-shadow: 0 0 10px #00aaaa44;
    }
    .stTextInput input::placeholder { color: #4d9999; }

    /* ── Text area ── */
    .stTextArea textarea {
        background: #001a1a99;
        border: 1px solid #00666655;
        color: #ccf2f2;
        border-radius: 10px;
    }
    .stTextArea textarea:focus { border-color: #00cccc; }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: #001a1a88;
        border: 2px dashed #00888866;
        border-radius: 12px;
        padding: 8px;
    }
    [data-testid="stFileUploader"]:hover { border-color: #00bbbb; }

    /* ── Dataframe table ── */
    .stDataFrame {
        border: 1px solid #00666655;
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Alerts / info boxes ── */
    .stInfo {
        background: #001f1f99 !important;
        border: 1px solid #00888866 !important;
        border-radius: 10px !important;
        color: #b2f0f0 !important;
    }
    .stSuccess {
        background: #001a2699 !important;
        border: 1px solid #00bb8866 !important;
        border-radius: 10px !important;
    }
    .stWarning {
        background: #1a150099 !important;
        border: 1px solid #aa880066 !important;
        border-radius: 10px !important;
    }

    /* ── Typography ── */
    h1 { color: #00ffff !important; text-shadow: 0 0 20px #00aaaa66; }
    h2, h3 { color: #00e5e5 !important; }
    p, .stMarkdown p { color: #ccf2f2; }
    .stCaption { color: #669999 !important; }
    hr { border-color: #00555533 !important; }

    /* ── Selectbox ── */
    .stSelectbox div[data-baseweb="select"] {
        background: #001a1a99;
        border: 1px solid #00666655;
        border-radius: 10px;
        color: #ccf2f2;
    }

    /* ── Slider ── */
    .stSlider [data-baseweb="slider"] div { background: #00aaaa !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #001a1a; }
    ::-webkit-scrollbar-thumb { background: #006666; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #009999; }
</style>
""", unsafe_allow_html=True)


# ── Helper: parse pasted text ─────────────────────────────
def parse_pasted_text(text):
    text = text.strip()
    if not text:
        return None
    try:
        df = pd.read_csv(io.StringIO(text))
        if df.shape[1] > 1:
            return df
    except Exception:
        pass
    try:
        df = pd.read_csv(io.StringIO(text), sep="\t")
        if df.shape[1] > 1:
            return df
    except Exception:
        pass
    return None


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊Clear Analytics")
    st.markdown("---")
    st.markdown("### Load Your Data")

    input_method = st.radio(
        "Choose input method:",
        ["📂 Upload a File", "📋 Paste Text", "🧪 Sample Data"]
    )

    df = None

    if input_method == "📂 Upload a File":
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx", "xls"],
            help="Supports .csv, .xlsx, .xls"
        )
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    sheet_names = pd.ExcelFile(uploaded_file).sheet_names
                    if len(sheet_names) > 1:
                        sheet = st.selectbox("Select sheet", sheet_names)
                    else:
                        sheet = sheet_names[0]
                    df = pd.read_excel(uploaded_file, sheet_name=sheet)
                st.success(f"✅ Loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif input_method == "📋 Paste Text":
        st.markdown("Paste CSV or copy from **Excel / Google Sheets**:")
        pasted = st.text_area(
            "Paste data here",
            height=180,
            placeholder="Month,Revenue,Profit\nJan,45000,15000\nFeb,52000,20000"
        )
        if st.button("▶ Analyse", use_container_width=True):
            if pasted.strip():
                df = parse_pasted_text(pasted)
                if df is None:
                    st.error("Could not parse. Use comma or tab separated data with a header row.")
            else:
                st.warning("Please paste some data first.")

    else:
        st.info("Loads 12-month business sample data.")
        if st.button("Load Sample Data", use_container_width=True):
            df = pd.DataFrame({
                "Month":    ["Jan","Feb","Mar","Apr","May","Jun",
                             "Jul","Aug","Sep","Oct","Nov","Dec"],
                "Revenue":  [45000,52000,48000,61000,70000,66000,
                             75000,80000,72000,85000,90000,95000],
                "Expenses": [30000,32000,29000,35000,38000,36000,
                             40000,42000,39000,44000,47000,50000],
                "Profit":   [15000,20000,19000,26000,32000,30000,
                             35000,38000,33000,41000,43000,45000],
                "Users":    [1200,1450,1380,1700,2100,1950,
                             2300,2600,2400,2800,3100,3400],
            })

    if df is not None:
        st.markdown("---")
        st.markdown("### Dataset Info")
        num_cols = df.select_dtypes(include="number").columns.tolist()
        st.markdown(f"- **Rows:** {df.shape[0]}")
        st.markdown(f"- **Columns:** {df.shape[1]}")
        st.markdown(f"- **Numeric cols:** {len(num_cols)}")
        st.markdown("---")
        csv_out = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_out,
            file_name="datalens_export.csv",
            mime="text/csv",
            use_container_width=True
        )


# ── Main Area ─────────────────────────────────────────────
st.title("📊Clear Analytics")

if df is None:
    st.markdown("### Load your data from the sidebar to get started")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**📂 Upload a File**\n\nCSV or Excel files from your computer")
    with col2:
        st.info("**📋 Paste Text**\n\nCopy-paste from Excel or Google Sheets")
    with col3:
        st.info("**🧪 Sample Data**\n\nExplore with built-in business data")
    st.stop()

# ── Auto-detect columns ───────────────────────────────────
numeric_cols = df.select_dtypes(include="number").columns.tolist()
label_cols   = df.select_dtypes(exclude="number").columns.tolist()
x_col        = label_cols[0] if label_cols else df.columns[0]

st.caption(f"Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────
if numeric_cols:
    kpi_cols = st.columns(min(len(numeric_cols), 4))
    for i, col in enumerate(numeric_cols[:4]):
        with kpi_cols[i]:
            total = df[col].sum()
            avg   = df[col].mean()
            st.metric(
                label=col,
                value=f"{total:,.0f}",
                delta=f"avg {avg:,.0f} / row"
            )
    st.markdown("---")

# ── Charts ────────────────────────────────────────────────
cols_to_plot = numeric_cols

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Line Chart",
    "📊 Bar Chart",
    "🥧 Pie Chart",
    "🕸️ Radar Chart"
])

with tab1:
    if cols_to_plot:
        fig = px.line(
            df, x=x_col, y=cols_to_plot,
            markers=True, template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            height=420,
            legend_title="Column"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    if cols_to_plot:
        bar_col = st.selectbox("Column for bar chart", cols_to_plot, key="bar")
        fig = px.bar(
            df, x=x_col, y=bar_col,
            color=bar_col, template="plotly_dark",
            color_continuous_scale="Blues"
        )
        fig.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            height=420
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    if cols_to_plot:
        pie_col = st.selectbox("Column for pie chart", cols_to_plot, key="pie")
        fig = px.pie(
            df, names=x_col, values=pie_col,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(paper_bgcolor="#0d1117", height=420)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    if len(cols_to_plot) >= 2:
        radar_rows = st.slider(
            "Number of rows to compare", 2,
            min(10, len(df)), min(5, len(df))
        )
        fig = go.Figure()
        for i, row in df.head(radar_rows).iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row[c] for c in cols_to_plot],
                theta=cols_to_plot,
                fill='toself',
                name=str(row[x_col])
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            template="plotly_dark",
            paper_bgcolor="#0d1117",
            height=420
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns for a radar chart.")

st.markdown("---")

# ── Data Table ────────────────────────────────────────────
st.markdown("### 📋 Data Table")
search = st.text_input("🔍 Search table", placeholder="Type to filter rows...")
if search:
    mask = df.apply(lambda row: row.astype(str).str.contains(
        search, case=False).any(), axis=1)
    st.dataframe(df[mask], use_container_width=True, height=320)
else:
    st.dataframe(df, use_container_width=True, height=320)

st.markdown("---")
st.caption("DataLens · Built with Streamlit + Plotly")