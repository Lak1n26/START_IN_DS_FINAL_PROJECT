import streamlit as st
from analytics import get_connection_to_db, get_main_data_from_db, create_plot_1, create_plot_2, create_plot_3, get_extra_data_from_db
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from PIL import Image


if __name__ == '__main__':
    st.title("Анализ зарплат в России")
    image = Image.open('image.jpg')
    st.image(image) 
    st.write(f'''
                Рассмотрим динамику заработных плат в России по видам экономической деятельности на примере трех отраслей:
                - Деятельность гостиниц и предприятий общественного питания
                - Финансовая и страховая деятельность
                - Образование
             
                Анализируемые период: 2000 - 2023 гг.
             
             ''')
    st.write('#### Номинальные зарплаты, годовая инфляция, реальные зарплаты и темпы изменения реальных зарплат')
    conn = get_connection_to_db()
    data = get_main_data_from_db(conn)
    st.dataframe(data)
    fig1, ax1 = create_plot_1(data)
    st.pyplot(fig1)
    st.write('Темпы роста номинальной заработной платы "Гостиниц и общепита" и "Образования" практические совпадают. Темпы рост номинальной зп у "Финансов и страхования" значительно выше.')
    fig2, ax2 = create_plot_2(data)
    st.pyplot(fig2)
    fig3, ax3 = create_plot_3(data)
    st.pyplot(fig3)
    st.write('В среднем темпы изменения зарплат по данным отраслям обгоняют темпы инфляции, но наблюдаются "кризисные" годы, когда эта тенденция нарушается: 2008, 2014 и т.д.')

    corr_fig1, corr_ax1 = plt.subplots()
    sns.heatmap(data[['Годовая_инфляция', 'Гостиницы_и_общепит_реал',
       'Финансы_и_страхование_реал', 'Образование_реал']].corr(), ax=corr_ax1, annot=True, linewidth=.5, cmap='crest')
    corr_ax1.set_title('Корреляция')
    st.pyplot(corr_fig1)

    st.write('#### Дополнительное исследование: связь важных экономических показателей с реальными зарплатами')
    extra_metrics = get_extra_data_from_db(conn)
    st.dataframe(extra_metrics)
    data = data.merge(extra_metrics)
    corr_fig2, corr_ax2 = plt.subplots()
    sns.heatmap(data[['Годовая_инфляция', 'Гостиницы_и_общепит_реал',
       'Финансы_и_страхование_реал', 'Образование_реал', 'ВВП_на_душу_населения', 'Доля_занятых_лиц_в_общей_численнос',
        'Уровень_безработицы', 'Доля_заработной_платы_в_ВВП',
        'Уровень_счастья']].corr()[['Гостиницы_и_общепит_реал',
       'Финансы_и_страхование_реал', 'Образование_реал']], ax=corr_ax2, annot=True)
    corr_ax2.set_title('Корреляция между зарплатами и важными экономическими показателями')
    st.pyplot(corr_fig2)
    st.write('''**Наибольшая корреляция реальных зарплат в России наблюдается с "ВВП на душу населения". С безработицей же наблюдается обратно пропорциональная зависимость: 
             когда безработица высока, спрос на рабочую силу снижается, что часто сопровождается снижением заработной платы (подтверждением этому служит Кривая Филлипса).**''')