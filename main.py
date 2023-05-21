import yaml
import numpy as np

from utils.clustering import perform_clustering
from utils.preprocessing.preprocess_functioncs import *

CONFIG_PATH = "configs/cluster_config.yaml"


def main(config):
    data = load_data(config['input_file'])
    data = get_processed_data(data, config)

    categorical_data = data[config['categorical_columns']]
    numerical_data = data[config['numeric_columns']]

    encoded_data = encode_categorical_attributes(categorical_data,
                                                 config['categorical_columns'])
    normalized_data = normalize_columns(numerical_data,
                                        config['numeric_columns'])

    processed_data = pd.concat([encoded_data, normalized_data], axis=1)
    processed_data = processed_data.dropna(subset=["Возраст"])
    cluster_labels = perform_clustering(processed_data,
                                        config)
    processed_data['кластер'] = cluster_labels
    data['кластер'] = np.nan
    data.loc[processed_data.index, 'кластер'] = cluster_labels
    save_cluster_labels(data, config['output_file'])
    print(f"Cluster data saved to: {config['output_file']}")


def cli():
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)

    main(config)


if __name__ == '__main__':
    cli()
