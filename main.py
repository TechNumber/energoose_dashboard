import yaml
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score

from utils.column_processing_category import get_category
from utils.gusev_processing_category import gusev_get_category
from utils.merge_tables import merge_scores

CONFIG_PATH = "/Users/karenkocharyan/PycharmProjects/energoose_dashboard/configs/cluster_config.yaml"


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def encode_categorical_attributes(data, categorical_columns):
    encoder = LabelEncoder()
    encoded_data = data[categorical_columns].apply(encoder.fit_transform)
    return encoded_data


def perform_clustering(data, eps, min_samples):
    dbscan = DBSCAN(eps=eps,
                    min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(data)
    return cluster_labels


def save_cluster_labels(data, cluster_labels, output_file):
    cluster_data = data
    cluster_data['cluster_labels'] = cluster_labels
    cluster_data.to_csv(output_file, index=False)


def main(config):
    data = load_data(config['input_file'])
    data = get_category(data)
    data = gusev_get_category(data)
    data = merge_scores(data, config['path_to_csv_files'])
    categorical_data = data[config['categorical_columns']]
    numerical_data = data[config['numeric_columns']]

    encoded_data = encode_categorical_attributes(categorical_data,
                                                 config['categorical_columns'])

    processed_data = pd.concat([encoded_data, numerical_data], axis=1)

    cluster_labels = perform_clustering(processed_data,
                                        config['eps'],
                                        config['min_samples'])

    save_cluster_labels(data, cluster_labels, config['output_file'])
    silhouette = silhouette_score(processed_data, cluster_labels)
    davies_bouldin = davies_bouldin_score(processed_data, cluster_labels)

    print(f"Silhouette Score: {silhouette}")
    print(f"Davies-Bouldin Index: {davies_bouldin}")
    print(f"Cluster data saved to: {config['output_file']}")


def cli():
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)

    main(config)


if __name__ == '__main__':
    cli()
