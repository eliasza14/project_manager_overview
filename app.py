import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state


from datetime import timedelta

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

def run_query(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        columnsnames=cur.column_names
        return cur.fetchall(),columnsnames
    
def update():
    st.session_state.submitted = True
    

def main():


    conn = init_connection()
   
  
    st.set_page_config(page_title="Sidebar Form Example")
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False


    # Define the sidebar form
    with st.sidebar.form("my_sidebar_form"):
        st.write("## date2222 range Form")
        startdate = st.date_input(
        "Give Start Date",
        datetime.date.today())




        enddate = st.date_input(
        "Give End Date",
        datetime.datetime.now() + datetime.timedelta(days=1))

        st.write('Your birthday is:', enddate)

        



        # name = st.text_input("Enter your name:")
        # email = st.text_input("Enter your email:")
        # age = st.number_input("Enter your age:", min_value=0, max_value=120)
        # color = st.selectbox("Choose your favorite color:", ["Red", "Green", "Blue"])
        #submit_button = st.form_submit_button(label="Submit",on_click=update)
        st.form_submit_button(label="Submit",on_click=update)
    # Display the results


    if st.session_state.submitted:
        st.write("Given startdate and endate",startdate)
        st.write("Given startdate and endate",enddate)

        st.write("## Results")
        sql = """SELECT kimai2_timesheet.*,kimai2_users.alias,kimai2_projects.name as project_name,kimai2_activities.name as activity_name FROM kimai2_timesheet 
        INNER JOIN kimai2_users ON kimai2_timesheet.user=kimai2_users.id
        INNER JOIN kimai2_projects ON kimai2_timesheet.project_id=kimai2_projects.id
        INNER JOIN kimai2_activities ON kimai2_timesheet.activity_id=kimai2_activities.id
        """
        sql2="WHERE DATE(start_time) >="+"'"+str(startdate)+"'"+"AND DATE(start_time) <="+"'"+ str(enddate)+"'"+""

    
        rows,columnames = run_query(conn,sql+sql2)

    # st.write(columnames)
        dfdata=pd.DataFrame(rows,columns=columnames)
        st.write("All Data from Query",dfdata)
        st.write('Your birthday is:', startdate)
        st.write('Your birthday is:', enddate)
        
        st.write("## Choose Activity Tag:")

        df1=dfdata.copy()
        # st.write(df1)
        regular_search_term =df1.activity_name.unique().tolist()
        choices = st.multiselect(" ",regular_search_term)
        df1=df1[df1.activity_name.isin(choices)]

        st.write("## Choose User:")

        regular_search_term =df1.alias.unique().tolist()
        choices2 = st.multiselect(" ",regular_search_term + ['All'])


        if 'All' not in choices2:

            df1=df1[df1.alias.isin(choices2)]
            st.write(df1)

        else:
            st.write(df1)
        #Counts Weekly reports per user activity
        st.write("## Weekly Report Comments Count:")
        st.write(df1.groupby(['alias'])['activity_name'].count())
    
        st.write("## Show comment of a user in detail:")
        # List of options for the dropdown menu
        optionlist =df1.alias.unique().tolist()
        options = optionlist

        # Display the dropdown menu
        selected_option = st.selectbox('Choose a user', options)

        # Show the selected option
        st.write('Selected option:', selected_option)
        df1 = df1[df1['alias'] == selected_option]

        st.write("## Show comment of a user per specific project:")
        optionlist =df1.project_name.unique().tolist()
        options = optionlist

        # Display the dropdown menu
        selected_option = st.selectbox('Choose a project name', options+ ['All'])
        if 'All' not in selected_option:
            df1 = df1[df1['project_name'] == selected_option]
        
            
        # Show the selected option
        st.write('Selected option:', selected_option)
        # df1 = df1[df1['alias'] == selected_option]



        st.text(df1["description"])

        st.write("## Zoom In on Specific Comment:")
        optionlistcomment =df1.description.unique().tolist()
        optionscomment = optionlistcomment

        # Display the dropdown menu
        selected_option = st.selectbox('Choose an option', optionscomment)

        # Show the selected option
        # st.write('Selected option:', selected_option)
        df1 = df1[df1['description'] == selected_option]
        df1=df1.reset_index()
        # st.write(df1)
        comment=df1['description'][0]
        st.text(comment)
        # st.text(df1["description"])

        # st.write(df1)

        # with st.form("Form Filter"):
        #     name = st.text_input("Enter your name:")
        #     email = st.text_input("Enter your email:")
        #     submit_button2   = st.form_submit_button(label="Submit2")
        # if submit_button2:

        #     st.write("## Results")
        #     st.write('Your birthday is:', startdate)
        #     st.write('Your birthday is:', enddate)
        #     st.write('name',name)
        #     st.write('email',email)
        # if st.session_state.submitted:

        # st.write(f"Name: {name}")
        # st.write(f"Email: {email}")
        # st.write(f"Age: {age}")
        # st.write(f"Favorite color: {color}")

if __name__ == '__main__':
    main()













# st.write("CMT Timesheets Extended")

# Initialize connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():
#     return mysql.connector.connect(**st.secrets["mysql"])

# conn = init_connection()

# st.write("VERSION 1")
# # cursor=conn.cursor()
# # cursor.execute("USE mproj_db")
# # cursor.close()

# sql = """SELECT kimai2_timesheet.*,kimai2_users.alias,kimai2_projects.name as project_name,kimai2_activities.name as activity_name,kimai2_timesheet_tags.name as tag_name FROM kimai2_timesheet 
# INNER JOIN kimai2_users ON kimai2_timesheet.user=kimai2_users.id
# INNER JOIN kimai2_projects ON kimai2_timesheet.project_id=kimai2_projects.id
# INNER JOIN kimai2_activities ON kimai2_timesheet.activity_id=kimai2_activities.id
# INNER JOIN (SELECT * FROM kimai2_tags INNER JOIN kimai2_timesheet_tags ON kimai2_tags.id=kimai2_timesheet_tags.tag_id ) AS kimai2_timesheet_tags ON kimai2_timesheet.id=kimai2_timesheet_tags.timesheet_id
# """
# # df1=pd.read_sql(sql, conn)
# # st.write(df1)


# # @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         columnsnames=cur.column_names
#         return cur.fetchall(),columnsnames

# rows,columnames = run_query(sql)

# st.write(columnames)
# df1=pd.DataFrame(rows,columns=columnames)



# # df1=pd.read_sql(sql, conn)
# st.write(df1)

# df2=df1[['start_time', 'end_time','duration', 'description', 'rate', 'fixed_rate', 'hourly_rate' , 'internal_rate', 'alias', 'project_name', 'activity_name','tag_name']]
# st.write(df2)
# # st.write(rows)
# # for row in rows:
# #     st.write(f"{row[18]} is :{row[18]}:")

# st.write("TESTTTTTTTTw22222")

# listnames=df2['alias'].unique().tolist()
# names=['']+listnames
# st.write(names)

# name_choice = st.sidebar.selectbox('Select  name:',names)
# dfbyname=df2[df2['alias']==name_choice]
# st.write(dfbyname)

# projects=dfbyname['project_name'].unique().tolist()


# project_choice = st.sidebar.selectbox('Select  project:', projects)
# dfbyproject=dfbyname[dfbyname['project_name']==project_choice]
# st.write(dfbyproject)








# year_choice = st.sidebar.selectbox('', years)
# model_choice = st.sidebar.selectbox('', models)
# engine_choice = st.sidebar.selectbox('', engines)






# option = st.selectbox(
#     'How would you like to be contacted?',
#     (df2['alias'].unique().tolist()))

# st.write('You selected:', option)

# st.write(df2[df2['alias']==option])