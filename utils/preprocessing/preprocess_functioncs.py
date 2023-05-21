import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from utils.preprocessing.column_processing_category import get_category
from utils.preprocessing.column_processing_ages import gusev_get_category
from utils.preprocessing.merge_tables import merge_scores
from utils.preprocessing.processing_interval_groups import get_interval_groups


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def get_processed_data(data, config):
    participants_data = pd.read_csv("data/participants_parsed.csv")
    data['parsed_workplace'] = participants_data['parsed_workplace']
    data = get_category(data)
    data = gusev_get_category(data)
    data = merge_scores(data, config['path_to_csv_files'])
    data = get_interval_groups(data)
    return data


def encode_categorical_attributes(data, categorical_columns):
    encoder = LabelEncoder()
    encoded_data = data[categorical_columns].apply(encoder.fit_transform)
    return encoded_data


def normalize_columns(df, columns):
    df_normalized = df.copy()
    columns_to_normalize = df_normalized[columns]
    scaler = MinMaxScaler()
    columns_normalized = scaler.fit_transform(columns_to_normalize)
    df_normalized[columns] = columns_normalized
    return df_normalized


def save_cluster_labels(data, output_file):
    cluster_data = data
    cluster_data.to_csv(output_file, index=False)
