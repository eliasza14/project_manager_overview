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
    dfdata.loc[:, 'duration'] = dfdata['duration'] // 3600

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


    st.title("User Overview")
    st.plotly_chart(fig)

    rows,columnames = run_query(conn,sql2)

    # st.write(columnames)
    dfdata2=pd.DataFrame(rows,columns=columnames)
    dfdata2.loc[:, 'duration'] = dfdata2['duration'] // 3600
    dfdata2=dfdata2.sort_values('duration', ascending=False)
    st.write("All Data from Query",dfdata2)


    fig2 = go.Figure(go.Bar(
    x=dfdata2['duration'].tolist(),
    y=dfdata2['alias'].tolist(),
    orientation='h'))

    fig2.update_layout(title="Users Total Working Hours",yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig2)

    st.title("Select User from the below list:")
        # List of options for the dropdown menu
    optionlist =dfdata2['alias'].tolist()
    options = optionlist

    # Display the dropdown menu
    selected_option = st.selectbox('Choose User', options)
    df1 = dfdata2[dfdata2['alias'] == selected_option]
    # df1['duration']=df1['duration']/3600
    # df1.loc[:, 'duration'] = df1['duration'] / 3600
    first_duration_value = df1['duration'].iloc[0]
    first_alias_value = df1['alias'].iloc[0]
    text="**Total** **duration** **is:** **"+str(first_duration_value)+"** **Hours** **\u23F0** "
    #st.write(first_alias_value)
    #st.markdown(text)
    st.title(text)
    userdf = dfdata.loc[dfdata['alias']==first_alias_value]

    st.write(userdf)

    fig3 = px.pie(userdf, values='duration', names='name',
             title='User Project durations',
             hover_data=['duration'], labels={'duration':'duration'})
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig3)

    st.title("Select Project from the below list")
    
    optionlist =userdf['name'].tolist()
    options2 = optionlist
    selected_option = st.selectbox('Choose Project', options2)
    df2 = userdf[userdf['name'] == selected_option]
    st.write(df2)







if __name__ == '__main__':
    main()


