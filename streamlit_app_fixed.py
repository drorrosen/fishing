import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import folium
from streamlit_folium import st_folium
import os
from scipy.optimize import fsolve

# Page configuration
st.set_page_config(
    page_title="Fishing Data Analytics Dashboard",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOGIN CREDENTIALS
VALID_CREDENTIALS = {
    "fishing2025": "moana123"
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
        if df_sorted.empty or len(df_sorted) < 2:
            return go.Figure(layout=dict(title="Not enough data to display for the selected time range."))

        max_depth = df_sorted['DEPTH'].max()
        if pd.isna(max_depth):
             max_depth = 0

        max_depth_time_series = df_sorted[df_sorted['DEPTH'] == max_depth]['DATETIME']
        max_depth_time = max_depth_time_series.iloc[0] if not max_depth_time_series.empty else df_sorted['DATETIME'].iloc[0]

        # Create the main figure
        fig = go.Figure()
        
        temp_min = df_sorted['TEMPERATURE'].min()
        temp_max = df_sorted['TEMPERATURE'].max()

        # Create a continuous line with a color gradient by plotting many small segments
        for i in range(len(df_sorted) - 1):
            p1 = df_sorted.iloc[i]
            p2 = df_sorted.iloc[i+1]
            avg_temp = (p1['TEMPERATURE'] + p2['TEMPERATURE']) / 2
            
            normalized_temp = (avg_temp - temp_min) / (temp_max - temp_min)
            segment_color = px.colors.sample_colorscale('inferno', normalized_temp)[0]
            
            fig.add_trace(go.Scatter(
                x=[p1['DATETIME'], p2['DATETIME']],
                y=[p1['DEPTH'], p2['DEPTH']],
                mode='lines',
                line=dict(color=segment_color, width=9),  # Increased thickness by 1.5x
                hoverinfo='none',
                showlegend=False
            ))
            
        # Add an invisible trace with markers to handle hovering and the colorbar
        fig.add_trace(go.Scatter(
            x=df_sorted['DATETIME'],
            y=df_sorted['DEPTH'],
            mode='markers',
            marker=dict(
                color=df_sorted['TEMPERATURE'],
                colorscale='inferno',
                cmin=temp_min,
                cmax=temp_max,
                size=10,
                opacity=0,  # Make markers invisible
                colorbar=dict(
                    title=dict(text="Temp (°C)", font=dict(size=12)),
                    thickness=15,
                    len=0.7,
                    x=1.05,
                    tickfont=dict(size=10)
                ),
                showscale=True,
            ),
            hovertemplate='<b>Time:</b> %{x}<br><b>Depth:</b> %{y:.1f}m<br><b>Temperature:</b> %{marker.color:.2f}°C<br><extra></extra>',
            showlegend=False
        ))

        # Manually add a legend entry
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
            line=dict(color='grey', width=9), name='Fishing Gear Profile'))
        
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

    # This is now a global control for the MOANA tab
    uploaded_file = st.sidebar.file_uploader(
        "Upload a MOANA CSV file", 
        type=['csv']
    )

    # Create tab system
    tab1, tab2, tab3 = st.tabs([
        "🎣 MOANA Sensor Analysis", 
        "⚓ Longline Catenary Calculator",
        "🐟 Fish Catch Analysis"
    ])
    
    with tab1:
        # MOANA sensor analysis (existing code)
        moana_sensor_analysis(uploaded_file)
        
    with tab2:
        # Catenary curve builder
        catenary_curve_builder()

    with tab3:
        # Fish catch analysis
        fish_catch_analysis()

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

        qc_flags = st.sidebar.multiselect(
            "Filter by Quality Control Flags",
            options=list(all_qc_options.keys()),
            default=available_flags, # Default to all available flags
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
        logo_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAJcEhZcwAACxMAAAsTAQCanBgAAAbnSURBVHhe7Zx/bBRVFMd/t3t3t9vtbru0Lb1YaVMrhQ21xgeijiYkFmOMiQkKKAjRj2hi/JgYvxijGGM0MVqJCWCCRsVHCjEaEaNqjA/UorRQCBgQWxraUtpSultL22232+3u7t3xMDs7d7e7e7d7S7b9J7k5d+acM+e7nzkzc+49QYj/WzP/k/C5c+e+p7u7+wcA//yL8L3+B3gCjxqNBgB+/jfgA/j60NBQ1vj4+CeAPwE+4N2/B/h++fn59R0dHX/5F+F75coVoVarDYsWLfrRvwc+A27dunXf/Pz8fwO/A47D4QCw2Wz/7N+A/w74GvjW1tY3+Hw+oFarQRAEGI1GMJlMAICaY+qP6Gg0AovFAu9s/Aew+g/A2NjY8fHx8V8DvgD8D/B/j5cvX4aCggJkMhlCoRDUajWqqoAgMvlwmazgclkAgDLy8tgNBpNJG24uLhQXV0NNpuNmzRpEufR0VEAmJ+f1/sL+u034Lq6usCqA34b07+J8MOHD4PValVcXNzX+S3DwcGBc+fOgbVd4K0wGAyMjIwc3g8bT05O8OjRI9jtdkQiEWg0Gvz8/ODo6AgeHh6wWq1gNBqBIAjEYjEEAgE4ODgAADQajZkT/sSJEwBAnR7d/5qamrwL+yWfzx/169cPAA4ODjQ2NjZs9C/KxcWFgoICVFVVAQDZ2dmYmJiAa7pAqVTCbrfD6XSCxWIBALRaLWZnZ8Hn84PFYgFj1gCj0QiTyQTWajWUSiXk83kkA0YDAwOgoqICEydOhNFoBACOHTuGiIgI4HA4AAAmk2lUa+zcuROZmZkAIBqNQpIkxGIxmM1mWCwWpKenQ6lUwmq1IjIyEoqiIDQ0FLW1tYhEIpBIJPDw8CAvLw/hcBisVisAYLFY9OXgHwA+j70oDofD8dDQkM4fAP8u/E8kEoGmaYhEIqHVaiEIAoqKirBaraivr4fBYICEhATs2rULxcXFsNlsEAgEUCoVOBwOJCYm4vHjx/A4oFKpoNFogNPpRKlUwuFwYNOmTYiMjIRCoeDRo0cIDg7GmjVrAgARERGQlpYGn88Hz+eDdDqF2WwGAFwuF3K5HAzDQNnZ2X3p8Pfv3x+pVAqdTgdsNhsHDhyAn58fXC4XAoEA/v7+oNFoMJlMGB4eho+PD0RFRUEul0Ok6+tA2WwWNpsNvr6+YDAYMDAwAIvFAgAEg0Gs6t27dw8AkMvlKioqsn9X+Ldu3Tqt0WgAABoaGqTT6VpP4P/C/927d3Xm5+cr5PN5lUqll/m3X9+BIAh1dHQ41tTU5PL5/N/m33499v89/P3gN2u6/g/8LzC/X6vV/gQ4fPhwrW63C+u64O/vb9A0DQD0ej3g8XgAQCaTUXx8/LeATp06pdbr9d764CftXhGNRsPhcMDpdCIRYDAY5PP5AICjR48CAPR6vZaWlno5793zG2FfX1/QarVobGyE0WiEz+cDADQajRkzZgyeIAhqampw/vx5sFot6PV6KBQK8Hq9oNFowOv1IjU1FbFYDIlEAiKRAADi4uKwbt06pFIpCIVCGI1GMJlMAICDBw/C5XLh4sWLmJiYgLa2NsjlcqSnp0OkLzT66dOnWFlZQbFYBAAnT57EmjVrAgBjxowBkiQBjuqcnJxobm4O3t+Ffvz4UaOjo2W73R71Jk2aBACOHDmi4eHh3Lfeeuv/Jk+e7Lh06dKV7e3tN9VqNQBwcHBgu3btWte/f39XOp2+qNFotJ4f8C/M7+PHj6usrKwP+E9MTDx//vw55H+N/SgMAACcnZ21hoaGfg04evQo5yMHDx6MwcHBl+z/7Ojo0Kqrq6Moiv12p6en3dTU1I8A3759WwA4Ojra6PV6k6WlZQEA3/gN+K1bt4DT6QAATqeTxcXFXwFubW1VVVVVTQEAubm5HwFubGzUAIABo6OjU1NTk+Pj4xkAOHfunJaUlHQBeL1erFar/Y349evXjxs3bgCAWbNm9d4Bf8mNGzeAQCCA3+/Hw8ODqqoqHDt2DABQV1cHX19feL1eOJ1OoFAoeHl5ISoqCrt370YwGAQALCwsQKFQsGPHDiilUigqKor8/HykUimMxiYAQFJSkh6fD8VisZkzZwIArKysgNPpBACTyYQNGzagrq6OzMxMREVFob6+HvX19Y368h4Gg0F8fDz8/f1NJN3AwEDEx8d3Hte4uLgQHR2Nffv24fz585g3bx5CQ0Oh1BADw9PXE4HEhkZCQ8PT0BACcnJ8yZM6dZf0eOHMFsNhMAqlarAYCrV69GfHw8cnNzkZGRgaNHjyIQCAAASZIQGBiIBQsWAAAqlUoJ4uPjc9Bo9B9PnjyJr6+vl/eBIAi4XC5UVFQAgKioKH1/5n818/8A/t2RfgfLqT0AAAAASUVORK5CYII="
        
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
    
    # Initialize session state for linked sliders if not already present
    if 'num_hooks' not in st.session_state:
        st.session_state.num_hooks = 26
    if 'hook_spacing' not in st.session_state:
        # Calculate initial spacing based on other defaults
        st.session_state.hook_spacing = (3000 * 0.8) / (26 - 1)

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
    col1, col2, col3 = st.columns(3)
    
    # --- Helper functions for callbacks ---
    def update_spacing():
        """Callback to update spacing when num_hooks or distance_between_bouys changes."""
        if st.session_state.num_hooks > 1:
            hook_spacing_factor = 0.8
            total_hook_span = st.session_state.distance_between_bouys * hook_spacing_factor
            calculated_spacing = total_hook_span / (st.session_state.num_hooks - 1)
            # Clamp the value to stay within slider bounds (10.0 to dynamic_max)
            max_possible_spacing = (st.session_state.distance_between_bouys * 0.8) / 1
            dynamic_max_spacing = float(max(max_possible_spacing, 2000))
            st.session_state.hook_spacing = max(10.0, min(calculated_spacing, dynamic_max_spacing))

    def update_hooks():
        """Callback to update num_hooks when spacing changes."""
        if st.session_state.hook_spacing > 0:
            hook_spacing_factor = 0.8
            total_hook_span = st.session_state.distance_between_bouys * hook_spacing_factor
            # num_hooks = number of spaces + 1
            calculated_hooks = int(total_hook_span / st.session_state.hook_spacing) + 1
            # Clamp to valid range
            st.session_state.num_hooks = max(1, min(calculated_hooks, 50))

    with col1:
        distance_between_bouys = st.slider(
            "Distance Between Floats (m)",
            min_value=500,
            max_value=5000,
            value=3000,
            step=50,
            help="Horizontal distance between the two main floats",
            key='distance_between_bouys', # Add key to access it in callbacks
            on_change=update_spacing # This ensures spacing updates if distance changes
        )
        sag_depth = st.slider(
            "Maximum Sag Depth (m)",
            min_value=50,
            max_value=450,
            value=300,
            step=1,
            help="Deepest point the longline reaches from the float line"
        )
        
    with col2:
        num_hooks = st.slider(
            "Number of Hooks",
            min_value=1,
            max_value=50,
            step=1,
            help="Total hooks on the longline. Adjusting this will change the Hook Spacing.",
            key='num_hooks',
            on_change=update_spacing # Correct: changing num_hooks should update the spacing
        )
        
        # Calculate dynamic max value for hook spacing based on distance between floats
        # Maximum spacing occurs when we have minimum hooks (2) and maximum distance
        max_possible_spacing = (st.session_state.distance_between_bouys * 0.8) / 1  # Worst case: only 1 gap
        dynamic_max_spacing = float(max(max_possible_spacing, 2000))  # Ensure at least 2000m max and convert to float
        
        hook_spacing = st.slider(
            "Hook Spacing (Horizontal, m)",
            min_value=10.0,
            max_value=dynamic_max_spacing,
            step=1.0,
            help="Horizontal distance between hooks. Adjusting this will change the Number of Hooks.",
            key='hook_spacing',
            on_change=update_hooks # Correct: changing spacing should update the number of hooks
        )
        
    with col3:
        branchline_length = st.slider(
            "Branchline Length (m)",
            min_value=1,
            max_value=50,
            value=15,
            step=1,
            help="The length of the vertical line the hook hangs from"
        )
        buoy_depth = st.slider(
            "Float Line Depth (m)",
            min_value=0,
            max_value=50,
            value=11,
            step=1,
            help="How deep the main float line sits below the surface"
        )

    # Re-run callbacks if the distance between bouys changes, as it affects both
    # This is a simple way to keep them in sync, Streamlit reruns top-to-bottom
    # update_spacing() # This line caused the error and must be removed

    # Temperature Profile Section
    st.markdown("---") # Visual separator
    st.markdown("### 🌡️ Temperature Profile Controls")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        surface_temp = st.slider(
            "Surface Temperature (°C)", 0, 35, 24,
            help="Temperature at the ocean surface"
        )
    with t_col2:
        bottom_temp = st.slider(
            "Bottom Temperature (°C)", 0, 35, 8,
            help="Temperature at the maximum fishing depth"
        )

    # Configuration summary KPIs at the top
    st.markdown("### Configuration Overview")
    
    # Validation checks
    validation_errors = []
    
    # Check if hook spacing is reasonable
    if st.session_state.num_hooks > 1:
        calculated_spacing = (st.session_state.distance_between_bouys * 0.8) / (st.session_state.num_hooks - 1)
        if calculated_spacing > 2000:
            validation_errors.append(f"⚠️ Hook spacing too large ({calculated_spacing:.0f}m). Try using more hooks or reducing distance between floats.")
        elif calculated_spacing < 5:
            validation_errors.append(f"⚠️ Hook spacing too small ({calculated_spacing:.1f}m). Try using fewer hooks or increasing distance between floats.")
    
    # Check if configuration is physically reasonable
    if st.session_state.num_hooks > 100:
        validation_errors.append("⚠️ Too many hooks for practical longline fishing. Consider reducing to under 100 hooks.")
    
    if sag_depth > st.session_state.distance_between_bouys / 2:
        validation_errors.append("⚠️ Sag depth is too large compared to distance between floats. This would create an unrealistic curve.")
    
    # Display validation warnings
    if validation_errors:
        st.markdown("### ⚠️ Configuration Warnings")
        for error in validation_errors:
            st.warning(error)
        st.markdown("**Please adjust the values above to continue.**")
        st.markdown("---")
    
    # Only show KPIs and chart if configuration is valid
    if not validation_errors:
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        max_fishing_depth = sag_depth + branchline_length

        with kpi_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🎣 TOTAL HOOKS</div>
                <div class="metric-value">{st.session_state.num_hooks}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📏 MAX SAG DEPTH</div>
                <div class="metric-value">{sag_depth}m</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⚓ MAX FISHING DEPTH</div>
                <div class="metric-value">{max_fishing_depth}m</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">↔️ HOOK SPACING (HORIZONTAL)</div>
                <div class="metric-value">{st.session_state.hook_spacing:.1f}m</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Create catenary curve
        catenary_fig = create_interactive_catenary(
            sag_depth, st.session_state.num_hooks, distance_between_bouys, 
            buoy_depth, branchline_length, surface_temp, bottom_temp
        )
        
        # Display the catenary visualization
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(catenary_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show placeholder when configuration is invalid
        st.markdown("### 📊 Longline Visualization")
        st.info("👆 Please fix the configuration warnings above to see your longline design.")

def fish_catch_analysis():
    """Tab for logging and analyzing fish catch data."""
    st.markdown(f"""
    <div class="header-container">
        <div>
            <h1>🐟 Fish Catch Logger & Trend Analysis</h1>
            <p>Log your catches to identify the most productive hook positions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for catch data if it doesn't exist
    if 'catch_data' not in st.session_state:
        st.session_state.catch_data = pd.DataFrame(columns=['Timestamp', 'Hook Number', 'Fish Weight (lbs)'])

    # --- Data Input Form ---
    st.markdown("### 📝 Log a New Catch")
    with st.form("catch_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            hook_number = st.number_input("Hook Number", min_value=1, max_value=1000, step=1)
            catch_date = st.date_input("Catch Date", value=datetime.now())
        with c2:
            fish_weight = st.number_input("Fish Weight (lbs, 0-1000)", min_value=0, max_value=1000, step=10)
            catch_time = st.time_input("Catch Time", value=datetime.now().time())
        
        submit_button = st.form_submit_button(label='➕ Add Catch Record')

    if submit_button:
        catch_timestamp = datetime.combine(catch_date, catch_time)
        new_catch = pd.DataFrame({
            'Timestamp': [catch_timestamp],
            'Hook Number': [hook_number],
            'Fish Weight (lbs)': [fish_weight]
        })
        st.session_state.catch_data = pd.concat([st.session_state.catch_data, new_catch], ignore_index=True)
        st.success(f"✅ Catch recorded for hook #{hook_number} ({fish_weight} lbs) on {catch_timestamp.strftime('%Y-%m-%d %H:%M')}!")

    st.markdown("---")

    # --- Catch Data Visualization & Management ---
    if st.session_state.catch_data.empty:
        st.info("No catch data logged yet. Use the form above to add your first catch.")
    else:
        st.markdown("### 📊 Catch Analysis Dashboard")
        
        # Create columns for pie charts with better spacing
        st.markdown("#### 📈 Visual Analysis")
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("##### 🎣 Hook Distribution")
            hook_pie_fig = create_hook_distribution_pie(st.session_state.catch_data)
            st.plotly_chart(hook_pie_fig, use_container_width=True)
            
        with col2:
            st.markdown("##### 🐟 Fish Size Distribution")
            size_pie_fig = create_fish_size_pie(st.session_state.catch_data)
            st.plotly_chart(size_pie_fig, use_container_width=True)
        
        st.markdown("---")  # Visual separator
        
        # Main analysis chart (existing)
        st.markdown("#### 📊 Detailed Hook Performance")
        fig = create_catch_analysis_chart(st.session_state.catch_data)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")  # Visual separator

        # Summary statistics
        st.markdown("#### 📋 Summary Statistics")
        total_catches = len(st.session_state.catch_data)
        total_weight = st.session_state.catch_data['Fish Weight (lbs)'].sum()
        avg_weight = st.session_state.catch_data['Fish Weight (lbs)'].mean()
        most_productive_hook = st.session_state.catch_data['Hook Number'].mode().iloc[0] if not st.session_state.catch_data.empty else "N/A"
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🎣 TOTAL CATCHES</div>
                <div class="metric-value">{total_catches}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⚖️ TOTAL WEIGHT</div>
                <div class="metric-value">{total_weight:.0f} lbs</div>
            </div>
            """, unsafe_allow_html=True)
            
        with stat_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 AVG WEIGHT</div>
                <div class="metric-value">{avg_weight:.1f} lbs</div>
            </div>
            """, unsafe_allow_html=True)
            
        with stat_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🏆 BEST HOOK</div>
                <div class="metric-value">#{most_productive_hook}</div>
            </div>
            """, unsafe_allow_html=True)

        # Data table and export
        st.markdown("### 🗂️ Raw Catch Data")
        st.dataframe(st.session_state.catch_data, use_container_width=True)
        
        col1, col2 = st.columns([1, 0.2])
        with col1:
            csv = st.session_state.catch_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Catch Data (CSV)",
                csv,
                f"catch_data_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        with col2:
            if st.button("🗑️ Clear All Data", type="primary"):
                st.session_state.catch_data = pd.DataFrame(columns=['Timestamp', 'Hook Number', 'Fish Weight (lbs)'])
                st.rerun()

def create_hook_distribution_pie(df):
    """Creates a pie chart showing which hooks are most productive"""
    
    if df.empty:
        return go.Figure().update_layout(title="No data to display")
    
    # Count catches per hook
    hook_counts = df['Hook Number'].value_counts().head(8)  # Top 8 hooks to avoid overcrowding
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=[f"Hook #{hook}" for hook in hook_counts.index],
        values=hook_counts.values,
        hole=0.4,
        textinfo='label+percent',
        textposition='auto',
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='#FFFFFF', width=2)
        ),
        pull=[0.05 if i == 0 else 0 for i in range(len(hook_counts))]  # Highlight the top hook
    )])
    
    fig.update_layout(
        title=dict(
            text="<b>Most Productive Hooks</b>",
            x=0.5,
            font=dict(size=16, color='#333333')
        ),
        showlegend=False,  # Remove legend to prevent overlap
        height=350,
        margin=dict(t=60, b=20, l=20, r=20),
        font=dict(size=12)
    )
    
    return fig

