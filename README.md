# TODO: Header

TODO: Description

## Installation

1. git clone https://github.com/TechNumber/energoose_dashboard.git
2. cd energoose_dashboard
3. pip install -r requirements.txt

## Running the script

To use the clustering script, run the following command:

```console
python run_clustering.py
```

To use the processing workplaces parser, run the following command:
```console
python processing_workplaces.py
```



## Usage
To use the clustering method for specified data, you should open configs/cluster_config.yaml and 
you should change params for your case:

- input_file (str): path to the input csv file
- path_to_csv_files (str): path to the csvs files which you want merge with member csv
- categorical_columns (list of str): categorical columns that you want to use for clustering
- numeric_columns (list of str): numeric columns that you want to use for clustering
- output_file (str): path to the output csv file with clustering and all preprocessing
- cluster_method (str, choice): choose a clustering method
- workplace_output (str): path to the save preprocessed workplace column in csv

## Tree of project

```bash
├── clustered_data  # Folder for storage clustered csvs
│   └── clustered.csv
├── configs. # Folder for configs
│   └── cluster_config.yaml  # Config for cluster script
├── data. # Folder for storage source data
│   ├── anonimized
│   └── Участники anonimized.csv
├── run_clustering.py  # Script for run clustering preprocessed data and save final file in csv
├── requirements.txt
└── utils
    ├── clustering.py  # Script for init cluster method and make cluster predict
    └── preprocessing  # Folder for storage preprocessing scripts
        ├── column_processing_ages.py  # Script for preprocessing ages columns
        ├── column_processing_category.py  # Script for preprocessing category columns
        ├── merge_tables.py  # Script for merge csvs in anonimized folder with members csv
        ├── preprocess_functioncs.py  # Script which run all our preprocessing scripts for specified data
        ├── processing_interval_groups.py  # Script for processing some columns to group category
        └── processing_workplaces.py  # Script for processing workplace column
```