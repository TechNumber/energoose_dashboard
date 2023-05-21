import pandas as pd

import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback, dash_table

INPUT_FILE_PATH = 'clustered_data/clustered.csv'

df = pd.read_csv(INPUT_FILE_PATH)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
filters = ["по полу", "по компетенции", "по возрасту"]
filter_dict = {"по полу": "Пол",
               "по компетенции":
               "Список компетенций",
               "по возрасту": "Группировка по возрасту"}

filter_choose_block = dbc.Card(
    [
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Фильтровать результаты: "), ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="filter",
                                options=filters,
                                value="по возрасту",
                            ),
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="filter2",
                                options=[],
                                value=df[filter_dict["по возрасту"]].unique()[0],
                                disabled=True

                            ),
                        )

                    ],
                    id="filters_container"
                ),
            ]
        )
    ]
)


@callback(
    Output("filters_container", "children"),
    Input("filter", "value"),
)
def filter_paste(filter):
    return dbc.Row(
        [
            dbc.Col(dbc.Label("Фильтровать результаты: "), ),
            dbc.Col(
                dcc.Dropdown(
                    id="filter",
                    options=filters,
                    value=filter,
                ),
            ),
            dbc.Col(dbc.Label(f"Выберите {filter_dict[filter]}: "), ),
            dbc.Col(
                dcc.Dropdown(
                    id="filter2",
                    options=df[filter_dict[filter]].unique(),
                    value=df[filter_dict[filter]].unique()[0]
                ),
            )
        ]
    )


app.layout = dbc.Container(
    [
        html.H4(
            "Интерактивный дэщборд чемпионата AtomSkills",
            style={"textAlign": "center"},
            className="mb-3",
        ),
        html.Hr(),
        filter_choose_block,
        dcc.Tabs(
            id="tab",
            value="base",
            children=[
                dcc.Tab(label="Общая инфографика", value="base"),
                dcc.Tab(label="Результаты кластеризации", value="clas"),
                dcc.Tab(label="Демографическая статистика", value="dem"),
                dcc.Tab(label="Результаты чемпионатов", value="res"),
            ],
        ),
        html.Div(id="content"),
    ],
    fluid=True,
)

@callback(
    Output("content", "children"),
    Input("filter", "value"),
    Input("filter2", "value"),
    Input("tab", "value"),
)
def update_content(filter1, filter2, tab):
    if tab == 'dem':
        fdf = df
        if filter1 != "нет":
            fdf = df[df[filter_dict[filter1]] == filter2]
        dff = fdf.groupby(['Пол'])['Пол'].count().reset_index(name="Кол-во")
        fig1 = px.pie(dff, values="Кол-во", names="Пол", title="Соотношение гендеров")
        dff2 = fdf.groupby(['Группировка по возрасту'])['Группировка по возрасту'].count().reset_index(name='Кол-во')
        fig2 = px.pie(dff2, values="Кол-во", names="Группировка по возрасту", title="Соотношение возрастов")
        demographic_stat_block = dbc.Card(
            [
                dbc.Label("Демографическая статистика участников", style={"textAlign": "center"}, ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(figure=fig1)),
                        dbc.Col(
                            dcc.Graph(figure=fig2))
                    ]
                )
            ]
        )
        return demographic_stat_block
    elif tab == 'base':
        dff = df.groupby(['Группировка по возрасту'])['Группировка по возрасту'].count().reset_index(name='Кол-во')
        fig1 = px.pie(dff, values="Кол-во", names="Группировка по возрасту", title="Соотношение возрастов")
        dff2 = df.groupby(['Список компетенций'])['Список компетенций'].count().reset_index(name='Кол-во').sort_values(['Кол-во'], ascending=False)[1:16]
        fig2 = px.pie(dff2, values="Кол-во", names="Список компетенций", title="Популярные компитенции")
        dff3 = df.groupby(['Список компетенций'])['Список компетенций'].count().reset_index(name='Кол-во')
        dff3['Средний балл'] = df.groupby(['Список компетенций'])['Баллы, %'].mean().reset_index(name='Средний балл')['Средний балл']
        dff3['Высший балл'] = df.groupby(['Список компетенций'])['Баллы, %'].max().reset_index(name='Высший балл')['Высший балл']
        dff3 = dff3.sort_values(['Кол-во'], ascending=False)[1:6]
        fig3 = px.bar(dff3, x='Список компетенций', y=['Высший балл', 'Средний балл'], barmode="group")

        base_stat_block = dbc.Card(
            [
                dbc.Label("Демографическая статистика участников", style={"textAlign": "center"}, ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(figure=fig1)),
                        dbc.Col(
                            dcc.Graph(figure=fig2))
                    ]
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig3))
                )
            ]
        )
        return base_stat_block
    else:
        fdf = df
        if filter1 != "нет":
            fdf = df[df[filter_dict[filter1]] == filter2]
        dff = fdf.sort_values(['Баллы, %'], ascending=False)[1:11]
        dff2 = fdf.groupby(['Группировка по баллам'])['Группировка по баллам'].count().reset_index(name='Кол-во')
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=dff2['Группировка по баллам'],
                y=dff2['Кол-во'],
            )
        )
        result_stat_block = dbc.Card(
            [
                dbc.Label("Результаты прохождения чемпионатов", style={"textAlign": "center"}, ),
                dbc.Row(
                    [
                        dash_table.DataTable(
                            dff.to_dict("records"),
                            [{"name": i, "id": i} for i in df.columns],
                            style_table={"overflowX": "auto"},
                        ),
                        dcc.Graph(figure=fig)
                    ]
                ),
            ]
        )
        return result_stat_block


if __name__ == '__main__':
    app.run_server(debug=True, port=8943)