def create_fish_size_pie(df):
    """Creates a pie chart showing fish size distribution with more granular categories"""
    
    if df.empty:
        return go.Figure().update_layout(title="No data to display")
    
    # More granular fish size categories
    def categorize_fish_size(weight):
        if weight == 0:
            return "No Fish"
        elif weight <= 5:
            return "Tiny (≤5 lbs)"
        elif weight <= 15:
            return "Small (6-15 lbs)"
        elif weight <= 30:
            return "Medium (16-30 lbs)"
        elif weight <= 50:
            return "Large (31-50 lbs)"
        elif weight <= 100:
            return "XL (51-100 lbs)"
        elif weight <= 200:
            return "XXL (101-200 lbs)"
        elif weight <= 400:
            return "Trophy (201-400 lbs)"
        else:
            return "Monster (>400 lbs)"
    
    df['Size Category'] = df['Fish Weight (lbs)'].apply(categorize_fish_size)
    size_counts = df['Size Category'].value_counts()
    
    # Define colors for each category with better contrast
    color_map = {
        "No Fish": "#d3d3d3",
        "Tiny (≤5 lbs)": "#ffb3ba",
        "Small (6-15 lbs)": "#bae1ff", 
        "Medium (16-30 lbs)": "#baffc9",
        "Large (31-50 lbs)": "#ffffba",
        "XL (51-100 lbs)": "#ffdfba",
        "XXL (101-200 lbs)": "#ffc9ba",
        "Trophy (201-400 lbs)": "#ff9999",
        "Monster (>400 lbs)": "#ff6b6b"
    }
    
    colors = [color_map.get(cat, "#cccccc") for cat in size_counts.index]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=size_counts.index,
        values=size_counts.values,
        hole=0.4,
        textinfo='label+percent',
        textposition='auto',
        marker=dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=2)
        ),
        pull=[0.05 if 'Trophy' in cat or 'Monster' in cat else 0 for cat in size_counts.index]  # Highlight big fish
    )])
    
    fig.update_layout(
        title=dict(
            text="<b>Fish Size Categories</b>",
            x=0.5,
            font=dict(size=16, color='#333333')
        ),
        showlegend=False,  # Remove legend to prevent overlap
        height=350,
        margin=dict(t=60, b=20, l=20, r=20),
        font=dict(size=12)
    )
    
    return fig

