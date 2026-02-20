# 🌍 Africa Disaster Events Analysis Dashboard

An interactive Streamlit dashboard for comprehensive exploratory data analysis of Africa disaster events.

## 📋 Project Description

This dashboard provides a comprehensive analysis of historical disaster events across Africa, including:

- Temporal patterns and trends
- Geographic distribution across African countries and regions
- Disaster type analysis
- Human and economic impact assessment
- Advanced statistical analytics

## ✨ Features

- **📊 Overview**: Dataset summary and basic statistics
- **📁 Data Quality**: Missing values analysis and data completeness
- **📈 Temporal Analysis**: Time-series trends and seasonal patterns
- **🌍 Geographic Analysis**: Continental and country-level distribution
- **💥 Disaster Types**: Categorization and frequency analysis
- **📊 Impact Analysis**: Deaths, injuries, affected population, and economic damages
- **🔍 Advanced Analytics**: Correlation analysis and custom filtering
- **📥 Data Export**: Download full or filtered datasets

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this project**

```bash
cd "Graduation project"
```

2. **Install required packages**

```bash
pip install -r requirements.txt
```

3. **Ensure data file exists**
   Make sure `Book1.csv` is in the same directory as `app.py`

## 💻 Usage

### Run Locally

```bash
streamlit run app.py
```

The app will automatically load the `Book1.csv` file and open in your default browser at `http://localhost:8501`

### Alternative: Using PowerShell

```powershell
python -m streamlit run app.py
```

## 📊 Data Requirements

The dashboard expects a CSV file named `Book1.csv` with the following columns (minimum):

- Year
- Country
- Continent
- Disaster Type
- Disaster Subtype
- Total Deaths
- No Injured
- No Affected
- Total Damages ('000 US$)
- Start Year
- Start Month

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit - Disaster Analysis Dashboard"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud**

- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your repository
- Set main file path: `app.py`
- Click "Deploy"

### Deploy to Other Platforms

**Heroku:**

1. Create `Procfile`:

```
web: streamlit run app.py --server.port=$PORT
```

2. Deploy:

```bash
heroku create your-app-name
git push heroku main
```

**Railway:**

1. Connect your GitHub repository
2. Set start command: `streamlit run app.py`

## 📁 Project Structure

```
Graduation project/
│
├── app.py                              # Main Streamlit application
├── Book1.csv                           # Disaster dataset
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
├── Disaster_EDA_Analysis.ipynb        # Original Jupyter notebook
└── ...
```

## 🛠️ Technologies Used

- **Streamlit**: Interactive web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Matplotlib & Seaborn**: Statistical data visualization
- **SciPy**: Scientific computing

## 📈 Dashboard Sections

### 1. Overview

- Dataset preview and basic statistics
- Data type distribution
- Quick metrics

### 2. Data Quality

- Missing values analysis
- Data completeness score
- Quality metrics

### 3. Temporal Analysis

- Disaster trends over time
- Monthly and yearly patterns
- Peak periods identification

### 4. Geographic Analysis

- Continental distribution
- Country-level analysis
- Top affected regions

### 5. Disaster Types

- Type and subtype categorization
- Frequency distribution
- Comparative analysis

### 6. Impact Analysis

- Human impact (deaths, injuries, affected)
- Economic damages
- Top devastating events

### 7. Advanced Analytics

- Correlation analysis
- Custom data filtering
- Interactive exploration

### 8. Data Export

- Download full dataset
- Export summary statistics
- Custom column selection

## 🎯 Use Cases

- **Disaster Risk Management**: Identify high-risk regions and periods
- **Policy Planning**: Data-driven decision making for disaster preparedness
- **Research**: Academic and scientific analysis of disaster patterns
- **Education**: Teaching tool for data analysis and visualization
- **Public Awareness**: Communicating disaster trends to stakeholders

## 🤝 Contributing

This project was created as part of a graduation project. Feel free to:

- Report issues
- Suggest improvements
- Fork and enhance

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

**Graduation Project 2026**

## 🙏 Acknowledgments

- Data Source: EM-DAT International Disaster Database
- Built with Streamlit
- Visualization powered by Plotly

## 📞 Support

For questions or issues, please refer to the Streamlit documentation or create an issue in the repository.

---

**Last Updated**: February 20, 2026

**Status**: ✅ Production Ready
