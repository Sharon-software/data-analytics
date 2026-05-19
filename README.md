# 📊 Clear Analytics

A dark-themed interactive data analytics web app built with Python and Streamlit.
Upload your data, explore it visually, and download the results — no coding required.

---

## 🌐 Live Demo

[Click here to open app](https://data-analytics-ewshccrnni4fq4zzyeyzda.streamlit.app/)

---

## ✨ Features

- 📂 Upload CSV or Excel files
- 📋 Paste data directly from Excel or Google Sheets
- 🧪 Built-in sample dataset to explore
- 📈 Line, Bar, Pie and Radar interactive charts
- 🔢 Auto-generated KPI summary cards
- 🔍 Searchable data table
- ⬇️ Download your data as CSV
- 🎨 Deep teal gradient dark theme

---

## 🛠️ Built With

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web framework and UI |
| Pandas | Data loading and processing |
| Plotly | Interactive charts |
| OpenPyXL | Excel file support |

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Sharon-software/data-analytics.git
cd data-analytics
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure
data-analytics/
│
├── app.py                 ← Main Streamlit application
├── requirements.txt       ← Python dependencies
├── README.md              ← You are here
│
└── data/
└── sample_data.csv    ← Built-in sample dataset

---

## 📊 Supported Data Formats

| Format | Extension |
|---|---|
| Comma separated | .csv |
| Excel workbook | .xlsx |
| Excel legacy | .xls |
| Tab separated | Paste directly |

---

## 🔄 How to Update the App

Make your changes in VS Code, test locally, then push to GitHub.
Streamlit Cloud will automatically redeploy within 60 seconds.

```bash
git add .
git commit -m "Your update message"
git push
```

---

## 👩‍💻 Author

**Sharon**
GitHub: [@Sharon-software](https://github.com/Sharon-software)

---

## 📄 License

This project is open source and free to use.
