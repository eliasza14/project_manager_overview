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
        sql = """SELECT `kimai2_teams`.name as team_name,`kimai2_users_teams`.`user_id`,`kimai2_users_teams`.`team_id`,`kimai2_users_teams`.`teamlead`,

`kimai2_projects_teams`.`project_id`

,`kimai2_users`.`alias` as username,`kimai2_projects`.`name` as project_name,
`kimai2_projects`.`visible` as active,`kimai2_projects`.`time_budget`,`kimai2_projects`.`start` as start_date, `kimai2_projects`.`end` as end_date,
 (
    SELECT SUM(kimai2_timesheet.duration)
    FROM kimai2_timesheet
    WHERE kimai2_timesheet.project_id = kimai2_projects.id
  ) AS duration
FROM `kimai2_teams`
INNER JOIN kimai2_users_teams ON kimai2_teams.id=kimai2_users_teams.team_id
INNER JOIN kimai2_projects_teams ON kimai2_projects_teams.team_id=kimai2_teams.id
INNER JOIN kimai2_users ON kimai2_users_teams.user_id=kimai2_users.id
INNER JOIN kimai2_projects ON kimai2_projects_teams.project_id=kimai2_projects.id
WHERE kimai2_users_teams.teamlead=1;
        """

        
    
        rows,columnames = run_query(conn,sql)

    # st.write(columnames)
        dfdata=pd.DataFrame(rows,columns=columnames)
        st.write("All Data from Query",dfdata)
   
        # Load the tips dataset from Plotly



        # Create a Streamlit app
        dfgroup=dfdata.groupby(['username'])['project_name'].count()


        dfgroup2=dfdata.groupby('username')['project_name'].agg(list).reset_index()


        dfframe=dfgroup.to_frame().reset_index()

        userlist=dfframe['username'].tolist()

        countlist=dfframe['project_name'].tolist()

        # dfgroup2

        for i in range(len(dfgroup2)):
            dfgroup2['project_name'][i] = '<br>'.join(dfgroup2['project_name'][i]).replace(',', ',<br>')


        # Create the pie chart using Plotly Express
        fig = px.pie(dfgroup2, values=countlist, names='username', hover_data=[dfgroup2['project_name']],labels={'username':'Project Manager',
                                                                                                         'values':'Project number',
                                                                                                            'project_name':'Projects'})
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Display the pie chart


        st.title("Project Manager Overview")
        st.plotly_chart(fig)

        st.title("Select Project Manager from the below list:")
        # List of options for the dropdown menu
        optionlist =dfdata['username'].unique().tolist()
        options = optionlist

        # Display the dropdown menu
        selected_option = st.selectbox('Choose Project Manager', options)
        df1 = dfdata[dfdata['username'] == selected_option]
        # df1['duration']=df1['duration']/3600
        df1.loc[:, 'duration'] = df1['duration'] / 3600

        # df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
        fig2 = px.bar(df1, y='duration', x='project_name', text_auto='.2s',
                    title="Project Manager: "+str(selected_option)+" - Hourly projects duaration")
        st.plotly_chart(fig2)

        
        # def get_tab_content():
        #     return [
        #         {"title":"Topic A", "content":"Topic A Content"},
        #         {"title":"Topic B", "content":"Topic B Content"},
        #         {"title":"Topic C", "content":"Topic C Content"},
        #     ]
        # # pull tab content from server
        # tab_contents = get_tab_content()
        # #tab_contents = df1
        # # create tabs
        # names = [content["title"] for content in tab_contents]
        # tabs = st.tabs(names)

        # # iterate through each tab and build content
        # for tab, tab_content in zip(tabs,tab_contents):
        #     with tab:
        #         st.header(tab_content["title"])
        #         st.write(tab_content["content"])
        # st.write(df1)
              
        tabs = st.tabs(df1['project_name'].tolist())
        tablist=df1['project_name'].tolist()
        

        # st.write(tablist[0])
        

        for i in range(len(tabs)):
            with tabs[i]:
                st.title("Analysis of "+str(tablist[i])+" Project")
                dftest=df1[df1['project_name']==str(tablist[i])]
                projectlist=dftest['project_id'].tolist()
                teamlist=dftest['team_id'].tolist()
                sql2=""" 
                        SELECT kimai2_projects_teams.*,kimai2_projects.name,kimai2_projects.visible,kimai2_projects.time_budget,kimai2_projects.budget,kimai2_users_teams.user_id,kimai2_users_teams.teamlead,
                (
                    SELECT SUM(kimai2_timesheet.duration)
                    FROM kimai2_timesheet
                    WHERE kimai2_timesheet.user = kimai2_users_teams.user_id and kimai2_timesheet.project_id=kimai2_projects_teams.project_id
                ) AS duration,kimai2_users.alias as username,kimai2_teams.name as team_name

                FROM `kimai2_projects_teams` 
                INNER JOIN kimai2_projects ON kimai2_projects.id=kimai2_projects_teams.project_id 
                INNER JOIN kimai2_users_teams ON kimai2_users_teams.team_id=kimai2_projects_teams.team_id 
                INNER JOIN kimai2_timesheet ON kimai2_timesheet.user=kimai2_users_teams.user_id and kimai2_timesheet.project_id=kimai2_projects_teams.project_id 
                INNER JOIN kimai2_users ON kimai2_users.id=kimai2_users_teams.user_id
                INNER JOIN kimai2_teams ON kimai2_teams.id=kimai2_projects_teams.team_id
                where kimai2_projects_teams.project_id="""+str(projectlist[0])+""" and kimai2_projects_teams.team_id="""+str(teamlist[0])+"""
                GROUP BY kimai2_users_teams.user_id;
                
                
                """

              
                rows2,columnames2 = run_query(conn,sql2)

                # st.write(columnames)
                dfdata2=pd.DataFrame(rows2,columns=columnames2)
                # dfdata2['duration']=dfdata2['duration']/3600
                dfdata2.loc[:, 'duration'] = dfdata2['duration'] / 3600

                # st.write(projectlist[0])
                # st.write(teamlist[0])
                # st.write("All Data from Query",dfdata2)

 # Create the visualization based on the selected option


                # visualization_option = st.radio("Select Visualization", ("Pie Chart", "Bar Plot"), key=str(i))
                # if visualization_option == "Pie Chart":
                #     figtab = px.pie(dfdata2, values='duration', names='username', hover_data=[dfdata2['username']])
                #     figtab.update_traces(textposition='inside', textinfo='percent+label')
                #     st.plotly_chart(figtab)
                # elif visualization_option == "Bar Plot":
                #     figtab = go.Figure(data=[go.Bar(x=dfdata2['username'], y=dfdata2['duration'])])
                #     st.plotly_chart(figtab)



                # Create the pie chart using Plotly Express
                figtab = px.pie(dfdata2, values='duration', names='username', hover_data=[dfdata2['username']])
                figtab.update_traces(textposition='inside', textinfo='percent+label')

                # Display the pie chart


                st.plotly_chart(figtab)


            

        # tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

        # with tab1:
        #     st.header("A cat")
        #     st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

        # with tab2:
        #     st.header("A dog")
        #     st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

        # with tab3:
        #     st.header("An owl")
        #     st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



        st.title("Compare Project Managers")

        regular_search_term =dfdata['username'].unique().tolist()
        choices2 = st.multiselect(" ",regular_search_term + ['All'])



        if 'All' not in choices2:

            df2=dfdata[dfdata['username'].isin(choices2)]
            df2['duration']=df2['duration']/3600
            # st.write(df2)
            
            #fig2 = px.bar(df2, x="username", y=df2['project_name'].tolist(), title="Wide-Form Input")
            fig2 = px.bar(df2, x="username", y="duration", color=df2['project_name'].tolist(), title="Project Manager Comparison between:"+str(choices2))
            st.plotly_chart(fig2)
        else:
            # st.write(dfdata)
            df3=dfdata.copy()
            df3['duration']=df3['duration']/3600
            # st.write(df3)
            
            #fig2 = px.bar(df2, x="username", y=df2['project_name'].tolist(), title="Wide-Form Input")
            fig2 = px.bar(df3, x="username", y="duration", color=df3['project_name'].tolist(), title="Project Manager Comparison between all")
            st.plotly_chart(fig2)





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