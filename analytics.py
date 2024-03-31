import psycopg2
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style("whitegrid")


def get_connection_to_db():
    USERNAME = "DWH_owner"
    PASSWORD = os.environ['start_in_ds_password']
    HOST = "ep-shiny-cake-a2v20jar.eu-central-1.aws.neon.tech"
    DATABASE = "DWH"
    conn_str = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?sslmode=require'
    conn = psycopg2.connect(conn_str)
    return conn

def get_main_data_from_db(conn):
    data = pd.read_sql_query(f'''
        select * from salaries_with_inflation
    ''', conn)
    data['Гостиницы_и_общепит_реал'] = data['Гостиницы_и_общепит'] / (1 + data['Годовая_инфляция'] / 100)
    data['Финансы_и_страхование_реал'] = data['Финансы_и_страхование'] / (1 + data['Годовая_инфляция'] / 100)
    data['Образование_реал'] = data['Образование']  / (1 + data['Годовая_инфляция'] / 100)

    prev_year = data[['Гостиницы_и_общепит_реал', 'Финансы_и_страхование_реал', 'Образование_реал']].shift(1).rename(columns={
        'Гостиницы_и_общепит_реал': 'Гостиницы_и_общепит_пред_год', 
        'Финансы_и_страхование_реал': 'Финансы_и_страхование_пред_год', 
        'Образование_реал': 'Образование_пред_год'
    })

    data = pd.concat([data, prev_year], axis=1)
    data['Гостиницы_и_общепит_прирост'] = (data['Гостиницы_и_общепит_реал'] / data['Гостиницы_и_общепит_пред_год'] - 1) * 100
    data['Финансы_и_страхование_прирост'] = (data['Финансы_и_страхование_реал'] / data['Финансы_и_страхование_пред_год'] - 1) * 100
    data['Образование_прирост'] = (data['Образование_реал'] / data['Образование_пред_год'] - 1) * 100

    return data

def get_extra_data_from_db(conn):
    data = pd.read_sql_query(f'''
        select * from extra_metrics
    ''', conn)
    return data

def create_plot_1(data):
    fig, ax = plt.subplots()
    ax.plot(data['Год'], data['Гостиницы_и_общепит'], 'g', label='Гостиницы и общепит (номинальная зп)')
    ax.plot(data['Год'], data['Финансы_и_страхование'],'r',label='Финансы и страхование (номинальная зп)')
    ax.plot(data['Год'], data['Образование'], 'b', label='Образование (номинальная зп)')
    ax.legend(loc='best')
    ax.set_title("Динамика номинальных зарплат в России")
    return fig, ax

def create_plot_2(data):
    fig, ax = plt.subplots()
    ax.plot(data['Год'], data['Гостиницы_и_общепит'], '--', label='Гостиницы и общепит (номин)')
    ax.plot(data['Год'], data['Финансы_и_страхование'],'--',label='Финансы и страхование (номин)')
    ax.plot(data['Год'], data['Образование'], '--', label='Образование (номин)')
    ax.plot(data['Год'], data['Гостиницы_и_общепит_реал'], label='Гостиницы и общепит (реал)')
    ax.plot(data['Год'], data['Финансы_и_страхование_реал'], label='Финансы и страхование (реал)')
    ax.plot(data['Год'], data['Образование_реал'], label='Образование (реал)')
    ax.legend(loc='best')
    ax.set_title('Номинальные и реальные зарплаты в России')
    return fig, ax

def create_plot_3(data):
    fig, ax = plt.subplots()
    ax.plot(data['Год'], data['Гостиницы_и_общепит_прирост'], label='Гостиницы и общепит', alpha=0.5)
    ax.plot(data['Год'], data['Финансы_и_страхование_прирост'],label='Финансы и страхование', alpha=0.5)
    ax.plot(data['Год'], data['Образование_прирост'], label='Образование', alpha=0.5)
    ax.plot(data['Год'], data['Годовая_инфляция'], label='Годовая инфляция')
    ax.legend(loc='best')
    ax.set_title('Темпы инфляции и изменения зарплат по сравнению с предыдущим годом')
    return fig, ax



    