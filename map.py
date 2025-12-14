import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data-table.csv')
if df['DEATHS'].dtype == 'object':
    df['DEATHS'] = df['DEATHS'].str.replace(',', '').astype(int)

fig = go.Figure(data=go.Choropleth(
    locations=df['STATE'],
    z=df['RATE'],
    locationmode='USA-states',
    colorscale='Reds',
    text=df['STATE'],
    colorbar_title='Crime Rate<br>per 100k',
    hovertemplate=(
        '<b>%{text}</b><br>' +
        'Crime Rate: %{z:.1f} per 100k<br>' +
        'Total Deaths: %{customdata:,}<br>' +
        '<extra></extra>'
    ),
    customdata=df['DEATHS'],
    marker_line_color='white',
    marker_line_width=1.5
))

fig.update_layout(
    title={
        'text': 'Crime Rate by State (2023)',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'family': 'Arial, sans-serif'}
    },
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(230, 245, 255)',
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=600,
    margin=dict(l=20, r=20, t=80, b=20),
    font=dict(family='Arial, sans-serif', size=12)
)

out_file = 'map.html'
fig.write_html(out_file, auto_open=False, include_plotlyjs='cdn', full_html=True)