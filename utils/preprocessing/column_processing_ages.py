import pandas as pd
import numpy as np


def get_year_of_employment(data):
    strr = data['Начало трудового стажа']
    vv1 = strr.str.findall('(\d{8})')
    vv2 = strr.str.findall('(\d{4})')
    vv3 = strr.str.findall('[а-я][а-я].\d\d')

    for i in range(0, 713):
        if type(vv2[i]) == list:
            if (len(vv2[i]) > 0):
                vv3[i] = vv2[i][0]
            else:
                if (len(vv3[i]) > 0):
                    if int(vv3[i][0][-2:]) > 24:
                        vv3[i] = "19" + vv3[i][0][-2:]
                    else:
                        vv3[i] = "20" + vv3[i][0][-2:]
    for i in range(0, 713):
        if type(vv1[i]) == list:
            if (len(vv1[i]) > 0):
                vv3[i] = vv1[i][0][4:8]
    stag_work = []
    for k in range(0, len(vv3)):
        try:
            res = 2023 - int(vv3[k])
            stag_work.append(res)
        except:
            stag_work.append(np.NaN)
    return vv3, stag_work


def get_year_of_birth(data):
    sta = data['Дата рождения']
    ddt = sta.str.findall('(\d{4})')
    res_bir_date = []
    for l in range(0, len(ddt)):
        if type(ddt[l]) == list:
            if len(ddt[l]) > 0:
                if int(ddt[l][0]) > 1900 and int(ddt[l][0]) < 2100:
                    res_bir_date.append(ddt[l][0])
                else:
                    res_bir_date.append(np.NaN)
            else:
                res_bir_date.append(np.NaN)
        else:
            res_bir_date.append(ddt[l])
    return res_bir_date


def get_age(res_bir_date):
    age = []
    for m in range(0, len(res_bir_date)):
        if pd.isna(res_bir_date[m]) == False:
            res_age = 2023 - int(res_bir_date[m])
            age.append(res_age)
        else:
            age.append(np.NaN)
    return age


def get_starting_work_at_rosatom(data):
    ros_at = data['Начало трудовой деятельности в РОСАТОМ']
    data_ros = ros_at.str.findall('(\d{4})')
    res_ros_date = []
    for l in range(0, len(data_ros)):
        if type(data_ros[l]) == list:
            if len(data_ros[l]) > 0:
                if int(data_ros[l][0]) > 1900 and int(data_ros[l][0]) < 2100:
                    res_ros_date.append(data_ros[l][0])
                else:
                    res_ros_date.append(np.NaN)

            else:
                res_ros_date.append(np.NaN)
        else:
            res_ros_date.append(data_ros[l])
    return res_ros_date


def get_work_experience_at_rosatom(res_ros_date):
    age_ros = []
    for m in range(0, len(res_ros_date)):
        if pd.isna(res_ros_date[m]) == False:
            res_age_ros = 2023 - int(res_ros_date[m])
            age_ros.append(res_age_ros)
        else:
            age_ros.append(np.NaN)
    return age_ros


def gusev_get_category(data):
    data['год начала стажа'], data['опыт работы'] = get_year_of_employment(data)
    data['Год рождения'] = get_year_of_birth(data)
    data['Возраст'] = get_age(data['Год рождения'])
    data['Начало работы в Росатоме'] = get_starting_work_at_rosatom(data)
    data['Стаж работы Росатом'] = get_work_experience_at_rosatom(data['Начало работы в Росатоме'])

    return data
