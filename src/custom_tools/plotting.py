import plotly.graph_objects as go
import streamlit as st
def plot_machine_data(viz_df):
    st_machines = viz_df['MACHINE_ID'].unique()
    st_min_date = viz_df['DATE'].min()
    st_max_date = viz_df['DATE'].max()
    
    col1, col2 = st.columns([0.8,0.2])
    st_d1, st_d2 = col1.slider("Select a range of values", min_value=st_min_date, max_value=st_max_date, value=(st_min_date, st_max_date))
    st_machine = col2.selectbox('Select a Machine:', st_machines)
    plot_df = viz_df[(viz_df['DATE'].between(st_d1,st_d2)) & (viz_df['MACHINE_ID'] == st_machine)]
    
    # --- 2. Initialize the Plotly Figure ---
    fig = go.Figure()
    
    # --- 3. Add Sensor Traces ---
    sensor_columns = [
        'SENSOR_1_DAILY_AVERAGE',
        'SENSOR_2_DAILY_AVERAGE',
        'SENSOR_3_DAILY_AVERAGE'
    ]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Blue, Orange, Green for distinction
    
    for i, col in enumerate(sensor_columns):
        fig.add_trace(go.Scatter(
            x=plot_df['DATE'],
            y=plot_df[col],
            mode='lines',
            name=col.replace('_', ' ').title(),
            line=dict(color=colors[i]),
            marker=dict(size=8)
        ))
    
    # --- 4. Identify and Add Vertical Lines for Failures ---
    # Filter the DataFrame to get only rows where FAILURE is 1
    failure_dates = plot_df[plot_df['FAILURE'] == 1]['DATE']
    failure_dates_list = failure_dates.tolist() # Convert to list for easy indexing
    
    # Loop through the failure dates and add a vertical line for each
    for date in failure_dates:
        # NOTE: We removed the 'name' argument so the vertical line does not appear in the legend,
        # and we rely on the visual style and annotation instead.
        fig.add_vline(
            x=date,
            line_width=2,
            line_dash="dash",
            line_color="#e32636",  # A distinct red color for failures
            # name=f"Failure: {date_str}" # Removed to declutter legend
        )
    
    # --- 4b. Add Annotation to Indicate Failure Line Type ---
    if failure_dates_list:
        first_failure_date = failure_dates_list[0]
        fig.add_annotation(
            x=first_failure_date,
            # Set y slightly above the top of the plot (yref='paper' with y=0.95)
            yref="paper", 
            y=0.95, # Place it near the top of the plotting area
            text="FAILURE",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#e32636",
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="#e32636",
            borderwidth=1,
            font=dict(color="#e32636", size=10, weight='bold')
        )
    
    # --- 5. Configure Layout for Aesthetics and Readability ---
    fig.update_layout(
        title={
            'text': "Sensor Data Time Series with Equipment Failures",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Date",
        yaxis_title="Daily Average Sensor Value",
        hovermode="x unified", # Combine tooltips across traces
        template="plotly_white", # Clean background
        legend_title_text='Sensor Readings',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        # Added a buffer at the top (t=100) for the new annotation
        margin=dict(l=40, r=40, t=100, b=40)
    )
    
    # Show the figure (this will open it in your default browser or display it in a notebook)
    st.plotly_chart(fig)
