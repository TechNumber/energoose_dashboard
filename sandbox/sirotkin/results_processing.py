import pandas as pd
import os
import glob

def appendScores(data, csv_folder):
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, csv_folder+'/*.csv'))
    
    res_df = pd.DataFrame()
    name_col = []
    score_col = []
    team_col = []
    names_n_scores = dict()
    for f in csv_files:
        df = pd.read_csv(f)
        for col in df.columns:
            if 'ФИО' in col:
                ncol_name = col
        for i in range(len(df)):
            names_n_scores.update({df[ncol_name][i]:df['Баллы, %'][i]})
            
    names_n_scores = list(names_n_scores.items())
    for i in range(len(names_n_scores)):
        if 'ФИО' not in names_n_scores[i][0]:
            pass
        else:
            for name in names_n_scores[i][0].split('; '):
                name_col.append(name)
                score = float(str(names_n_scores[i][1]).replace(',','.').replace('%',''))
                score_col.append(score)
                if len(names_n_scores[i][0].split('; '))>1:
                    team_col.append(True)
                else:
                    team_col.append(False)
                    
    res_df['ФИО'] = name_col
    res_df['Баллы, %'] = score_col
    res_df['Участвовал в команде'] = team_col
    
    res_df = res_df.dropna()
    
    return data.merge(res_df, on = 'ФИО')

df = pd.read_csv('Участники anonimized.csv')
newdf = appendScores(df,'Results')