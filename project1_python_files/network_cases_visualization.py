import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RangeSlider, TextBox
import io
import base64
from flask import Flask, render_template, jsonify
import networkx as nx

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from generate_graph import WARD_NEIGHBORS, WARDS_NAME
from typing import List, Tuple, Optional
import os
import scipy
from scipy.stats import pearsonr
import datetime
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib.animation as animation


# from network_names_positions import WARD_NEIGHBORS, WARD_POSITIONS
from project1_python_files.network_names_positions import WARD_NEIGHBORS, WARD_POSITIONS


### THINGS TO CHANGE:

DNM_DATA_PATH_URL = "https://raw.githubusercontent.com/ely808chen/epidemic_prediction/refs/heads/main/Data/tokyo_processed_infectious_disease_data/dnm_scores_%E3%82%A4%E3%83%B3%E3%83%95%E3%83%AB%E3%82%A8%E3%83%B3%E3%82%B6.csv"
PCC_DATA_PATH_URL = "https://raw.githubusercontent.com/ely808chen/epidemic_prediction/refs/heads/main/Data/tokyo_processed_infectious_disease_data/dnm_pcc_scores_%E3%82%A4%E3%83%B3%E3%83%95%E3%83%AB%E3%82%A8%E3%83%B3%E3%82%B6.csv"
CASES_DATA_PATH_URL = "https://raw.githubusercontent.com/ely808chen/epidemic_prediction/refs/heads/main/Data/tokyo_processed_infectious_disease_data/SD_sliding_window_master_disease_data.csv"

START_YEAR_OF_VISUALIZATION = 2024
START_MONTH_OF_VISUALIZATION = 6
I_DNM_NOISE_THRESHOLD = 2.5
I_DNM_GROWTH_THRESHOLD = 2.0

### END ##########################################################################

def load_data():
    dnm_df = pd.read_csv(DNM_DATA_PATH_URL, encoding='utf-8')
    pcc_df = pd.read_csv(PCC_DATA_PATH_URL, encoding='utf-8')
    cases_df = pd.read_csv(CASES_DATA_PATH_URL, encoding='utf-8')

    # Convert dates to datetime
    dnm_df['Date'] = pd.to_datetime(dnm_df['Date'])
    pcc_df['Date'] = pd.to_datetime(pcc_df['Date'])
    cases_df['Date'] = pd.to_datetime(cases_df['Date'])

    # Sort the data
    dnm_df = dnm_df.sort_values('Date')
    pcc_df = pcc_df.sort_values('Date')
    cases_df = cases_df.sort_values('Date')

    # Filter cases data for influenza
    cases_df_filtered = cases_df[cases_df['Disease'] == 'インフルエンザ']

    # Filter cases data for the start year of visualization
    dnm_df_filtered = dnm_df[dnm_df['Date'] >= datetime.datetime(START_YEAR_OF_VISUALIZATION, START_MONTH_OF_VISUALIZATION, 1)]
    pcc_df_filtered = pcc_df[pcc_df['Date'] >= datetime.datetime(START_YEAR_OF_VISUALIZATION, START_MONTH_OF_VISUALIZATION, 1)]
    cases_df_filtered = cases_df_filtered[cases_df_filtered['Date'] >= datetime.datetime(START_YEAR_OF_VISUALIZATION, START_MONTH_OF_VISUALIZATION, 1)]

    return dnm_df_filtered, pcc_df_filtered, cases_df_filtered


# Scale positions function
def scale_positions(positions, vertical_scale=1.2):
    """Scale the positions vertically"""
    scaled_positions = {}
    
    # Calculate center
    center_y = sum(pos[1] for pos in positions.values()) / len(positions)
    
    # Scale positions vertically from center
    for ward, pos in positions.items():
        dy = pos[1] - center_y
        scaled_positions[ward] = (
            pos[0],  # Keep x coordinate the same
            center_y + dy * vertical_scale  # Scale y coordinate
        )
    return scaled_positions

# Scale the original positions
WARD_POSITIONS = scale_positions(WARD_POSITIONS, vertical_scale=1.2)

# Create custom colormap for the colorbar
colors = [(1, 1, 1), (1, 0, 0)]  # green -> white -> red
custom_cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)  # Use 256 for a smooth gradient

