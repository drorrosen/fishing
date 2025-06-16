import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import folium
from streamlit_folium import st_folium
import os

# Page configuration
st.set_page_config(
    page_title="Fishing Data Analytics Dashboard",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOGIN CREDENTIALS
VALID_CREDENTIALS = {
    "captain": "fishing2025",
    "admin": "moana123",
    "demo": "demo123"
}

def show_login_page():
    """Display the login page"""
    
    # Hide sidebar and other elements
    st.markdown("""
    <style>
        .css-1d391kg {display: none;}
        .css-18e3th9 {display: none;}
        .css-hby737 {display: none;}
        .css-17eq0hr {display: none;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        .css-1rs6os {display: none;}
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login header
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #1f77b4; font-size: 3rem; margin-bottom: 0;">🎣</h1>
            <h2 style="color: #2c3e50; margin-top: 0;">Professional Fishing Analytics</h2>
            <p style="color: #6c757d; font-size: 1.1rem;">MOANA Sensor Data & Longline Configuration Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login container
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 2rem;">
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔐 Login to Dashboard")
        
        # Login form
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            
            col_login1, col_login2, col_login3 = st.columns([1, 2, 1])
            with col_login2:
                login_clicked = st.form_submit_button(
                    "🚢 Access Dashboard",
                    use_container_width=True
                )
        
        if login_clicked:
            if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success(f"Welcome aboard, {username}! 🎣")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
                
        st.markdown("</div>", unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    return st.session_state.authenticated

def show_logout_option():
    """Show logout option in sidebar"""
    if st.session_state.get("authenticated", False):
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👤 Logged in as:** {st.session_state.get('username', 'User')}")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

# Custom CSS for better styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    :root {
        --ocean-blue-dark: #0a2d5c;
        --ocean-blue-primary: #1f77b4;
        --ocean-blue-light: #6baed6;
        --ocean-teal: #17a2b8;
        --ocean-sand: #f8f9fa;
        --ocean-white: #ffffff;
        --ocean-gray: #6c757d;
        --ocean-success: #28a745;
        --ocean-danger: #dc3545;
    }

    /* Global styling */
    body {
        font-family: 'Inter', sans-serif;
        color: var(--ocean-blue-dark);
    }

    .main {
        background-color: var(--ocean-sand);
        padding: 2rem;
    }

    /* Header styling */
    .header-container {
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, var(--ocean-blue-dark) 0%, var(--ocean-blue-primary) 100%);
        color: var(--ocean-white);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-container img {
        height: 60px;
        margin-right: 20px;
    }
    .header-container h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        color: var(--ocean-white) !important;
    }
    .header-container p {
        font-size: 1.1rem;
        margin: 0;
        opacity: 0.9;
    }

    /* Metric cards styling */
    .metric-card {
        background-color: var(--ocean-white);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid var(--ocean-blue-light);
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--ocean-gray);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--ocean-blue-dark);
    }

    /* Chart container styling */
    .chart-container {
        background-color: var(--ocean-white);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .chart-container h2, .chart-container h3 {
        color: var(--ocean-blue-dark);
        font-weight: 700;
        margin-top: 0;
    }
    
    /* Specific Streamlit components */
    .stButton>button {
        border-radius: 8px;
        background-color: var(--ocean-blue-primary);
        color: var(--ocean-white);
        border: none;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: var(--ocean-blue-dark);
    }
    
    .stDownloadButton>button {
        border-radius: 8px;
        background-color: var(--ocean-teal);
        color: var(--ocean-white);
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
    }
    
    .stDownloadButton>button:hover {
        background-color: #138496;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--ocean-blue-dark);
    }
    .streamlit-expander {
        border-radius: 15px !important;
        border: 1px solid #dee2e6 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_moana_data(file_source):
    """Load and process MOANA sensor data from a given file source."""
    try:
        # Read MOANA data - skip the metadata rows (first 11 rows)
        df = pd.read_csv(file_source, skiprows=11)
        
        # Clean column names
        df.columns = ['Index', 'DATETIME', 'LATITUDE', 'LONGITUDE', 'TEMPERATURE', 'DEPTH', 'QC_FLAG']
        
        # Convert datetime column
        df['DATETIME'] = pd.to_datetime(df['DATETIME'])
        
        return df
    except Exception as e:
        st.error(f"An error occurred while reading the data file: {e}")
        st.info("Please ensure the uploaded file has the correct MOANA CSV structure (11 metadata rows to skip).")
        return None

def create_depth_temperature_profile(df):
    """Create professional depth vs temperature profile with advanced features"""
    
    try:
        # Sort data by depth for proper plotting
        df_sorted = df.sort_values('DEPTH').reset_index(drop=True)
        
        # Calculate temperature gradient for thermocline detection
        df_sorted['temp_gradient'] = df_sorted['TEMPERATURE'].diff() / df_sorted['DEPTH'].diff()
        
        # Create the main figure
        fig = go.Figure()
    
        # Add temperature profile with beautiful gradient colors
        fig.add_trace(go.Scatter(
            x=df_sorted['TEMPERATURE'],
            y=df_sorted['DEPTH'],
            mode='lines+markers',
            line=dict(color='rgba(0,0,0,0.8)', width=3),
            marker=dict(
                color=df_sorted['TEMPERATURE'],
                colorscale='RdYlBu_r',  # Red-Yellow-Blue reversed (warm to cold)
                size=6,
                colorbar=dict(
                    title=dict(text="Temperature (°C)", font=dict(size=14)),
                    thickness=20,
                    len=0.7,
                    x=1.02
                ),
                cmin=df_sorted['TEMPERATURE'].min(),
                cmax=df_sorted['TEMPERATURE'].max(),
                showscale=True,
                line=dict(color='white', width=1)
            ),
            name='Temperature Profile',
            hovertemplate='<b>Depth:</b> %{y:.1f} m<br><b>Temperature:</b> %{x:.2f}°C<br><extra></extra>'
        ))
        
        # Detect and highlight thermocline
        thermocline_depth = calculate_thermocline(df_sorted)
        if thermocline_depth:
            # Find the row index with depth closest to thermocline depth
            closest_idx = (df_sorted['DEPTH'] - thermocline_depth).abs().idxmin()
            thermocline_temp = df_sorted.loc[closest_idx, 'TEMPERATURE']
            
            # Add thermocline marker
            fig.add_trace(go.Scatter(
                x=[thermocline_temp],
                y=[thermocline_depth],
                mode='markers',
                marker=dict(
                    color='red',
                    size=15,
                    symbol='diamond',
                    line=dict(color='white', width=2)
                ),
                name='Thermocline',
                hovertemplate='<b>Thermocline</b><br>Depth: %{y:.1f} m<br>Temperature: %{x:.2f}°C<extra></extra>'
            ))
            
            # Add thermocline line
            fig.add_hline(
                y=thermocline_depth,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Thermocline: {thermocline_depth:.1f}m",
                annotation_position="top right"
            )
        
        # Add depth zones (typical oceanographic zones)
        fig.add_hrect(
            y0=0, y1=50,
            fillcolor="rgba(255,255,0,0.1)",
            layer="below",
            line_width=0,
            annotation_text="Epipelagic Zone",
            annotation_position="top left"
        )
        
        fig.add_hrect(
            y0=50, y1=200,
            fillcolor="rgba(0,255,255,0.1)",
            layer="below",
            line_width=0,
            annotation_text="Mesopelagic Zone",
            annotation_position="top left"
        )
        
        if df_sorted['DEPTH'].max() > 200:
            fig.add_hrect(
                y0=200, y1=df_sorted['DEPTH'].max(),
                fillcolor="rgba(0,0,255,0.1)",
                layer="below",
                line_width=0,
                annotation_text="Bathypelagic Zone",
                annotation_position="top left"
            )
        
        # Update layout with professional styling
        fig.update_layout(
            title=dict(
                text="<b>Mangōpare Sensor Measurements</b><br><sub>Temperature vs Depth Profile</sub>",
                x=0.5,
                font=dict(size=18, color='#2c3e50')
            ),
            xaxis=dict(
                title=dict(text="Temperature (°C)", font=dict(size=14, color='#2c3e50')),
                range=[df_sorted['TEMPERATURE'].min()-1, df_sorted['TEMPERATURE'].max()+1],
                gridcolor='rgba(128,128,128,0.3)',
                showgrid=True,
                zeroline=True,
                zerolinecolor='rgba(128,128,128,0.5)',
                tickfont=dict(size=12, color='#2c3e50')
            ),
            yaxis=dict(
                title=dict(text="Depth (m)", font=dict(size=14, color='#2c3e50')),
                autorange='reversed',
                range=[df_sorted['DEPTH'].max()+10, -5],
                gridcolor='rgba(128,128,128,0.3)',
                showgrid=True,
                zeroline=True,
                zerolinecolor='rgba(128,128,128,0.5)',
                tickfont=dict(size=12, color='#2c3e50')
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            width=900,
            height=700,
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(128,128,128,0.5)',
                borderwidth=1
            ),
            hovermode='closest'
        )
        
        return fig
    
    except Exception as e:
        # If there's an error creating the advanced plot, return a simple one
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['TEMPERATURE'],
            y=df['DEPTH'],
            mode='lines+markers',
            name='Temperature Profile',
            line=dict(color='blue', width=2),
            marker=dict(size=4, color='red'),
            hovertemplate='<b>Depth:</b> %{y:.1f}m<br><b>Temperature:</b> %{x:.2f}°C<extra></extra>'
        ))
        
        fig.update_layout(
            title="Temperature vs Depth Profile (Simplified)",
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)",
            yaxis=dict(autorange='reversed'),
            width=800,
            height=600,
            plot_bgcolor='white'
        )
        
        return fig

def create_time_series_plots(df):
    """Create enhanced time series plots for temperature and depth"""
    
    try:
        # Sort by time
        df_sorted = df.sort_values('DATETIME').reset_index(drop=True)
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Temperature Profile Over Time', 'Depth Profile Over Time'),
            vertical_spacing=0.15,
            shared_xaxes=True
        )
        
        # Add temperature trace with gradient fill
        fig.add_trace(go.Scatter(
            x=df_sorted['DATETIME'],
            y=df_sorted['TEMPERATURE'],
            mode='lines',
            name='Temperature',
            line=dict(color='#e74c3c', width=3),
            fill='tonexty',
            fillcolor='rgba(231, 76, 60, 0.2)',
            hovertemplate='<b>Time:</b> %{x}<br><b>Temperature:</b> %{y:.2f}°C<extra></extra>'
        ), row=1, col=1)
        
        # Add depth trace with inverted fill
        fig.add_trace(go.Scatter(
            x=df_sorted['DATETIME'],
            y=df_sorted['DEPTH'],
            mode='lines',
            name='Depth',
            line=dict(color='#3498db', width=3),
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.2)',
            hovertemplate='<b>Time:</b> %{x}<br><b>Depth:</b> %{y:.1f}m<extra></extra>'
        ), row=2, col=1)
        
        # Add depth zones as background
        max_depth = df_sorted['DEPTH'].max()
        if max_depth > 50:
            fig.add_hline(y=50, line_dash="dot", line_color="orange", 
                         annotation_text="Epipelagic Zone", row=2, col=1)
        if max_depth > 200:
            fig.add_hline(y=200, line_dash="dot", line_color="purple", 
                         annotation_text="Mesopelagic Zone", row=2, col=1)
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="<b>Sensor Data Time Series Analysis</b>",
                x=0.5,
                font=dict(size=18, color='#2c3e50')
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified',
            width=1000,
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(
            title_text="Time (UTC)",
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            row=2, col=1
        )
        
        fig.update_yaxes(
            title_text="Temperature (°C)",
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            row=1, col=1
        )
        
        fig.update_yaxes(
            title_text="Depth (m)",
            autorange='reversed',
            gridcolor='rgba(128,128,128,0.3)',
            showgrid=True,
            row=2, col=1
        )
        
        return fig
    
    except Exception as e:
        # Return simple plot if error occurs
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['DATETIME'],
            y=df['TEMPERATURE'],
            mode='lines',
            name='Temperature',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title="Temperature vs Time (Simplified)",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            width=800,
            height=400
        )
        
        return fig

def calculate_thermocline(df, temp_gradient_threshold=0.1):
    """Advanced thermocline depth calculation using multiple methods"""
    
    try:
        # Sort and clean data
        df_sorted = df.sort_values('DEPTH').reset_index(drop=True)
        
        if len(df_sorted) < 3:
            return None
        
        # Calculate temperature gradient using rolling window for smoothing
        df_sorted['depth_diff'] = df_sorted['DEPTH'].diff()
        df_sorted['temp_diff'] = df_sorted['TEMPERATURE'].diff()
        df_sorted['temp_gradient'] = df_sorted['temp_diff'] / df_sorted['depth_diff']
        
        # Apply smoothing with rolling mean
        df_sorted['temp_gradient_smooth'] = df_sorted['temp_gradient'].rolling(window=3, center=True).mean()
        
        # Find thermocline candidates (negative gradient indicates cooling with depth)
        # Filter to typical thermocline depth range (20-200m)
        thermocline_zone = df_sorted[
            (df_sorted['DEPTH'] >= 20) & 
            (df_sorted['DEPTH'] <= 200) &
            (df_sorted['temp_gradient_smooth'] < -temp_gradient_threshold)
        ]
        
        if thermocline_zone.empty:
            # If no strong gradient found, look for maximum gradient in any depth
            valid_gradients = df_sorted[df_sorted['temp_gradient_smooth'].notna()]
            if not valid_gradients.empty:
                max_gradient_idx = valid_gradients['temp_gradient_smooth'].abs().idxmax()
                return df_sorted.loc[max_gradient_idx, 'DEPTH']
            return None
        
        # Find the depth with maximum temperature gradient (most negative)
        max_gradient_idx = thermocline_zone['temp_gradient_smooth'].idxmin()
        thermocline_depth = df_sorted.loc[max_gradient_idx, 'DEPTH']
        
        return thermocline_depth
    
    except Exception as e:
        return None

def calculate_advanced_statistics(df):
    """Calculate advanced oceanographic statistics with error handling"""
    
    try:
        df_sorted = df.sort_values('DEPTH').reset_index(drop=True)
        
        # Safe calculations with fallbacks
        surface_temp = df_sorted[df_sorted['DEPTH'] <= 5]['TEMPERATURE'].mean() if len(df_sorted[df_sorted['DEPTH'] <= 5]) > 0 else df_sorted['TEMPERATURE'].iloc[0]
        bottom_temp = df_sorted[df_sorted['DEPTH'] >= df_sorted['DEPTH'].max() * 0.9]['TEMPERATURE'].mean() if len(df_sorted) > 0 else 0
        temp_range = df_sorted['TEMPERATURE'].max() - df_sorted['TEMPERATURE'].min() if len(df_sorted) > 0 else 0
        depth_range = df_sorted['DEPTH'].max() - df_sorted['DEPTH'].min() if len(df_sorted) > 0 else 0
        
        stats_dict = {
            'surface_temp': surface_temp,
            'bottom_temp': bottom_temp,
            'temp_range': temp_range,
            'depth_range': depth_range,
        }
        
        return stats_dict
        
    except Exception as e:
        # Return default values if calculation fails
        return {
            'surface_temp': 0,
            'bottom_temp': 0,
            'temp_range': 0,
            'depth_range': 0,
        }

def create_time_depth_profile(df):
    """Create the crucial time vs depth profile showing fishing gear deployment timeline"""
    
    try:
        # Sort data by time for proper plotting
        df_sorted = df.sort_values('DATETIME').reset_index(drop=True)
        
        # Handle empty or all-NaN data gracefully
        if df_sorted.empty:
            return go.Figure(layout=dict(title="No data to display for the selected time range."))

        max_depth = df_sorted['DEPTH'].max()
        if pd.isna(max_depth):
             max_depth = 0

        max_depth_time_series = df_sorted[df_sorted['DEPTH'] == max_depth]['DATETIME']
        max_depth_time = max_depth_time_series.iloc[0] if not max_depth_time_series.empty else df_sorted['DATETIME'].iloc[0]

        # Create the main figure
        fig = go.Figure()
        
        # Add main depth profile line with temperature color coding
        fig.add_trace(go.Scatter(
            x=df_sorted['DATETIME'],
            y=df_sorted['DEPTH'],
            mode='lines+markers',
            line=dict(color='rgba(30, 64, 175, 0.8)', width=3), # Darker blue line from reference
            marker=dict(
                color=df_sorted['TEMPERATURE'],
                colorscale='YlOrRd_r',  # Yellow-Orange-Red reversed, closer to reference
                size=6,
                colorbar=dict(
                    title=dict(text="Temp (°C)", font=dict(size=12)),
                    thickness=15,
                    len=0.7,
                    x=1.05,
                    tickfont=dict(size=10)
                ),
                cmin=df_sorted['TEMPERATURE'].min(),
                cmax=df_sorted['TEMPERATURE'].max(),
                showscale=True,
                line=dict(color='rgba(30, 64, 175, 0.5)', width=1)
            ),
            name='Fishing Gear Profile',
            hovertemplate='<b>Time:</b> %{x}<br><b>Depth:</b> %{y:.1f}m<br><b>Temperature:</b> %{marker.color:.2f}°C<br><extra></extra>'
        ))
        
        # Dynamic fishing phase annotations based on time, not record count
        deployment_time = df_sorted['DATETIME'].iloc[0]
        retrieval_time = df_sorted['DATETIME'].iloc[-1]
        total_duration_seconds = (retrieval_time - deployment_time).total_seconds()
        
        # Define phases: Deployment (first 10%), Retrieval (last 5%)
        deployment_end_time = deployment_time + pd.Timedelta(seconds=total_duration_seconds * 0.1)
        retrieval_start_time = retrieval_time - pd.Timedelta(seconds=total_duration_seconds * 0.05)
        
        fig.add_vrect(
            x0=deployment_time, x1=deployment_end_time,
            fillcolor="rgba(144, 238, 144, 0.2)", # Light green like reference
            layer="below", line_width=0,
            annotation_text="DEPLOYMENT", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=retrieval_start_time, x1=retrieval_time,
            fillcolor="rgba(255, 182, 193, 0.2)", # Light red/pink like reference
            layer="below", line_width=0,
            annotation_text="RETRIEVAL", annotation_position="top right"
        )
        
        # Add maximum depth marker
        fig.add_trace(go.Scatter(
            x=[max_depth_time], y=[max_depth],
            mode='markers',
            marker=dict(color='red', size=12, symbol='diamond', line=dict(color='white', width=2)),
            name=f'Max Depth: {max_depth:.1f}m',
            hovertemplate=f'<b>Maximum Fishing Depth</b><br>Time: %{{x}}<br>Depth: {max_depth:.1f}m<extra></extra>'
        ))
        
        # Add depth zone lines matching reference image style
        if max_depth > 50:
            fig.add_hline(
                y=50, line_dash="dot", line_color="#f5a623", # Muted orange
                annotation_text="Epipelagic Zone (0-50m)", annotation_position="bottom right"
            )
        
        if max_depth > 200:
            fig.add_hline(
                y=200, line_dash="dot", line_color="#7e57c2", # Muted purple
                annotation_text="Mesopelagic Zone (50-200m)", annotation_position="bottom right"
            )
        
        # Update layout with styling to match reference image
        fig.update_layout(
            title=dict(
                text="<b>Longline Fishing Operation Timeline</b><br><sub>Gear Deployment Profile - Time vs Depth with Temperature</sub>",
                x=0.5, font=dict(size=18, color='#333333')
            ),
            xaxis=dict(
                title=None, gridcolor='#EAEAEA', showgrid=True,
                tickfont=dict(size=12, color='#555555'), tickangle=-30
            ),
            yaxis=dict(
                title=dict(text="Depth (m)", font=dict(size=14, color='#555555')),
                autorange='reversed', range=[max_depth + 20, -10],
                gridcolor='#EAEAEA', showgrid=True,
                tickfont=dict(size=12, color='#555555')
            ),
            plot_bgcolor='#fbf9f4', # Beige background from reference
            paper_bgcolor='#fbf9f4',
            height=600,
            showlegend=True,
            legend=dict(
                x=0.02, y=0.98, yanchor="top", xanchor="left",
                bgcolor='white', # Opaque background
                bordercolor='#CCCCCC', borderwidth=1
            ),
            hovermode='x unified'
        )
        
        return fig
    
    except Exception as e:
        # Fallback simple plot with error message
        fig = go.Figure()
        fig.update_layout(title=f"Could not generate plot: {e}")
        return fig

def main():
    # Check authentication first
    if not check_authentication():
        show_login_page()
        return
    
    # Show logout option in sidebar
    show_logout_option()
    
    # Sidebar controls
    st.sidebar.header("📊 Dashboard Controls")

    st.sidebar.subheader("📂 Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Upload a MOANA CSV file", 
        type=['csv']
    )

    # Create tab system
    tab1, tab2 = st.tabs(["🎣 MOANA Sensor Analysis", "⚓ Longline Catenary Calculator"])
    
    with tab1:
        # MOANA sensor analysis (existing code)
        moana_sensor_analysis(uploaded_file)
        
    with tab2:
        # Catenary curve builder
        catenary_curve_builder()

def moana_sensor_analysis(uploaded_file):
    """MOANA sensor data analysis tab"""
    data_source = None
    if uploaded_file is not None:
        data_source = uploaded_file
    else:
        default_file = 'MOANA_0874_136_250610090002_qc.csv'
        if os.path.exists(default_file):
            data_source = default_file
            st.sidebar.info(f"📌 Using default file. Upload a file to analyze your own data.")
        else:
            st.warning("Please upload a MOANA data file to begin.")
            st.stop()
    
    # Load data
    try:
        moana_df = load_moana_data(data_source)

        if moana_df is None:
            st.stop()
        
        # Data overview
        st.sidebar.subheader("Data Overview")
        st.sidebar.info(f"""
        **Total Records:** {len(moana_df):,}  
        **Start Time:** {moana_df['DATETIME'].min().strftime('%Y-%m-%d %H:%M')}  
        **End Time:** {moana_df['DATETIME'].max().strftime('%Y-%m-%d %H:%M')}
        """)
        
        # Quality control filter
        st.sidebar.subheader("⚙️ Filters")

        # Define all possible QC flags and their labels
        all_qc_options = {
            1: "✅ Good", 
            2: "👍 Probably Good", 
            3: "🤔 Probably Bad", 
            4: "❌ Bad"
        }
        
        # Get available flags from the dataframe
        available_flags = sorted(moana_df['QC_FLAG'].unique())
        
        # Determine a safe default, only using flags that are actually present
        desired_defaults = [1, 2, 3]
        safe_default = [flag for flag in desired_defaults if flag in available_flags]
        
        # If no desired defaults are available, fall back to all available flags
        if not safe_default:
            safe_default = available_flags

        qc_flags = st.sidebar.multiselect(
            "Filter by Quality Control Flags",
            options=list(all_qc_options.keys()),
            default=safe_default,
            format_func=lambda x: all_qc_options.get(x, f"Unknown Flag: {x}")
        )
        
        # --- Date/Time Filter ---
        st.sidebar.markdown("---")
        min_time = moana_df['DATETIME'].min()
        max_time = moana_df['DATETIME'].max()
        
        selected_time_range = st.sidebar.slider(
            "Filter by Time Range",
            min_value=min_time.to_pydatetime(),
            max_value=max_time.to_pydatetime(),
            value=(min_time.to_pydatetime(), max_time.to_pydatetime()),
            format="MM/DD/YY - HH:mm"
        )

        # Filter data based on QC flags and time range
        filtered_df = moana_df[
            (moana_df['QC_FLAG'].isin(qc_flags)) &
            (moana_df['DATETIME'] >= selected_time_range[0]) &
            (moana_df['DATETIME'] <= selected_time_range[1])
        ]

        if filtered_df.empty:
            st.warning("No data available for the selected filters. Please adjust the QC flags or time range.")
            st.stop()
        
        # Header
        logo_base64 = "data:image/png;base64,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"
        
        st.markdown(f"""
        <div class="header-container">
            <img src="{logo_base64}" alt="Fishing Logo">
            <div>
                <h1>Professional Fishing Data Dashboard</h1>
                <p>MOANA Sensor Data Analysis for Longline Operations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate key statistics
        avg_depth = filtered_df['DEPTH'].mean()
        avg_temp = filtered_df['TEMPERATURE'].mean()
        min_temp = filtered_df['TEMPERATURE'].min()
        max_temp = filtered_df['TEMPERATURE'].max()
        max_depth = filtered_df['DEPTH'].max()
        
        # Calculate advanced oceanographic statistics
        advanced_stats = calculate_advanced_statistics(filtered_df)
        thermocline_depth = calculate_thermocline(filtered_df)
        
        # Main dashboard layout
        st.markdown("### Key Performance Indicators")
        cols = st.columns(4)
        metric_cards_1 = [
            (cols[0], "🌊 Average Depth", f"{avg_depth:.1f} m"),
            (cols[1], "🌡️ Average Temperature", f"{avg_temp:.2f} °C"),
            (cols[2], "❄️ Min Temperature", f"{min_temp:.2f} °C"),
            (cols[3], "🔥 Max Temperature", f"{max_temp:.2f} °C"),
        ]
        for col, label, value in metric_cards_1:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # Additional statistics row
        st.markdown("") # for spacing
        cols = st.columns(4)
        metric_cards_2 = [
            (cols[0], "🏊 Max Depth", f"{max_depth:.1f} m"),
            (cols[1], "📍 Latitude", f"{filtered_df['LATITUDE'].iloc[0]:.3f}°N"),
            (cols[2], "📍 Longitude", f"{filtered_df['LONGITUDE'].iloc[0]:.3f}°E"),
            (cols[3], "🌡️ Thermocline", f"{thermocline_depth:.1f} m" if thermocline_depth else "Not Detected"),
        ]
        for col, label, value in metric_cards_2:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")

        # Main visualization section - CRITICAL TIME VS DEPTH PROFILE
        st.markdown('<div class="chart-container"><h3>🎣 Longline Fishing Operation Timeline</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        time_depth_fig = create_time_depth_profile(filtered_df)
        st.plotly_chart(time_depth_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Secondary visualizations
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="chart-container"><h3>📈 Temperature-Depth Profile</h3>', unsafe_allow_html=True)
            depth_temp_fig = create_depth_temperature_profile(filtered_df)
            st.plotly_chart(depth_temp_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="chart-container"><h3>⏱️ Time Series Analysis</h3>', unsafe_allow_html=True)
            time_series_fig = create_time_series_plots(filtered_df)
            st.plotly_chart(time_series_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Map and Data Export Section
        col_map, col_data = st.columns([1, 1])

        with col_map:
             st.markdown('<div class="chart-container"><h3>📍 Deployment Location</h3>', unsafe_allow_html=True)
             lat = filtered_df['LATITUDE'].iloc[0]
             lon = filtered_df['LONGITUDE'].iloc[0]
             m = folium.Map(location=[lat, lon], zoom_start=8, tiles='CartoDB positron')
             folium.Marker([lat, lon], popup="MOANA Sensor Location", icon=folium.Icon(color='blue', icon='ship', prefix='fa')).add_to(m)
             st_folium(m, use_container_width=True, height=450)
             st.markdown('</div>', unsafe_allow_html=True)
        
        with col_data:
            st.markdown('<div class="chart-container" style="height: 100%;"><h3>💾 Data Export & Viewer</h3>', unsafe_allow_html=True)
            
            # Data export section
            st.markdown("##### Download Data")
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Filtered Data",
                    data=csv,
                    file_name=f"moana_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )
            
            with col_export2:
                summary_stats = {
                    'Metric': ['Average Depth (m)', 'Average Temperature (°C)', 'Min Temperature (°C)', 
                              'Max Temperature (°C)', 'Max Depth (m)', 'Thermocline Depth (m)'],
                    'Value': [f"{avg_depth:.1f}", f"{avg_temp:.2f}", f"{min_temp:.2f}", 
                             f"{max_temp:.2f}", f"{max_depth:.1f}", 
                             f"{thermocline_depth:.1f}" if thermocline_depth else "Not detected"]
                }
                summary_df = pd.DataFrame(summary_stats)
                
                csv_summary = summary_df.to_csv(index=False)
                st.download_button(
                    label="📊 Summary Stats",
                    data=csv_summary,
                    file_name=f"moana_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )
            
            st.markdown("---")
            
            # Raw data viewer
            with st.expander("🔍 View Raw Data Table"):
                st.dataframe(filtered_df, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"An error occurred while rendering the dashboard: {str(e)}")
        st.error(f"Error type: {type(e).__name__}")
        
        # More detailed error information
        import traceback
        st.error("Full error traceback:")
        st.code(traceback.format_exc())
        
        st.info("Please make sure the MOANA_0874_136_250610090002_qc.csv file is in the same directory as this app.")
        
        # Check if file exists
        if os.path.exists('MOANA_0874_136_250610090002_qc.csv'):
            st.success("✅ CSV file found in directory.")
        else:
            st.error("❌ CSV file not found in directory.")
            try:
                files_in_dir = [f for f in os.listdir('.') if f.endswith('.csv')]
                if files_in_dir:
                    st.info("Found these CSV files in the directory:")
                    st.code('\n'.join(files_in_dir))
            except Exception as list_e:
                st.error(f"Could not list directory contents: {list_e}")

def catenary_curve_builder():
    """Interactive catenary curve builder"""
    
    # Header for catenary tab
    st.markdown(f"""
    <div class="header-container">
        <div>
            <h1>⚓ Interactive Longline Catenary Calculator</h1>
            <p>Design and visualize your longline gear configuration</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive controls in main area (not sidebar)
    st.markdown("### ⚙️ Longline Configuration Controls")
    
    # Create columns for the sliders
    col1, col2 = st.columns(2)
    
    with col1:
        sag_depth = st.slider(
            "Maximum Sag Depth (m)",
            min_value=50,
            max_value=450,
            value=300,
            step=10,
            help="Deepest point your longline reaches"
        )
        
        num_hooks = st.slider(
            "Number of Hooks",
            min_value=5,
            max_value=50,
            value=26,
            step=1,
            help="Total hooks between floats"
        )
        
        distance_between_bouys = st.slider(
            "Distance Between Bouys (m)",
            min_value=1000,
            max_value=3000,
            value=1929,
            step=50,
            help="Horizontal distance between floats"
        )
    
    with col2:
        buoy_depth = st.slider(
            "Buoy Drop Depth (m)",
            min_value=0,
            max_value=50,
            value=11,
            step=1,
            help="How deep the buoys sit"
        )
        
        hook_start_offset = st.slider(
            "Hook Start Offset (m)",
            min_value=50,
            max_value=200,
            value=120,
            step=10,
            help="Distance from buoy before hooks start"
        )
    
    # Configuration summary KPIs at the top
    st.markdown("### Configuration Overview")
    col1, col2, col3 = st.columns(3)
    
    hook_spacing = (distance_between_bouys - 2 * hook_start_offset) / (num_hooks - 1) if num_hooks > 1 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚓ CONFIGURATION</div>
            <div class="metric-value">{num_hooks} Hooks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📏 MAX DEPTH</div>
            <div class="metric-value">{sag_depth}m</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🎣 HOOK SPACING</div>
            <div class="metric-value">{hook_spacing:.1f}m</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create catenary curve
    catenary_fig = create_interactive_catenary(
        sag_depth, num_hooks, distance_between_bouys, 
        buoy_depth, hook_start_offset
    )
    
    # Display the catenary visualization
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(catenary_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def create_interactive_catenary(sag_depth, num_hooks, distance_between_bouys, buoy_depth, hook_start_offset):
    """Create interactive catenary curve with temperature background"""
    
    # Calculate catenary curve parameters
    L = distance_between_bouys  # horizontal distance
    D = sag_depth - buoy_depth  # vertical sag from buoy level
    
    # Catenary parameter calculation (simplified)
    # For a catenary: y = a * cosh(x/a) - a
    # We need to solve for 'a' given L and D
    
    # Approximate solution for catenary parameter
    a = L / (2 * np.arcsinh(D / (L/2)))
    
    # Generate catenary curve points
    x_points = np.linspace(-L/2, L/2, 1000)
    y_points = a * np.cosh(x_points / a) - a + buoy_depth
    
    # Create temperature background
    fig = go.Figure()
    
    # Add temperature gradient background (30°C to 0°C from 0-450m)
    depth_levels = np.linspace(0, 450, 50)
    temp_levels = 30 - (depth_levels / 450) * 30  # 30°C at surface, 0°C at 450m
    
    for i in range(len(depth_levels)-1):
        temp_color = temp_levels[i]
        # Create color from temperature (red=warm, blue=cold)
        normalized_temp = temp_color / 30
        red = int(255 * normalized_temp)
        blue = int(255 * (1 - normalized_temp))
        color = f"rgba({red}, 100, {blue}, 0.3)"
        
        fig.add_shape(
            type="rect",
            x0=-L/2 - 200, x1=L/2 + 200,
            y0=depth_levels[i], y1=depth_levels[i+1],
            fillcolor=color,
            line_width=0,
            layer="below"
        )
    
    # Add main catenary line (BLACK as requested)
    fig.add_trace(go.Scatter(
        x=x_points,
        y=y_points,
        mode='lines',
        line=dict(color='black', width=4),
        name='Longline',
        hovertemplate='<b>Distance:</b> %{x:.0f}m<br><b>Depth:</b> %{y:.1f}m<extra></extra>'
    ))
    
    # Add buoys
    fig.add_trace(go.Scatter(
        x=[-L/2, L/2],
        y=[buoy_depth, buoy_depth],
        mode='markers',
        marker=dict(
            size=20,
            color='orange',
            symbol='circle',
            line=dict(color='black', width=2)
        ),
        name='Buoys',
        hovertemplate='<b>Buoy Position</b><br>Distance: %{x:.0f}m<br>Depth: %{y:.1f}m<extra></extra>'
    ))
    
    # Add hooks along the line (starting from offset)
    if num_hooks > 0:
        hook_x_start = -L/2 + hook_start_offset
        hook_x_end = L/2 - hook_start_offset
        hook_x_positions = np.linspace(hook_x_start, hook_x_end, num_hooks)
        
        # Interpolate hook depths from catenary curve
        hook_depths = np.interp(hook_x_positions, x_points, y_points)
        
        fig.add_trace(go.Scatter(
            x=hook_x_positions,
            y=hook_depths,
            mode='markers',
            marker=dict(
                size=8,
                color='red',
                symbol='x',
                line=dict(color='white', width=1)
            ),
            name=f'{num_hooks} Hooks',
            hovertemplate='<b>Hook #%{pointNumber}</b><br>Distance: %{x:.0f}m<br>Depth: %{y:.1f}m<extra></extra>'
        ))
    
    # Add depth zone reference lines
    fig.add_hline(y=50, line_dash="dot", line_color="yellow", 
                  annotation_text="Epipelagic Zone (0-50m)", annotation_position="right")
    fig.add_hline(y=200, line_dash="dot", line_color="orange", 
                  annotation_text="Mesopelagic Zone (50-200m)", annotation_position="right")
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>Longline Configuration: {num_hooks} Hooks at {sag_depth}m Maximum Depth</b>",
            x=0.5,
            font=dict(size=18, color='#333333')
        ),
        xaxis=dict(
            title="Distance (m)",
            range=[-L/2 - 200, L/2 + 200],
            gridcolor='#EAEAEA',
            showgrid=True,
            tickfont=dict(size=12, color='#555555')
        ),
        yaxis=dict(
            title="Depth (m)",
            range=[450, 0],  # Fixed range as requested (0-450m)
            gridcolor='#EAEAEA',
            showgrid=True,
            tickfont=dict(size=12, color='#555555')
        ),
        plot_bgcolor='#fbf9f4',
        paper_bgcolor='#fbf9f4',
        height=700,
        showlegend=True,
        legend=dict(
            x=0.02, y=0.98,
            bgcolor='white',
            bordercolor='#CCCCCC',
            borderwidth=1
        ),
        hovermode='closest'
    )
    
    return fig

if __name__ == "__main__":
    main() 