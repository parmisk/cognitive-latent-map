#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 23:43:03 2024

@author: khosravip2
"""


import os
import pandas as pd
import glob
from datetime import datetime, timedelta



today = datetime.now().strftime('%m%d%Y')  # Format as MMDDYYYY  

# Set Directory
ROOTDIR = '/Volumes/SDAN-EDB/SDAN1/Data/Memory-Project'
DATA_PATH = os.path.join(ROOTDIR, 'derivatives', 'nihtb')
OUTPUT_DIR = os.path.join(ROOTDIR, "derivatives", "preprocessed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'NIH_TB_data_{}.csv'.format(today))

HV_LIST = [24237, 24369, 24423, 24157, 24276, 23032, 23069, 24265, 24268, 24445, 
           24444, 24467, 24483, 24479, 24270, 24492, 24501, 24493, 24275, 24490,
           24487, 24521, 24533, 24475, 24556, 24570, 24571, 24557, 24558, 24197,
           24599, 24608, 24598, 24198, 24543, 23995, 24687, 24685, 24583, 24698,
           24624, 24662, 24789, 24833, 24902, 24915, 24898, 24921, 24930, 24916]
MDD_LIST = [24567, 24409, 24668, 24576, 24679, 24674, 24699, 24703, 24746, 24739,
            24759, 24771, 24757, 24748, 24782, 24735, 24806, 24781, 24792, 24799,
            24811, 24793, 24808, 24868, 24713, 24861, 24875, 24924]

# Helper Functions
def get_csv_files(directory):
    """Returns a list of CSV files in the specified directory."""
    return glob.glob(os.path.join(directory, '*Scores.csv'))


def classify_subject(subject_id):
    """Classifies a subject as HV, MDD, or ANX."""
    if subject_id in HV_LIST:
        return 'HV'
    elif subject_id in MDD_LIST:
        return 'MDD'
    return 'ANX'


def process_csv_files(csv_files):
    """Processes CSV files and concatenates them into a single DataFrame."""
    data_frames = []
    for file in csv_files:
        print(f"Processing file: {file}")
        data = pd.read_csv(file)
        data_frames.append(data)
    
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()


def clean_data(data):
    """Cleans and processes the merged data."""
    # Remove test sessions
    data = data[~data['PIN'].isin([11111, 99999])]
    
    # Add Type column based on subject classification
    data['Type'] = data['PIN'].apply(classify_subject)
    
    return data

#%%

def main():
    print("Starting NIH Toolbox data processing...")
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get CSV files
    csv_files = get_csv_files(DATA_PATH)
    if not csv_files:
        print("No files found in the directory. Exiting.")
        return

    # Process and clean data
    merged_data = process_csv_files(csv_files)
    cleaned_data = clean_data(merged_data)

    # Save cleaned data to CSV
    cleaned_data.to_csv(OUTPUT_FILE, index=False, header=True)
    print(f"Data saved successfully to {OUTPUT_FILE}")

    # Count unique subjects and occurrences of each type
    unique_data = cleaned_data.drop_duplicates(subset='PIN')
    type_counts = unique_data['Type'].value_counts()


    print("Counts of Each Type:")
    print(type_counts)

if __name__ == "__main__":
    main()
