import pandas as pd
from difflib import SequenceMatcher


# Определение схожести строк
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_category(df):
    # Загрузка набора данных
    # df = pd.read_csv(file_path)

    # Словарь "Должность-категория" для значений без пропусков
    categorized_vals = dict()
    for i in range(len(df)):
        if str(df['Категория'][i]) not in ['nan', 'Нет'] \
                and str(df['Должность'][i]) not in ['nan', 'Нет']:
            categorized_vals.update({str(df['Должность'][i]): str(df['Категория'][i])})

    # Наполнение столбца "Категория" на основе схожести строк столбца "Должность" и ключей словаря выше
    catcol = []
    for i in range(len(df)):
        category = df['Категория'][i]
        if str(category) in ['nan', 'Нет']:
            category = 'Не указано'
        for c_val in categorized_vals.keys():
            if (similar(str(df['Должность'][i]), c_val) >= 0.45):
                category = categorized_vals.get(c_val)
        catcol.append(category)

    df['EX-Категория'] = catcol
    return df
