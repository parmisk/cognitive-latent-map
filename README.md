# Cognitive Assessment Data Processing Pipeline
## cognitive-latent-map

A collection of Python scripts developed to automate preprocessing, cleaning, and integration of data from multiple computerized cognitive assessments used in a memory research project.

## Overview

This repository contains scripts preparing cognitive assessment data for statistical analyses. The pipeline standardizes participant data across multiple tasks, performs quality control, identifies incomplete sessions, classifies participant groups, and generates analysis-ready datasets.

## Repository Contents

### `NIH_toolbox.py`

Processes data from the NIH Toolbox, Picture Sequence Memory assessment.

Features include:

* Merges participant score files
* Removes test sessions
* Classifies participants into study groups
* Produces standardized datasets for analysis
* Generates participant summary statistics

---

### `Paired_Association.py`

Processes data from the computerized Paired Association memory task.

Features include:

* Merges participant task files
* Extracts task trials from raw experiment logs
* Identifies incomplete or invalid sessions
* Recodes behavioral accuracy
* Generates analysis-ready datasets
* Produces lists of excluded participants

---

### `Spatial_Navigation.py`

Processes data from the Spatial Navigation memory task.

Features include:

* Extracts task-specific behavioral data
* Standardizes navigation task sections
* Recodes participant responses
* Removes practice and instructional trials
* Identifies incomplete sessions
* Produces cleaned datasets for analysis


## Needs the following packages
```
Python
pandas
NumPy
pathlib
glob
logging
```
