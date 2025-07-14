#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 16:14:28 2023
Updated to improve efficiency Dec 8 2024

@author: khosravip2
"""
import os
import pandas as pd
from datetime import datetime, timedelta

# Set Directories
#ROOTDIR = '/Volumes/SDAN-EDB/SDAN1/Data/Memory-Project'
ROOTDIR ="Z:\SDAN1\Data\Memory-Project"
DATA_PATH = os.path.join(ROOTDIR, 'derivatives', 'pairedassociation')
OUTPUT_DIR = os.path.join(ROOTDIR, "derivatives", "preprocessed")


today = datetime.now().strftime('%m%d%Y')  # Format as MMDDYYYY  

HV_LIST = [24237, 24369, 24423, 24157, 24276, 23032, 23069, 24265, 24268, 24445, 
           24444, 24467, 24483, 24479, 24270, 24492, 24501, 24493, 24275, 24490,
           24487, 24521, 24533, 24475, 24556, 24570, 24571, 24557, 24558, 24197,
           24599, 24608, 24598, 24198, 24543, 23995, 24687, 24685, 24583, 24698,
           24624, 24662, 24789, 24833, 24902, 24915, 24898, 24921, 24930, 24916, 
           24917, 24999, 25021, 25023, 25010, 25029, 25007]
MDD_LIST = [24567, 24409, 24668, 24576, 24679, 24674, 24699, 24703, 24746, 24739,
            24759, 24771, 24757, 24748, 24782, 24735, 24806, 24781, 24792, 24799,
            24811, 24793, 24808, 24868, 24713, 24861, 24875, 24924, 24984, 24985, 
            24972, 24974, 24973]

# Set Functions
def get_csv_files(directory):
    """Returns a list of CSV files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.csv')]



def filter_data(data, start_key, end_key):
    """Filters rows between start_key and end_key in the 'Section' column."""
    try:
        start_idx = data[data['Section'] == start_key].index[0] + 1
        end_idx = data[data['Section'] == end_key].index[0]
        return data.loc[start_idx:end_idx]
    except IndexError:
        return None
    


def classify_subject(subject_id):
    """Classifies a subject as HV, MDD, or ANX."""
    if subject_id in HV_LIST:
        return 'HV'
    elif subject_id in MDD_LIST:
        return 'MDD'
    return 'ANX'



def process_csv_files(csv_files, data_path):
    """Processes CSV files and filters data based on specific keys."""
    data_frames = []
    skipped_files = []

    for file in csv_files:
        file_path = os.path.join(data_path, file)
        try:
            data = pd.read_csv(file_path)
            filtered_data = filter_data(data, 'Practice Success Screen', 'Test:24 of 24 (Try #0)')
            if filtered_data is not None:
                data_frames.append(filtered_data)
            else:
                skipped_files.append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            skipped_files.append(file)

    return pd.concat(data_frames) if data_frames else pd.DataFrame(), skipped_files

#%%

def main():
    print("Starting data processing...")
    
    # Creates output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gets CSV files
    csv_files = get_csv_files(DATA_PATH)
    merged_data, skipped_files = process_csv_files(csv_files, DATA_PATH)

    # Save skipped files
 
    skipped_files_path = os.path.join(OUTPUT_DIR, 'PA_Subjexcluded_{}.csv'.format(today))
    pd.DataFrame(skipped_files, columns=['Filename']).to_csv(skipped_files_path, index=False)

    # Add Process Type column
    merged_data['Type'] = merged_data['SubjectID'].apply(classify_subject)

    # Recode User Answer Correctness
    merged_data['User Answer Correctness'] = merged_data['User Answer Correctness'].replace({'Correct': 1, 'Incorrect': 0})

    # Filter out irrelevant lines/sections
    merged_data = merged_data[merged_data['Section'] != "Time Out Warning Screen"]

    # Drop rows with NaN in Correct Answer
    merged_data.dropna(subset=["User Answer Correctness"], inplace=True)

    # Save merged data
    output_file = os.path.join(OUTPUT_DIR, 'PairedAssociation_{}.csv'.format(today))
    merged_data.to_csv(output_file, index=False)

    print(f"Data saved successfully to {output_file}")
    print(f"Skipped files list saved to {skipped_files_path}")
    print(f"Skipped files Subject list {skipped_files}")
    print(f"Number of unique subjects: {merged_data['SubjectID'].nunique()}")
    unique_data = merged_data.drop_duplicates(subset='SubjectID')
    type_counts = unique_data['Type'].value_counts()
    print("Counts of Each Type:")
    print(type_counts)

if __name__ == "__main__":
    main()
