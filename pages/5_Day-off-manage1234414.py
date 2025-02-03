import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import calendar 
from PIL import Image

from streamlit.components.v1 import html

from html_shortcuts import *
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

def run_query(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        columnsnames=cur.column_names
        return cur.fetchall(),columnsnames
    
def format_year(year):
    return "{:d}".format(year)  
    
def main():
    


    conn = init_connection()
    st.set_page_config(page_title="DayOff Management")

    st.title("Day Off Management")
    st.markdown("""
        <style>

            /*the main div*/
            .css-1v0mbdj {
                width: 100px; /*max value according to image width, can be smaller but not larger*/
                height: 100px;
                position: relative;
                border:3px solid #d1d1d1;
                overflow: hidden;
                border-radius: 50%;
            }
            
            /*the img elements in the main div class*/
            .css-1v0mbdj > img{
                display: inline;
                margin: 0 auto;
                margin-top: 4%; /*Tweak this one according to your need*/
            }
        
        </style>
        """, unsafe_allow_html=True)

    sql = f"""
      SELECT kimai2_users.id, kimai2_users.alias as name FROM `kimai2_users`;
    """
    rows,columnames = run_query(conn,sql)

    # st.write(columnames)
    dfdata=pd.DataFrame(rows,columns=columnames)
    dfdata=dfdata[dfdata['name']!='ADMINISTRATOR']
    st.write("Get all user list",dfdata)




    optionlist =dfdata['name'].unique().tolist()
    options = optionlist
    selected_option = st.selectbox('Select User', options)
    df1 = dfdata[dfdata['name'] == selected_option]
    userid=df1['id'].iloc[0]
    st.write(userid)

    ##get user daysoff total
    st.title("User Dayoff Total")

    # sql = f""" 
    #     SELECT start_time FROM `kimai2_timesheet` WHERE (activity_id=4 OR activity_id=115 OR activity_id=116) AND user={userid};
    # """
    sql = f"""
        SELECT
        start_time,
        CASE
            WHEN activity_id = 4 THEN 'Normal'
            WHEN activity_id = 115 THEN 'Sick'
            WHEN activity_id = 116 THEN 'Educational'
            ELSE 'Other'
        END AS category
        FROM `kimai2_timesheet`
        WHERE (activity_id = 4 OR activity_id = 115 OR activity_id = 116) AND user = {userid};
    """
    rows,columnames = run_query(conn,sql)
    dfdaysofftotal=pd.DataFrame(rows,columns=columnames)
    dfdaysofftotal['Year'] = dfdaysofftotal['start_time'].dt.year
    st.write(dfdaysofftotal)

    #dfdaysoff2=dfdaysoff2[dfdaysoff2['Year']==selected_option]

    ##YEAR SELECTION START
    yearlist=dfdaysofftotal['Year'].unique().tolist()
    options2 = yearlist
    selected_option = st.selectbox('Select Year', options2)
    dfdaysoffYear=dfdaysofftotal[dfdaysofftotal['Year']==selected_option]
    st.write(dfdaysoffYear)
    ##YEAR SELECTION END


    ##START Query for kanoniki adeia 
    

    # sql = f"""
    #     SELECT start_time FROM `kimai2_timesheet` WHERE activity_id=4 and user={userid};
    #     """
    # rows,columnames = run_query(conn,sql)

    # # st.write(columnames)
    # dfdaysoff=pd.DataFrame(rows,columns=columnames)
    # st.write("All Days Off for current user",dfdaysoff)
    # useddaysoff=len(dfdaysoff['start_time'])
    # st.write("Total DaysOff has beeb used until now:",useddaysoff)

    # dfdaysoff['Year'] = dfdaysoff['start_time'].dt.year
    # dfdaysoff['Year'] = dfdaysoff['Year'].apply(format_year)

    # # yearlist=dfdaysofftotal['Year'].unique().tolist()
    # # options2 = yearlist
    # # selected_option = st.selectbox('Select User', options2)
    # st.write(dfdaysoff)
    #dfdaysoff=dfdaysoff[dfdaysoff['Year']==selected_option]
    dfdaysoff=dfdaysoffYear[dfdaysoffYear['category']=='Normal']
    useddaysoff=len(dfdaysoff['start_time'])
    if(useddaysoff!=0):
        st.title("Normal Dayoff")
        st.write(dfdaysoff)
        st.write("Total DaysOff has beeb used until now:",useddaysoff)
    ##END Query for kanoniki adeia 


    ##START Query for Asthenia adeia
    # sql = f"""
    #     SELECT start_time FROM `kimai2_timesheet` WHERE activity_id=115 and user={userid};
    #     """
    # rows,columnames = run_query(conn,sql)

    # # st.write(columnames)
    # sickdaysoff=pd.DataFrame(rows,columns=columnames)
    sickdaysoff=dfdaysoffYear[dfdaysoffYear['category']=='Sick']

    usersickdayoff=len(sickdaysoff['start_time'])
    if(usersickdayoff!=0):
        # st.write(sickdaysoff)
        sickdaysoff['Year'] = sickdaysoff['start_time'].dt.year
        sickdaysoff=sickdaysoff[sickdaysoff['Year']==selected_option]

        st.title("Sickness Dayoff")
        st.write("All Days Off for sickness user",sickdaysoff)
        st.write("Total DaysOff has beeb used until now:",usersickdayoff)
        with open("animated_counter.js", "r") as file:
            js_code = file.read()
        with st.container():
            html_content2 = html_days4(js_code,usersickdayoff)
            html(html_content2,height=250)
    ##END Query for Asthenia adeia


    ##START Query for Education adeia
    # sql = f"""
    #     SELECT start_time FROM `kimai2_timesheet` WHERE activity_id=116 and user={userid};
    #     """
    # rows,columnames = run_query(conn,sql)

    # # st.write(columnames)
    # edudaysoff=pd.DataFrame(rows,columns=columnames)
    edudaysoff=dfdaysoffYear[dfdaysoffYear['category']=='Educational']
    useredudayoff=len(edudaysoff['start_time'])
    if(useredudayoff!=0):
        st.title("Educational Dayoff")
        st.write("All Days Off for edu user",edudaysoff)
        st.write("Total edu DaysOff has beeb used until now:",useredudayoff)
        with open("animated_counter.js", "r") as file:
            js_code = file.read()
        with st.container():
            html_content2 = html_days5(js_code,useredudayoff)
            html(html_content2,height=250)
    ##END Query for Education adeia



    st.title("Total Days off for this user")
    sql = f"""
      SELECT kimai2_daysoff.total_daysoff, kimai2_daysoff.user_id,kimai2_users.alias,kimai2_users.avatar
 FROM `kimai2_daysoff`
 INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_daysoff.user_id
 WHERE  `user_id`={userid};
        """
    rows,columnames = run_query(conn,sql)


    # st.write(columnames)
    dfdata2=pd.DataFrame(rows,columns=columnames)
    if(not dfdata2.empty):
        
        st.write(dfdata2)
        imagepath=dfdata2['avatar'].iloc[0]

        if pd.isna(imagepath):
            st.image('noimage.png',width=350,use_column_width="auto")
        else:
            st.image(imagepath,width=350,use_column_width="auto")

        st.write("All Days Off for current user",dfdata2)

        total_daysoff=dfdata2['total_daysoff'].iloc[0]
        remaindays=total_daysoff-useddaysoff
        st.write("Remainig Days of:",remaindays)


        with open("animated_counter.js", "r") as file:
            js_code = file.read()
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                html_content3 = html_days3(js_code,remaindays)
                html(html_content3,height=250)
    

            with col2:
                html_content2 = html_days2(js_code,useddaysoff)
                html(html_content2,height=250)
            with col3:
                html_content1 = html_days1(js_code,total_daysoff)
                html(html_content1,height=250)



        labels = ['Remaining Days','Used Days']
        values = [remaindays, useddaysoff ]

        colors = ['green', 'red']

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors ))
        st.plotly_chart(fig)


    # Assuming you have DataFrames 'dfdaysoff', 'dfsickdays', and 'dfthird' with 'start_time' columns
    dfdaysoff['start_time'] = pd.to_datetime(dfdaysoff['start_time'])

    # Check if dfsickdays is not empty
    if not sickdaysoff.empty:
        sickdaysoff['start_time'] = pd.to_datetime(sickdaysoff['start_time'])
        monthly_sick_counts = sickdaysoff.groupby(sickdaysoff['start_time'].dt.month).size().reset_index(name='Sick_Count')
    else:
        # Create an empty DataFrame with the expected columns if dfsickdays is empty
        monthly_sick_counts = pd.DataFrame(columns=['start_time', 'Sick_Count'])

    # Check if dfthird is not empty
    if not edudaysoff.empty:
        edudaysoff['start_time'] = pd.to_datetime(edudaysoff['start_time'])
        monthly_third_counts = edudaysoff.groupby(edudaysoff['start_time'].dt.month).size().reset_index(name='edu_Count')
    else:
        # Create an empty DataFrame with the expected columns if dfthird is empty
        monthly_third_counts = pd.DataFrame(columns=['start_time', 'edu_Count'])

    # Group by month and count the occurrences for daysoff
    monthly_daysoff_counts = dfdaysoff.groupby(dfdaysoff['start_time'].dt.month).size().reset_index(name='Daysoff_Count')

    # Create a DataFrame with all months (1 to 12)
    all_months = pd.DataFrame({'start_time': range(1, 13)})

    # Merge the DataFrames to ensure all months are included
    monthly_counts = all_months.merge(monthly_daysoff_counts, on='start_time', how='left').fillna(0)
    monthly_counts = monthly_counts.merge(monthly_sick_counts, on='start_time', how='left').fillna(0)
    monthly_counts = monthly_counts.merge(monthly_third_counts, on='start_time', how='left').fillna(0)

    # Create a bar plot using Plotly Express for daysoff, sickdays, and the third category
    fig = px.bar(monthly_counts, x='start_time', y=['Daysoff_Count', 'Sick_Count', 'edu_Count'],
                labels={'start_time': 'Month', 'value': 'Count'}, title='Count of Dates by Month')
    fig.update_xaxes(type='category', tickmode='array', tickvals=list(range(1, 13)),
                    ticktext=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    fig.update_layout(yaxis_title='Count')

    #Show the combined plot
    st.plotly_chart(fig)




####################################################################
############ADMINISTRATION PART EDIT ##############################

    st.title("Edit Days off")
    id=st.number_input("Enter ID",userid)
    total_days=st.number_input("Enter total days off",min_value=0,value=total_daysoff)





    # fig = px.pie(dfgroup, values='duration', names='name',
    #             title='% Διάρκεια ανα Project επί του Συνόλου  ',
    #             hover_data=['duration'], labels={'duration':'duration'})
    #             fig.update_traces(textposition='inside', textinfo='percent+label')
    #             st.plotly_chart(fig)

    if st.button("Update"):
        sql="update kimai2_daysoff  set kimai2_daysoff.total_daysoff=%s where kimai2_daysoff.user_id=%s"
        val=(total_days,id)
        with conn.cursor() as cur:
            cur.execute(sql,val)
            conn.commit()
            st.success("Record Updated Successfully")
            st.experimental_rerun()









if __name__ == '__main__':
    main()
