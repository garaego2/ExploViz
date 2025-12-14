import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Load both datasets
ts_df = pd.read_csv('filtered_data.csv')
ts_df['date_parsed'] = pd.to_datetime(ts_df['date'], format='%B %Y')

state_df = pd.read_csv('data-table.csv')
if state_df['DEATHS'].dtype == 'object':
    state_df['DEATHS'] = state_df['DEATHS'].str.replace(',', '').astype(int)

# Create subplots: time series on top (60% height), map on bottom (40% height)
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Reported Murders Over Time (National)', 'Crime Rate by State'),
    specs=[[{}], [{'type': 'geo'}]],
    vertical_spacing=0.12,
    row_heights=[0.55, 0.45]
)

# Add time series trace to top subplot
fig.add_trace(
    go.Scatter(
        x=ts_df['date_parsed'],
        y=ts_df['12mo_rolling_sum'],
        mode='lines+markers',
        name='Murders (12-mo rolling)',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=6, color='#c0392b'),
        hovertemplate='<b>%{x|%B %Y}</b><br>Murders: %{y:,}<extra></extra>',
    ),
    row=1, col=1
)

# Add choropleth map trace to bottom subplot
fig.add_trace(
    go.Choropleth(
        locations=state_df['STATE'],
        z=state_df['RATE'],
        zmin=0,
        zmax=20,
        locationmode='USA-states',
        colorscale='Reds',
        text=state_df['STATE'],
        colorbar=dict(title='Crime Rate<br>per 100k', x=1.08),
        hovertemplate='<b>%{text}</b><br>Crime Rate: %{z:.1f} per 100k<extra></extra>',
        marker_line_color='white',
        marker_line_width=1.5,
        name='Crime Rate by State'
    ),
    row=2, col=1
)

# Update layout for time series axes
fig.update_xaxes(title_text='Date', row=1, col=1, showgrid=True, gridcolor='lightgray')
fig.update_yaxes(title_text='Reported Murders', row=1, col=1, showgrid=True, gridcolor='lightgray')

# Update geo for the map
fig.update_geos(
    scope='usa',
    projection=go.layout.geo.Projection(type='albers usa'),
    showlakes=True,
    lakecolor='rgb(230, 245, 255)',
    bgcolor='rgba(0,0,0,0)',
    row=2, col=1, 
)

# Update overall layout
fig.update_layout(
    title={
        'text': 'US Crime & Murder Statistics Dashboard',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 22, 'family': 'Arial, sans-serif'}
    },
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial, sans-serif', size=12),
    height=1000,
    margin=dict(l=80, r=100, t=100, b=60),
    hovermode='closest',
    legend=dict(
        orientation='h',
        x=0.5,
        xanchor='center',
        y=1.02,
        yanchor='bottom',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    showlegend=True
)
# Write to HTML file (dashboard) without auto-opening the browser
out_file = 'dashboard.html'
fig.write_html(out_file, auto_open=False, include_plotlyjs='cdn', full_html=True)
print(f"Wrote dashboard to {out_file}")