# Normalize the I-scores to the range [0, 1] for color mapping
norm = Normalize(vmin=0, vmax=1)


# First, modify the ward positions by scaling them out a bit
def scale_positions(positions, scale_factor=1.2):
    """Scale the positions outward from the center"""
    # Calculate center
    center_x = sum(pos[0] for pos in positions.values()) / len(positions)
    center_y = sum(pos[1] for pos in positions.values()) / len(positions)
    
    # Scale positions outward from center
    scaled_positions = {}
    for ward, pos in positions.items():
        dx = pos[0] - center_x
        dy = pos[1] - center_y
        scaled_positions[ward] = (center_x + dx * scale_factor, 
                                center_y + dy * scale_factor)
    return scaled_positions

def create_colored_network(date, dnm_df_filtered, pcc_df_filtered, cases_df_filtered):
    """Create network with nodes colored according to I-scores and edges weighted by PCC"""
    G = nx.Graph()
    
    # Get I-scores and cases for the specific date
    date_mask = dnm_df_filtered['Date'] == date
    date_scores = dnm_df_filtered[date_mask].set_index('Ward')
    date_pcc = pcc_df_filtered[pcc_df_filtered['Date'] == date]
    date_cases = cases_df_filtered[cases_df_filtered['Date'] == date].set_index('Ward')
    
    # Calculate total cases for Tokyo
    total_cases = date_cases['Value'].sum()
    
    # Calculate average I_DNM score for current week
    avg_score = date_scores['I_score'].mean()
    
    # Get data from exactly one week ago
    prev_week_date = date - pd.Timedelta(weeks=1)
    prev_week_mask = dnm_df_filtered['Date'] == prev_week_date
    prev_week_scores = dnm_df_filtered[prev_week_mask]
    
    if not prev_week_scores.empty:
        prev_avg_score = prev_week_scores['I_score'].mean()
        # Check if previous week had an early warning state stored
        prev_week_warning = prev_week_scores['is_warning'].iloc[0] if 'is_warning' in prev_week_scores.columns else False
        # Check if previous week was in post-warning state
        prev_post_warning = prev_week_scores['post_warning'].iloc[0] if 'post_warning' in prev_week_scores.columns else False
    else:
        prev_avg_score = avg_score
        prev_week_warning = False
        prev_post_warning = False
    
    # First determine post-warning state
    # Post-warning is triggered if:
    # 1. Previous week had early warning AND current score > threshold, OR
    # 2. Previous week was in post-warning AND current score > threshold
    post_warning = avg_score > I_DNM_NOISE_THRESHOLD and (prev_week_warning or prev_post_warning)
    # Early warning is only considered if we're not in post-warning state
    is_warning = False
    if not post_warning:  # Only check for early warning if not in post-warning
        is_warning = (avg_score > I_DNM_NOISE_THRESHOLD and 
                     avg_score > 2 * prev_avg_score)
    
    # Store both warning states in the original DataFrame
    if 'is_warning' not in dnm_df_filtered.columns:
        dnm_df_filtered['is_warning'] = False
    if 'post_warning' not in dnm_df_filtered.columns:
        dnm_df_filtered['post_warning'] = False
        
    dnm_df_filtered.loc[date_mask, 'is_warning'] = is_warning
    dnm_df_filtered.loc[date_mask, 'post_warning'] = post_warning
    
    # Normalize scores to 0-1 range if they exceed 1
    max_score = max(1.0, date_scores['I_score'].max())
    
    # Add nodes with positions, colors, and case values
    for ward in WARD_POSITIONS:
        if ward in date_scores.index:
            raw_score = date_scores.loc[ward, 'I_score']
            score = raw_score / max_score
            cases = date_cases.loc[ward, 'Value'] if ward in date_cases.index else 0
            
            # Use the colormap to get the color
            color = custom_cmap(norm(score))
            
            G.add_node(ward, pos=WARD_POSITIONS[ward], color=color, cases=cases)
        else:
            # Very light red for nodes with no data
            G.add_node(ward, pos=WARD_POSITIONS[ward], color=(1, 0.95, 0.95), cases=0)
    
    # Add edges with PCC values
    for _, row in date_pcc.iterrows():
        ward1, ward2 = row['Ward'], row['Neighbor']
        if ward1 in date_scores.index and ward2 in date_scores.index:
            pcc_row = date_pcc[
                ((date_pcc['Ward'] == ward1) & (date_pcc['Neighbor'] == ward2)) |
                ((date_pcc['Ward'] == ward2) & (date_pcc['Neighbor'] == ward1))
            ]
            if not pcc_row.empty:
                pcc = abs(pcc_row['PCC_in'].values[0])
                G.add_edge(ward1, ward2, weight=pcc, color='gray')
    
    # Calculate 2-week running average of I_scores
    two_week_avg = dnm_df_filtered[dnm_df_filtered['Date'] <= date].tail(2)['I_score'].mean()
    
    # Determine if the red part of the bar chart should be displayed
    show_warning_data = int(post_warning or two_week_avg > I_DNM_NOISE_THRESHOLD)  # Convert to int
    
    # Find the most recent warning date
    warning_date = None
    warning_cases = None
    last_warning_date = None
    
    # Look back through all data up to current date to find the last warning
    past_data = dnm_df_filtered[dnm_df_filtered['Date'] <= date].sort_values('Date', ascending=False)
    for past_date, group in past_data.groupby('Date'):
        if group['is_warning'].iloc[0]:
            last_warning_date = past_date.strftime('%Y-%m-%d')  # Format the date as string
            if warning_date is None:  # Only for the most recent warning
                warning_date = past_date
                warning_cases = cases_df_filtered[cases_df_filtered['Date'] == warning_date].set_index('Ward')['Value'].to_dict()
            break
    
    # Add warning cases to the node data
    for ward in G.nodes():
        G.nodes[ward]['warning_cases'] = warning_cases.get(ward, 0) if warning_cases else 0
    
    return G, total_cases, int(is_warning), int(post_warning), float(avg_score), int(show_warning_data), last_warning_date

