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





if __name__ == '__main__':
    main()


