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
    st.write("Get all user list",dfdata)



    optionlist =dfdata['name'].unique().tolist()
    options = optionlist
    selected_option = st.selectbox('Select User', options)
    df1 = dfdata[dfdata['name'] == selected_option]
    userid=df1['id'].iloc[0]
    st.write(userid)


    st.title("User Analytics Dayoff")
    sql = f"""

SELECT start_time FROM `kimai2_timesheet` WHERE activity_id=4 and user={userid};
        """
    rows,columnames = run_query(conn,sql)

    # st.write(columnames)
    dfdaysoff=pd.DataFrame(rows,columns=columnames)
    st.write("All Days Off for current user",dfdaysoff)
    useddaysoff=len(dfdaysoff['start_time'])
    st.write("Total DaysOff has beeb used until now:",useddaysoff)







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
