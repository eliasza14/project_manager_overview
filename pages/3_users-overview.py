import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

def run_query(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        columnsnames=cur.column_names
        return cur.fetchall(),columnsnames
    


def main():
    conn = init_connection()
    st.set_page_config(page_title="User Overview")
    st.title("User Overview")
    sql = """SELECT kimai2_projects.name,kimai2_users.alias,SUM(kimai2_timesheet.duration) as duration ,MIN(kimai2_timesheet.start_time) as startime,MAX(kimai2_timesheet.start_time) as lasttime,kimai2_projects.visible
FROM `kimai2_timesheet`
INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
INNER JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
GROUP BY kimai2_users.alias,kimai2_projects.name,kimai2_projects.visible;"""

    sql2 ="""SELECT kimai2_users.alias,SUM(kimai2_timesheet.duration) as duration 
FROM `kimai2_timesheet`
INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
GROUP BY kimai2_users.alias; """

    

    rows,columnames = run_query(conn,sql)

# st.write(columnames)
    dfdata=pd.DataFrame(rows,columns=columnames)
    st.write("All Data from Query",dfdata)


    dfgroup=dfdata.groupby(['alias'])['name'].count()

    dfgroup2=dfdata.groupby('alias')['name'].agg(list).reset_index()


    dfframe=dfgroup.to_frame().reset_index()

    userlist=dfframe['alias'].tolist()

    countlist=dfframe['name'].tolist()

    # dfgroup2

    for i in range(len(dfgroup2)):
        dfgroup2['name'][i] = '<br>'.join(dfgroup2['name'][i]).replace(',', ',<br>')






    st.write(dfgroup2)


           # Create the pie chart using Plotly Express
    fig = px.pie(dfgroup2, values=countlist, names='alias', hover_data=[dfgroup2['name']],labels={'alias':'User',
                                                                                                        'values':'Project count',
                                                                                                        'name':'Projects'})
    fig.update_traces(textposition='inside', textinfo='label+value')

    # Display the pie chart


    st.title("Project Manager Overview")
    st.plotly_chart(fig)

    rows,columnames = run_query(conn,sql2)

    # st.write(columnames)
    dfdata2=pd.DataFrame(rows,columns=columnames)
    st.write("All Data from Query",dfdata2)


    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    import numpy as np

    y_saving = [1.3586, 2.2623000000000002, 4.9821999999999997, 6.5096999999999996,
                7.4812000000000003, 7.5133000000000001, 15.2148, 17.520499999999998
                ]
    y_net_worth = [93453.919999999998, 81666.570000000007, 69889.619999999995,
                78381.529999999999, 141395.29999999999, 92969.020000000004,
                66090.179999999993, 122379.3]
    x = ['Japan', 'United Kingdom', 'Canada', 'Netherlands',
        'United States', 'Belgium', 'Sweden', 'Switzerland']


    # Creating two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=y_saving,
        y=x,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Household savings, percentage of household disposable income',
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=y_net_worth, y=x,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Household net worth, Million USD/capita',
    ), 1, 2)

    fig.update_layout(
        title='Household savings & net worth for eight OECD countries',
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.47, 1],
            side='top',
            dtick=25000,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
    )

    annotations = []

    y_s = np.round(y_saving, decimals=2)
    y_nw = np.rint(y_net_worth)

    # Adding labels
    for ydn, yd, xd in zip(y_nw, y_s, x):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn - 20000,
                                text='{:,}'.format(ydn) + 'M',
                                font=dict(family='Arial', size=12,
                                        color='rgb(128, 0, 128)'),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 3,
                                text=str(yd) + '%',
                                font=dict(family='Arial', size=12,
                                        color='rgb(50, 171, 96)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=-0.109,
                            text='OECD "' +
                                '(2015), Household savings (indicator), ' +
                                'Household net worth (indicator). doi: ' +
                                '10.1787/cfc6f499-en (Accessed on 05 June 2015)',
                            font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    st.plotly_chart(fig)












if __name__ == '__main__':
    main()