def create_flu_figure():
    # Load data
    dnm_df_filtered, pcc_df_filtered, cases_df_filtered = load_data()
    dates_filtered = dnm_df_filtered['Date'].unique()
    
    # Create data for all dates
    all_data = []
    historical_max_cases = cases_df_filtered['Value'].max()
    
    for date in dates_filtered:
        G, total_cases, is_warning, post_warning, avg_score, show_warning_data, last_warning_date = create_colored_network(
            date, dnm_df_filtered, pcc_df_filtered, cases_df_filtered)
        
        # Modify the nodes data to include warning cases
        nodes = []
        for node in G.nodes():
            node_data = dnm_df_filtered[
                (dnm_df_filtered['Date'] == date) & 
                (dnm_df_filtered['Ward'] == node)
            ].iloc[0]
            
            nodes.append({
                'id': str(node),
                'x': float(G.nodes[node]['pos'][0]),
                'y': float(G.nodes[node]['pos'][1]),
                'i_score': float(node_data['I_score']),
                'cases': int(G.nodes[node].get('cases', 0)),
                'warning_cases': int(G.nodes[node].get('warning_cases', 0))
            })
        
        # Get edge data with PCC values
        edges = []
        for u, v in G.edges():
            pcc_row = pcc_df_filtered[
                (pcc_df_filtered['Date'] == date) & 
                (((pcc_df_filtered['Ward'] == u) & (pcc_df_filtered['Neighbor'] == v)) |
                 ((pcc_df_filtered['Ward'] == v) & (pcc_df_filtered['Neighbor'] == u)))
            ]
            if not pcc_row.empty:
                pcc_value = float(abs(pcc_row['PCC_in'].iloc[0]))
                edges.append({
                    'source': str(u),
                    'target': str(v),
                    'pcc': pcc_value
                })
        
        all_data.append({
            'nodes': nodes,
            'edges': edges,
            'total_cases': int(total_cases),
            'is_warning': int(is_warning),
            'post_warning': int(post_warning),
            'show_warning_data': int(show_warning_data),
            'last_warning_date': last_warning_date
        })
    
    return render_template('project1.html',
                         network_data=all_data,
                         dates=[d.strftime('%Y-%m-%d') for d in dates_filtered],
                         historical_max_cases=historical_max_cases)

