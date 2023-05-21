import time

import requests
import pandas as pd
import yaml

CONFIG_PATH = "/home/technum/coding/pycharm/energoose_dashboard/configs/cluster_config.yaml"

url = r'https://yandex.ru/maps/?from=tabbar&text='
tag = 'analyticsId'


def get_name_coords(place):
    html = requests.get(url + place).text
    print('Captcha:', 'data-testid="checkbox-captcha"' in html)

    names_list = []
    coords_list = []
    pos = 0

    while html.find(tag, pos) != -1:
        pos = html.find(tag, pos) + len(tag)
        name = html[html.find('title', pos) + 8:html.find('description', pos) - 3]
        coords = html[html.find('[', pos) + 1:html.find(']', pos)].split(',')
        coords = list(map(float, map(str.strip, coords)))
        name.replace('"', '')
        names_list.append(name)
        coords_list.extend(coords)

    if names_list:
        return names_list[0], coords_list[:2]
    else:
        return '', []


def parse_workplace(df):
    for i in range(len(df)):
        if df.at[i, 'parsed_workplace'] == '':
            orig_name = df.at[i, 'Место работы']
            rows = df['Место работы'].str.lower() == orig_name.lower()
            parsed_name, coords = get_name_coords(orig_name)

            df.loc[rows, 'parsed_workplace'] = parsed_name
            if coords:
                df.loc[rows, 'lon'] = coords[1]
                df.loc[rows, 'lat'] = coords[0]

            time.sleep(1)
    return df


def save_processed_workplace(df, path):
    workplace_data = df[['Место работы']].copy()
    workplace_data['Место работы'] = workplace_data['Место работы'].fillna('')
    workplace_data['Место работы'] = workplace_data['Место работы'].str.replace('\'', '').str.replace('"', '')
    workplace_data['Место работы'] = workplace_data['Место работы'].str.replace('»', '').str.replace('«', '')
    workplace_data['parsed_workplace'] = ''
    workplace_data['lat'] = -1000.
    workplace_data['lon'] = -1000.
    workplace_data.to_csv(path, index_label='index')


if __name__ == '__main__':
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)
    workplace_data = pd.read_csv(config['workplace_output'], index_col=False)
    workplace_data['parsed_workplace'] = workplace_data['parsed_workplace'].fillna('')
    workplace_data = parse_workplace(workplace_data)
    workplace_data.to_csv(config['workplace_output'], index_label='index')
