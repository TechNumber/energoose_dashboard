import pandas as pd


def get_interval_groups(data):
    exp_intervals = [0, 1, 3, 6, 13, 30]
    age_intervals = [14, 24, 40, 65, 100]
    score_intervals = [0, 20, 40, 60, 80, 100]

    data['Группировка по опыту работы'] = \
        pd.cut(data['опыт работы'], bins=exp_intervals, labels=['0-1', '1-3', '3-6', '6-13', '14+'])
    data['Группировка по опыту в Росатоме'] = \
        pd.cut(data['Стаж работы Росатом'], bins=exp_intervals, labels=['0-1', '1-3', '3-6', '6-13', '14+'])
    data['Группировка по возрасту'] = \
        pd.cut(data['Возраст'], bins=age_intervals, labels=['14-24', '25-40', '41-65', '65+'])
    data['Группировка по баллам'] = \
        pd.cut(data['Баллы, %'], bins=score_intervals, labels=['0-20', '20-40', '40-60', '60-80', '80-100'])
    return data