def create_catch_analysis_chart(df):
    """Creates a bar chart to visualize catch frequency and weight by hook number."""
    
    if df.empty:
        return go.Figure().update_layout(title="No data to display")

    # Aggregate data: count catches and sum weight per hook
    analysis_df = df.groupby('Hook Number').agg(
        Catch_Count=('Hook Number', 'size'),
        Total_Weight=('Fish Weight (lbs)', 'sum')
    ).reset_index()

    fig = go.Figure()

    # Add bar for catch count
    fig.add_trace(go.Bar(
        x=analysis_df['Hook Number'],
        y=analysis_df['Catch_Count'],
        name='Number of Catches',
        marker_color='rgba(31, 119, 180, 0.8)',
        hovertemplate='<b>Hook #:</b> %{x}<br><b>Catches:</b> %{y}<extra></extra>'
    ))

    # Add line for total weight
    fig.add_trace(go.Scatter(
        x=analysis_df['Hook Number'],
        y=analysis_df['Total_Weight'],
        name='Total Weight (lbs)',
        mode='lines+markers',
        line=dict(color='rgba(255, 127, 14, 1)', width=3),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate='<b>Hook #:</b> %{x}<br><b>Total Weight:</b> %{y} lbs<extra></extra>'
    ))

    # Update layout for a dual-axis chart
    fig.update_layout(
        title=dict(
            text="<b>Catch Frequency and Weight by Hook Number</b>",
            x=0.5,
            font=dict(size=18, color='#333333')
        ),
        xaxis=dict(
            title="Hook Number",
            type='category' # Treat hook numbers as categories
        ),
        yaxis=dict(
            title="Number of Catches",
            side='left',
            color='#1f77b4'
        ),
        yaxis2=dict(
            title="Total Weight (lbs)",
            side='right',
            overlaying='y',
            showgrid=False,
            color='#ff7f0e'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white',
        barmode='group'
    )
    return fig

def solve_catenary_a(L, D):
    """
    Solves the catenary equation D = a * (cosh(L/(2a)) - 1) for the parameter 'a'.
    L = horizontal distance between endpoints
    D = vertical sag from endpoints to the vertex
    """
    if D <= 1e-6:  # If there is no sag, the line is straight (infinite 'a')
        return 1e9
    # The equation to solve for a: a * (cosh(L / (2a)) - 1) - D = 0
    func = lambda a: a * (np.cosh(L / (2 * a)) - 1) - D
    
    # A good initial guess can be found from the parabolic approximation of a catenary
    initial_guess = L**2 / (4 * D)
    
    # Use fsolve to find the root
    try:
        a_solution, = fsolve(func, x0=initial_guess)
    except: # fsolve might fail in some edge cases
        a_solution = initial_guess
    return a_solution

def create_interactive_catenary(sag_depth, num_hooks, distance_between_bouys, buoy_depth, branchline_length, surface_temp, bottom_temp):
    """Create an interactive, single-basket catenary curve with branchlines."""
    
    fig = go.Figure()
    
    max_fishing_depth = sag_depth + branchline_length

    # --- Draw Temperature Gradient Background ---
    depth_levels = np.linspace(0, max_fishing_depth + 50, 20)
    for i in range(len(depth_levels) - 1):
        # Calculate temperature at this depth segment (linear interpolation)
        depth_fraction = (depth_levels[i] / (max_fishing_depth + 50))
        temp = surface_temp - (surface_temp - bottom_temp) * depth_fraction
        
        # Normalize temperature to 0-1 for the colorscale
        normalized_temp = (temp - bottom_temp) / (surface_temp - bottom_temp) if (surface_temp - bottom_temp) != 0 else 0.5
        
        segment_color = px.colors.sample_colorscale('inferno', normalized_temp)[0]

        fig.add_shape(
            type="rect",
            x0=-distance_between_bouys, x1=distance_between_bouys * 2,
            y0=depth_levels[i], y1=depth_levels[i+1],
            fillcolor=segment_color,
            line_width=0,
            layer="below",
            opacity=0.3
        )

    L = distance_between_bouys
    D = sag_depth - buoy_depth

    # --- Catenary Calculation ---
    # 1. Solve for the catenary parameter 'a', which defines the shape
    a = solve_catenary_a(L, D)

    # 2. Generate points for the main catenary curve using the CORRECTED formula
    # This formula ensures the curve hangs down ("smiles")
    x_points = np.linspace(-L/2, L/2, 200)
    y_points = sag_depth - a * (np.cosh(x_points / a) - 1)

    # Add the main catenary line
    fig.add_trace(go.Scatter(
        x=x_points,
        y=y_points,
        mode='lines',
        line=dict(color='black', width=3),
        name='Mainline'
    ))

    # --- Draw hooks and branchlines ---
    if num_hooks > 0:
        # Distribute hooks evenly, avoiding the very edges
        hook_spacing_factor = 0.8
        hook_start_x = - (L / 2) * hook_spacing_factor
        hook_end_x = (L / 2) * hook_spacing_factor
        
        hook_x_positions = np.linspace(hook_start_x, hook_end_x, num_hooks)
        
        # Calculate hook positions on the main line using the CORRECTED formula
        hook_y_on_line = sag_depth - a * (np.cosh(hook_x_positions / a) - 1)
        
        # Calculate final hook positions at the end of the branchlines
        hook_y_final = hook_y_on_line + branchline_length
        
        # Draw branchlines
        for j in range(num_hooks):
            fig.add_trace(go.Scatter(
                x=[hook_x_positions[j], hook_x_positions[j]],
                y=[hook_y_on_line[j], hook_y_final[j]],
                mode='lines',
                line=dict(color='black', width=1),
                hoverinfo='none',
                showlegend=False
            ))

        # Draw hook markers
        fig.add_trace(go.Scatter(
            x=hook_x_positions,
            y=hook_y_final,
            mode='markers',
            marker=dict(
                size=8,
                color='black',
                symbol='line-ns',
                line=dict(width=2)
            ),
            name=f'Hooks',
            hovertemplate='<b>Hook</b><br>Depth: %{y:.1f}m<extra></extra>'
        ))
            
    # --- Draw Floats ---
    fig.add_trace(go.Scatter(
        x=[-L/2, L/2],
        y=[buoy_depth, buoy_depth],
        mode='markers',
        marker=dict(
            size=15,
            color='orange',
            symbol='circle',
            line=dict(color='black', width=2)
        ),
        name='Floats',
        hovertemplate='<b>Float</b><br>Depth: %{y:.1f}m<extra></extra>'
    ))

    # --- Final Layout Configuration ---
    fig.update_layout(
        title=dict(
            text=f"<b>Longline Configuration: {num_hooks} Hooks</b>",
            x=0.5,
            font=dict(size=18, color='#333333')
        ),
        xaxis=dict(
            title="Distance (m)",
            range=[-L/2 - 50, L/2 + 50],
            gridcolor='#EAEAEA',
            zeroline=False,
            showgrid=True,
            tickfont=dict(size=12, color='#555555')
        ),
        yaxis=dict(
            title="Depth (m)",
            range=[max_fishing_depth + 50, -10],
            autorange=False, # Y-axis is already oriented correctly (depth increases downwards)
            gridcolor='#EAEAEA',
            showgrid=True,
            tickfont=dict(size=12, color='#555555')
        ),
        plot_bgcolor='rgba(0,0,0,0)', # Make plot background transparent to see shapes
        paper_bgcolor='white',
        height=700,
        showlegend=True,
        legend=dict(
            x=0.02, y=0.98,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#CCCCCC',
            borderwidth=1
        ),
        hovermode='closest'
    )
    
    return fig

if __name__ == "__main__":
    main() 
