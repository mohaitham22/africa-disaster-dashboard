import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Africa Disaster Data Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: white;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-left: 4px solid #2196F3;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌍 Africa Disaster Events Analysis Dashboard</h1>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load disaster data"""
    try:
        df = pd.read_csv('Book1.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file 'Book1.csv' not found!")
        return None

df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.image("https://img.icons8.com/clouds/200/000000/earthquake.png", width=150)
    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Select Analysis Section:",
        ["🏠 Overview", 
         "📁 Data Quality", 
         "📊 Temporal Analysis", 
         "🌍 Geographic Analysis",
         "💥 Disaster Types",
         "📈 Impact Analysis",
         "🔍 Advanced Analytics",
         "📥 Data Export"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Total Records:** {len(df):,}")
    st.sidebar.markdown(f"**Features:** {len(df.columns)}")
    st.sidebar.markdown(f"**Time Period:** {int(df['Year'].min())} - {int(df['Year'].max())}")
    
    # =================== OVERVIEW PAGE ===================
    if page == "🏠 Overview":
        st.header("📋 Dataset Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📝 Total Events", f"{len(df):,}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🌍 Countries", f"{df['Country'].nunique():,}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📊 Features", len(df.columns))
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📅 Years Covered", f"{int(df['Year'].max() - df['Year'].min())}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Dataset information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Dataset Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': [str(dtype) for dtype in df.dtypes.values],
                'Non-Null': df.count().values,
                'Null %': (df.isnull().sum() / len(df) * 100).round(2).values
            })
            st.dataframe(col_info, use_container_width=True, height=400)
        
        with col2:
            st.markdown("### 📊 Data Type Distribution")
            dtype_counts = df.dtypes.value_counts()
            
            # Convert dtype to string for proper display
            dtype_df = pd.DataFrame({
                'Data Type': [str(dtype) for dtype in dtype_counts.index],
                'Count': dtype_counts.values
            })
            
            fig = px.pie(dtype_df, values='Count', names='Data Type',
                        title='Distribution of Data Types',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 📈 Quick Statistics")
            st.write(f"**Numeric Columns:** {len(df.select_dtypes(include=[np.number]).columns)}")
            st.write(f"**Categorical Columns:** {len(df.select_dtypes(include=['object']).columns)}")
            st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # =================== DATA QUALITY PAGE ===================
    elif page == "📁 Data Quality":
        st.header("📁 Data Quality Analysis")
        
        # Missing values analysis
        st.markdown("### 🔍 Missing Values Analysis")
        
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum(),
            'Missing_Percentage': (df.isnull().sum() / len(df)) * 100,
            'Data_Type': [str(dtype) for dtype in df.dtypes]
        })
        
        missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values(
            'Missing_Percentage', ascending=False
        ).reset_index(drop=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if len(missing_data) > 0:
                st.markdown(f"**Columns with Missing Values:** {len(missing_data)} out of {len(df.columns)}")
                
                # Visualize missing data
                top_missing = missing_data.head(20)
                fig = px.bar(top_missing, 
                            x='Missing_Percentage', 
                            y='Column',
                            orientation='h',
                            title='Top 20 Columns with Missing Data',
                            labels={'Missing_Percentage': 'Missing Percentage (%)', 'Column': 'Column Name'},
                            color='Missing_Percentage',
                            color_continuous_scale='Reds')
                fig.update_layout(height=600, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No missing values found in the dataset!")
        
        with col2:
            st.markdown("### 📊 Missing Data Summary")
            if len(missing_data) > 0:
                st.dataframe(missing_data.head(20), use_container_width=True, height=600)
            
        # Completeness score
        st.markdown("### 📈 Data Completeness Score")
        completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Completeness", f"{completeness:.2f}%")
        with col2:
            st.metric("Total Missing Values", f"{df.isnull().sum().sum():,}")
        with col3:
            st.metric("Complete Rows", f"{df.dropna().shape[0]:,}")
    
    # =================== TEMPORAL ANALYSIS PAGE ===================
    elif page == "📊 Temporal Analysis":
        st.header("📊 Temporal Analysis")
        
        # Disaster trend over time
        st.markdown("### 📈 Disaster Events Over Time")
        
        yearly_counts = df['Year'].value_counts().sort_index().reset_index()
        yearly_counts.columns = ['Year', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='Year', nbins=50,
                             title='Distribution of Disaster Events',
                             labels={'Year': 'Year', 'count': 'Number of Events'},
                             color_discrete_sequence=['#667eea'])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(yearly_counts, x='Year', y='Count',
                         title='Disaster Frequency Trend',
                         labels={'Year': 'Year', 'Count': 'Number of Disasters'},
                         markers=True)
            fig.update_traces(line_color='#e74c3c', fill='tozeroy', fillcolor='rgba(231, 76, 60, 0.2)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Temporal statistics
        st.markdown("### 📊 Temporal Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Start Year", int(df['Year'].min()))
        with col2:
            st.metric("End Year", int(df['Year'].max()))
        with col3:
            st.metric("Peak Year", int(yearly_counts.loc[yearly_counts['Count'].idxmax(), 'Year']))
        with col4:
            st.metric("Max Events/Year", int(yearly_counts['Count'].max()))
        
        # Monthly analysis if available
        if 'Start Month' in df.columns:
            st.markdown("### 📅 Monthly Distribution")
            monthly_counts = df['Start Month'].value_counts().sort_index()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            fig = px.bar(x=monthly_counts.index, y=monthly_counts.values,
                        title='Disaster Events by Month',
                        labels={'x': 'Month', 'y': 'Number of Events'},
                        color=monthly_counts.values,
                        color_continuous_scale='Viridis')
            fig.update_xaxes(tickmode='array', 
                           tickvals=list(range(1, 13)),
                           ticktext=month_names)
            st.plotly_chart(fig, use_container_width=True)
    
    # =================== GEOGRAPHIC ANALYSIS PAGE ===================
    elif page == "🌍 Geographic Analysis":
        st.header("🌍 Geographic Distribution Analysis")
        
        # Continent analysis
        if 'Continent' in df.columns:
            st.markdown("### 🗺️ Disasters by Continent")
            
            continent_counts = df['Continent'].value_counts().reset_index()
            continent_counts.columns = ['Continent', 'Count']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(continent_counts, x='Continent', y='Count',
                           title='Disaster Events by Continent',
                           color='Count',
                           color_continuous_scale='Sunset')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(continent_counts, values='Count', names='Continent',
                           title='Percentage Distribution by Continent',
                           hole=0.4,
                           color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)
        
        # Country analysis
        st.markdown("### 🌏 Top Countries by Disaster Events")
        
        country_counts = df['Country'].value_counts().head(20).reset_index()
        country_counts.columns = ['Country', 'Count']
        
        fig = px.bar(country_counts, x='Count', y='Country',
                    orientation='h',
                    title='Top 20 Countries with Most Disaster Events',
                    color='Count',
                    color_continuous_scale='Reds')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Geographic statistics
        st.markdown("### 📊 Geographic Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Countries", df['Country'].nunique())
        with col2:
            if 'Continent' in df.columns:
                st.metric("Total Continents", df['Continent'].nunique())
        with col3:
            st.metric("Most Affected Country", country_counts.iloc[0]['Country'])
    
    # =================== DISASTER TYPES PAGE ===================
    elif page == "💥 Disaster Types":
        st.header("💥 Disaster Type Analysis")
        
        # Disaster type distribution
        if 'Disaster Type' in df.columns:
            st.markdown("### 📊 Distribution by Disaster Type")
            
            disaster_counts = df['Disaster Type'].value_counts().reset_index()
            disaster_counts.columns = ['Disaster Type', 'Count']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(disaster_counts, x='Disaster Type', y='Count',
                           title='Disaster Events by Type',
                           color='Count',
                           color_continuous_scale='Viridis')
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(disaster_counts, values='Count', names='Disaster Type',
                           title='Proportion of Disaster Types',
                           hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
        
        # Disaster subtype
        if 'Disaster Subtype' in df.columns:
            st.markdown("### 🔍 Top Disaster Subtypes")
            
            subtype_counts = df['Disaster Subtype'].value_counts().head(15).reset_index()
            subtype_counts.columns = ['Disaster Subtype', 'Count']
            
            fig = px.bar(subtype_counts, x='Count', y='Disaster Subtype',
                        orientation='h',
                        title='Top 15 Disaster Subtypes',
                        color='Count',
                        color_continuous_scale='Oranges')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Disaster type statistics
        st.markdown("### 📊 Disaster Type Statistics")
        if 'Disaster Type' in df.columns:
            st.dataframe(disaster_counts, use_container_width=True)
    
    # =================== IMPACT ANALYSIS PAGE ===================
    elif page == "📈 Impact Analysis":
        st.header("📈 Impact Analysis")
        
        # Impact metrics
        impact_cols = ['Total Deaths', 'No Injured', 'No Affected', 'Total Damages (\'000 US$)']
        available_impact_cols = [col for col in impact_cols if col in df.columns]
        
        if available_impact_cols:
            st.markdown("### 💔 Human and Economic Impact Overview")
            
            cols = st.columns(len(available_impact_cols))
            for i, col in enumerate(available_impact_cols):
                with cols[i]:
                    total = df[col].sum()
                    if 'Damages' in col:
                        st.metric(col.replace('(\'000 US$)', ''), f"${total/1e6:.1f}B")
                    else:
                        st.metric(col, f"{total:,.0f}")
            
            # Distribution plots
            st.markdown("### 📊 Impact Distribution (Log Scale)")
            
            fig = make_subplots(rows=2, cols=2,
                              subplot_titles=[f'{col} Distribution' for col in available_impact_cols[:4]])
            
            colors = ['crimson', 'orange', 'purple', 'green']
            
            for idx, col in enumerate(available_impact_cols[:4]):
                row = (idx // 2) + 1
                col_pos = (idx % 2) + 1
                
                data = df[col].dropna()
                data_log = np.log10(data[data > 0] + 1)
                
                fig.add_trace(
                    go.Histogram(x=data_log, nbinsx=50, 
                               marker_color=colors[idx],
                               opacity=0.7,
                               name=col),
                    row=row, col=col_pos
                )
                
                fig.update_xaxes(title_text=f"Log10({col} + 1)", row=row, col=col_pos)
                fig.update_yaxes(title_text="Frequency", row=row, col=col_pos)
            
            fig.update_layout(height=700, showlegend=False, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics table
            st.markdown("### 📊 Impact Statistics")
            st.dataframe(df[available_impact_cols].describe().T, use_container_width=True)
            
            # Top disasters by impact
            st.markdown("### 🔝 Most Devastating Disasters")
            
            impact_metric = st.selectbox("Select impact metric:", available_impact_cols)
            
            top_disasters = df.nlargest(10, impact_metric)[['Year', 'Country', 'Disaster Type', impact_metric]].reset_index(drop=True)
            st.dataframe(top_disasters, use_container_width=True)
    
    # =================== ADVANCED ANALYTICS PAGE ===================
    elif page == "🔍 Advanced Analytics":
        st.header("🔍 Advanced Analytics")
        
        # Correlation analysis
        st.markdown("### 📊 Correlation Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 1:
            # Select columns for correlation
            selected_cols = st.multiselect(
                "Select columns for correlation analysis:",
                numeric_cols,
                default=numeric_cols[:10] if len(numeric_cols) > 10 else numeric_cols
            )
            
            if len(selected_cols) > 1:
                corr_matrix = df[selected_cols].corr()
                
                fig = px.imshow(corr_matrix,
                              text_auto='.2f',
                              aspect='auto',
                              title='Correlation Heatmap',
                              color_continuous_scale='RdBu_r',
                              zmin=-1, zmax=1)
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                # Strong correlations
                st.markdown("### 🔗 Strong Correlations (|r| > 0.5)")
                strong_corr = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        if abs(corr_matrix.iloc[i, j]) > 0.5:
                            strong_corr.append({
                                'Feature 1': corr_matrix.columns[i],
                                'Feature 2': corr_matrix.columns[j],
                                'Correlation': corr_matrix.iloc[i, j]
                            })
                
                if strong_corr:
                    st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
                else:
                    st.info("No strong correlations found")
        
        # Data filtering and exploration
        st.markdown("### 🎯 Custom Data Filtering")
        
        with st.expander("📊 Apply Filters", expanded=True):
            filter_cols = {}
            
            # Year range filter
            if 'Year' in df.columns:
                year_range = st.slider("Year Range", 
                                      int(df['Year'].min()), 
                                      int(df['Year'].max()),
                                      (int(df['Year'].min()), int(df['Year'].max())))
                filter_cols['Year'] = year_range
            
            # Categorical filters
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            for col in categorical_cols[:3]:
                unique_vals = df[col].dropna().unique().tolist()[:20]
                if len(unique_vals) > 0:
                    selected = st.multiselect(f"Select {col}", unique_vals, default=unique_vals)
                    filter_cols[col] = selected
        
        # Apply filters
        filtered_df = df.copy()
        
        if 'Year' in filter_cols:
            filtered_df = filtered_df[(filtered_df['Year'] >= filter_cols['Year'][0]) & 
                                     (filtered_df['Year'] <= filter_cols['Year'][1])]
        
        for col, vals in filter_cols.items():
            if col != 'Year' and isinstance(vals, list):
                filtered_df = filtered_df[filtered_df[col].isin(vals)]
        
        st.success(f"✅ Filtered dataset: **{len(filtered_df):,}** rows (from {len(df):,})")
        st.dataframe(filtered_df.head(20), use_container_width=True)
    
    # =================== DATA EXPORT PAGE ===================
    elif page == "📥 Data Export":
        st.header("📥 Data Export & Download")
        
        st.markdown("### 💾 Export Options")
        
        # Export full dataset
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Export Full Dataset")
            csv_full = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Dataset (CSV)",
                data=csv_full,
                file_name="disaster_data_full.csv",
                mime="text/csv"
            )
        
        with col2:
            st.markdown("#### 📊 Export Summary Statistics")
            summary = df.describe()
            csv_summary = summary.to_csv()
            st.download_button(
                label="📥 Download Summary Statistics (CSV)",
                data=csv_summary,
                file_name="disaster_data_summary.csv",
                mime="text/csv"
            )
        
        # Custom export
        st.markdown("### 🎯 Custom Export")
        
        export_cols = st.multiselect(
            "Select columns to export:",
            df.columns.tolist(),
            default=df.columns.tolist()[:5]
        )
        
        if export_cols:
            export_df = df[export_cols]
            csv_custom = export_df.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {len(export_cols)} Selected Columns (CSV)",
                data=csv_custom,
                file_name="disaster_data_custom.csv",
                mime="text/csv"
            )
            
            st.markdown("#### Preview")
            st.dataframe(export_df.head(10), use_container_width=True)

else:
    # Error state
    st.error("❌ Unable to load data file 'Book1.csv'. Please ensure the file exists in the same directory as this app.")
    st.info("📁 Expected file: Book1.csv")
    
    # File upload option
    st.markdown("### 📤 Upload Your Data File")
    uploaded_file = st.file_uploader("Upload disaster dataset (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>Africa Disaster Events Analysis Dashboard</strong></p>
        <p>Created with ❤️ using Streamlit | © 2026</p>
        <p>Data Source: Africa Disaster Database Analysis</p>
        <p>📧 Share this dashboard with your friends!</p>
    </div>
""", unsafe_allow_html=True)
