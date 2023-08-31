import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import calendar 
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

SELECT start_time,duration FROM `kimai2_timesheet` WHERE activity_id=4 and user={userid};
        """
    rows,columnames = run_query(conn,sql)

    # st.write(columnames)
    dfdaysoff=pd.DataFrame(rows,columns=columnames)
    dfdaysoff['duration']=dfdaysoff['duration'] // 3600
    st.write("All Days Off for current user",dfdaysoff)







    st.title("Total Days off for this user")
    sql = f"""
      SELECT kimai2_daysoff.total_daysoff, kimai2_daysoff.user_id,kimai2_users.alias
 FROM `kimai2_daysoff`
 INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_daysoff.user_id
 WHERE  `user_id`={userid};
        """
    rows,columnames = run_query(conn,sql)

    # st.write(columnames)
    dfdata2=pd.DataFrame(rows,columns=columnames)
    st.write("All Days Off for current user",dfdata2)
    total_daysoff=dfdata2['total_daysoff'].iloc[0]

    st.title("Edit Days off")
    id=st.number_input("Enter ID",userid)
    total_days=st.number_input("Enter total days off",min_value=0,value=total_daysoff)
    if st.button("Update"):
        sql="update kimai2_daysoff  set kimai2_daysoff.total_daysoff=%s where kimai2_daysoff.user_id=%s"
        val=(total_days,id)
        with conn.cursor() as cur:
            cur.execute(sql,val)
            conn.commit()
            st.success("Record Updated Successfully")







if __name__ == '__main__':
    main()
