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

HV_LIST = [37, 69, 23, 57, 76, 32, 65, 68, 45, 
           44, 67, 83, 79, 70, 92, 93, 75, 90]
MDD_LIST = [66, 86, 72, 74, 99, 46, 39,
            59, 71, 55, 48, 82, 81]

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
