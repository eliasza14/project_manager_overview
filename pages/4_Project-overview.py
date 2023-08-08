import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import calendar 
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

def run_query(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        columnsnames=cur.column_names
        return cur.fetchall(),columnsnames
    
def format_year(year):
    return "{:d}".format(year)  # Removes the comma separator


def update():
    st.session_state.submitted = True

def main():

    conn = init_connection()
    st.set_page_config(page_title="Project Overview")

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    st.title("Project Overview")

    # Define the sidebar form
    with st.sidebar.form("my_sidebar_form"):
        st.write("# Filters User Overview")
        startdate = st.date_input(
        "Give Start Date",
        datetime.date.today())




        enddate = st.date_input(
        "Give End Date",
        datetime.datetime.now() + datetime.timedelta(days=1))
        filter_option = st.radio("Select Filter:", ["Active", "Inactive", "Total"], index=2)  # Set default to "Total"
        st.write(filter_option)
        st.write('Your birthday is:', enddate)

        



        # name = st.text_input("Enter your name:")
        # email = st.text_input("Enter your email:")
        # age = st.number_input("Enter your age:", min_value=0, max_value=120)
        # color = st.selectbox("Choose your favorite color:", ["Red", "Green", "Blue"])
        #submit_button = st.form_submit_button(label="Submit",on_click=update)
        st.form_submit_button(label="Apply Filters",on_click=update)


    # Display the results
    if st.session_state.submitted:
        st.write("Given startdate and endate",startdate)
        st.write("Given startdate and endate",enddate)

        filter_values = {
        "Active": 1,
        "Inactive": 0,
        "Total": "All"
        }

        selected_filter_value = filter_values[filter_option]

        # selected_filter = filter_values[filter_option]
        # st.write(selected_filter)
        # st.write("visble:",value)


        if selected_filter_value == "All":
            filter_condition = "1 OR kimai2_projects.visible=0"  # Show all data regardless of visibility
        else:
            filter_condition = f"kimai2_projects.visible={selected_filter_value}"

        sql = f"""
        SELECT kimai2_projects.name, kimai2_users.alias, SUM(kimai2_timesheet.duration) as duration,
            MIN(kimai2_timesheet.start_time) as startime, MAX(kimai2_timesheet.start_time) as lasttime,
            kimai2_projects.visible, kimai2_user_preferences.name as rate, kimai2_user_preferences.value
        FROM `kimai2_timesheet`
        INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
        INNER JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
        INNER JOIN `kimai2_user_preferences` ON kimai2_users.id=kimai2_user_preferences.user_id
        WHERE DATE(start_time) >= '{startdate}' AND DATE(start_time) <= '{enddate}'
            AND kimai2_user_preferences.name = 'hourly_rate' AND ({filter_condition})
        GROUP BY kimai2_users.alias, kimai2_projects.name, kimai2_projects.visible,
                kimai2_user_preferences.name, kimai2_user_preferences.value;
        """


    #     sql="""SELECT kimai2_projects.name,kimai2_users.alias,SUM(kimai2_timesheet.duration) as duration ,MIN(kimai2_timesheet.start_time) as startime,MAX(kimai2_timesheet.start_time) as lasttime,kimai2_projects.visible,kimai2_user_preferences.name as rate,kimai2_user_preferences.value

    # FROM `kimai2_timesheet`

    # INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user

    # INNER JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id

    # INNER JOIN `kimai2_user_preferences`ON kimai2_users.id=kimai2_user_preferences.user_id

    # WHERE DATE(start_time) >='"""+str(startdate)+"""' AND DATE(start_time) <='"""+str(enddate)+"""' AND kimai2_user_preferences.name = 'hourly_rate' AND kimai2_projects.visible='"""+str(selected_filter)+"""'

    # GROUP BY kimai2_users.alias,kimai2_projects.name,kimai2_projects.visible,kimai2_user_preferences.name,kimai2_user_preferences.value;"""


    #     sql = """SELECT kimai2_projects.name,kimai2_users.alias,SUM(kimai2_timesheet.duration) as duration ,MIN(kimai2_timesheet.start_time) as startime,MAX(kimai2_timesheet.start_time) as lasttime,kimai2_projects.visible
    # FROM `kimai2_timesheet`
    # INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
    # INNER JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
    # WHERE DATE(start_time) >='"""+str(startdate)+"""' AND DATE(start_time) <='"""+str(enddate)+"""' 
    # GROUP BY kimai2_users.alias,kimai2_projects.name,kimai2_projects.visible;"""
        






        sql2 ="""SELECT kimai2_users.alias,SUM(kimai2_timesheet.duration) as duration 
    FROM `kimai2_timesheet`
    INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
    WHERE DATE(start_time) >='"""+str(startdate)+"""' AND DATE(start_time) <='"""+str(enddate)+"""' 

    GROUP BY kimai2_users.alias; """

        

        rows,columnames = run_query(conn,sql)

    # st.write(columnames)
        dfdata=pd.DataFrame(rows,columns=columnames)
        st.write("All Data from Query",dfdata)
        dfdata=dfdata[dfdata['alias']!='ADMINISTRATOR']
        st.write("All Data from Filter",dfdata)

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
        ##############containers
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.title("hello")
                st.write(f"""
                    <body>
                        <div style="display:flex; justify-content: center; " >
                            <div style="width:310px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                                <div style="text-align:right;">
                                <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g id="&#206;&#147;&#206;&#181;&#206;&#189;&#206;&#185;&#206;&#186;&#207;&#140;&#207;&#130; &#207;&#128;&#206;&#187;&#206;&#183;&#206;&#184;&#207;&#133;&#207;&#131;&#206;&#188;&#207;&#140;&#207;&#130;">
                                    <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                                    <g id="Group">
                                    <path id="Vector" fill-rule="evenodd" clip-rule="evenodd" d="M19.9398 24.2348C20.8399 24.2348 21.7032 23.8772 22.3397 23.2407C22.9762 22.6042 23.3337 21.741 23.3337 20.8408C23.3337 19.9407 22.9762 19.0775 22.3397 18.441C21.7032 17.8045 20.8399 17.4469 19.9398 17.4469C19.0397 17.4469 18.1764 17.8045 17.5399 18.441C16.9034 19.0775 16.5458 19.9407 16.5458 20.8408C16.5458 21.741 16.9034 22.6042 17.5399 23.2407C18.1764 23.8772 19.0397 24.2348 19.9398 24.2348ZM19.9398 25.9318C20.6083 25.9318 21.2703 25.8001 21.888 25.5442C22.5057 25.2884 23.0669 24.9134 23.5396 24.4407C24.0123 23.9679 24.3873 23.4067 24.6432 22.7891C24.899 22.1714 25.0307 21.5094 25.0307 20.8408C25.0307 20.1723 24.899 19.5103 24.6432 18.8926C24.3873 18.275 24.0123 17.7138 23.5396 17.241C23.0669 16.7683 22.5057 16.3933 21.888 16.1375C21.2703 15.8816 20.6083 15.7499 19.9398 15.7499C18.5896 15.7499 17.2947 16.2863 16.34 17.241C15.3852 18.1958 14.8489 19.4907 14.8489 20.8408C14.8489 22.191 15.3852 23.4859 16.34 24.4407C17.2947 25.3954 18.5896 25.9318 19.9398 25.9318Z" fill="url(#paint0_linear_31_789)"/>
                                    <path id="Vector_2" fill-rule="evenodd" clip-rule="evenodd" d="M17.9949 24.0583C18.0739 24.1371 18.1366 24.2307 18.1794 24.3338C18.2222 24.4369 18.2442 24.5474 18.2442 24.659C18.2442 24.7706 18.2222 24.8811 18.1794 24.9842C18.1366 25.0873 18.0739 25.1809 17.9949 25.2597L17.4213 25.8316C16.3175 26.9358 15.6974 28.433 15.6972 29.9943V33.1439C15.6972 33.3689 15.6078 33.5847 15.4487 33.7438C15.2896 33.903 15.0738 33.9924 14.8487 33.9924C14.6237 33.9924 14.4079 33.903 14.2488 33.7438C14.0896 33.5847 14.0002 33.3689 14.0002 33.1439V29.9943C14.0005 27.983 14.7995 26.0542 16.2216 24.6319L16.7935 24.0583C16.8723 23.9793 16.9659 23.9166 17.069 23.8738C17.1721 23.831 17.2826 23.809 17.3942 23.809C17.5058 23.809 17.6163 23.831 17.7194 23.8738C17.8225 23.9166 17.9161 23.9793 17.9949 24.0583ZM38.0056 23.5492C37.9266 23.628 37.8639 23.7216 37.8211 23.8247C37.7783 23.9278 37.7563 24.0383 37.7563 24.1499C37.7563 24.2615 37.7783 24.372 37.8211 24.4751C37.8639 24.5782 37.9266 24.6718 38.0056 24.7507L38.5792 25.3225C39.1258 25.8692 39.5594 26.5182 39.8552 27.2324C40.151 27.9466 40.3033 28.7121 40.3033 29.4852V33.1439C40.3033 33.3689 40.3927 33.5847 40.5518 33.7438C40.7109 33.903 40.9267 33.9924 41.1518 33.9924C41.3768 33.9924 41.5926 33.903 41.7517 33.7438C41.9109 33.5847 42.0002 33.3689 42.0002 33.1439V29.4852C42 27.4739 41.201 25.5451 39.7789 24.1228L39.207 23.5492C39.1282 23.4702 39.0346 23.4075 38.9315 23.3647C38.8284 23.3219 38.7179 23.2999 38.6063 23.2999C38.4947 23.2999 38.3842 23.3219 38.2811 23.3647C38.178 23.4075 38.0844 23.4702 38.0056 23.5492Z" fill="url(#paint1_linear_31_789)"/>
                                    <path id="Vector_3" fill-rule="evenodd" clip-rule="evenodd" d="M35.2122 24.2348C34.3121 24.2348 33.4488 23.8772 32.8124 23.2407C32.1759 22.6042 31.8183 21.741 31.8183 20.8408C31.8183 19.9407 32.1759 19.0775 32.8124 18.441C33.4488 17.8045 34.3121 17.4469 35.2122 17.4469C36.1124 17.4469 36.9756 17.8045 37.6121 18.441C38.2486 19.0775 38.6062 19.9407 38.6062 20.8408C38.6062 21.741 38.2486 22.6042 37.6121 23.2407C36.9756 23.8772 36.1124 24.2348 35.2122 24.2348ZM35.2122 25.9318C34.5437 25.9318 33.8817 25.8001 33.264 25.5442C32.6464 25.2884 32.0852 24.9134 31.6124 24.4407C31.1397 23.9679 30.7647 23.4067 30.5088 22.7891C30.253 22.1714 30.1213 21.5094 30.1213 20.8408C30.1213 20.1723 30.253 19.5103 30.5088 18.8926C30.7647 18.275 31.1397 17.7138 31.6124 17.241C32.0852 16.7683 32.6464 16.3933 33.264 16.1375C33.8817 15.8816 34.5437 15.7499 35.2122 15.7499C36.5624 15.7499 37.8573 16.2863 38.8121 17.241C39.7668 18.1958 40.3031 19.4907 40.3031 20.8408C40.3031 22.191 39.7668 23.4859 38.8121 24.4407C37.8573 25.3954 36.5624 25.9318 35.2122 25.9318ZM27.5759 31.4469C26.4507 31.4469 25.3716 31.8939 24.576 32.6895C23.7804 33.4851 23.3334 34.5642 23.3334 35.6893V37.8954C23.3334 38.1204 23.2441 38.3362 23.0849 38.4954C22.9258 38.6545 22.71 38.7439 22.485 38.7439C22.2599 38.7439 22.0441 38.6545 21.885 38.4954C21.7259 38.3362 21.6365 38.1204 21.6365 37.8954V35.6893C21.6365 34.1141 22.2622 32.6034 23.3761 31.4895C24.4899 30.3757 26.0006 29.7499 27.5759 29.7499C29.1511 29.7499 30.6618 30.3757 31.7757 31.4895C32.8895 32.6034 33.5153 34.1141 33.5153 35.6893V37.8954C33.5153 38.1204 33.4259 38.3362 33.2667 38.4954C33.1076 38.6545 32.8918 38.7439 32.6668 38.7439C32.4417 38.7439 32.2259 38.6545 32.0668 38.4954C31.9077 38.3362 31.8183 38.1204 31.8183 37.8954V35.6893C31.8183 35.1322 31.7086 34.5805 31.4954 34.0658C31.2822 33.5511 30.9697 33.0834 30.5757 32.6895C30.1818 32.2955 29.7141 31.983 29.1994 31.7698C28.6847 31.5566 28.133 31.4469 27.5759 31.4469Z" fill="url(#paint2_linear_31_789)"/>
                                    <path id="Vector_4" fill-rule="evenodd" clip-rule="evenodd" d="M27.5758 28.9014C28.4759 28.9014 29.3392 28.5438 29.9756 27.9074C30.6121 27.2709 30.9697 26.4076 30.9697 25.5075C30.9697 24.6073 30.6121 23.7441 29.9756 23.1076C29.3392 22.4711 28.4759 22.1135 27.5758 22.1135C26.6756 22.1135 25.8124 22.4711 25.1759 23.1076C24.5394 23.7441 24.1818 24.6073 24.1818 25.5075C24.1818 26.4076 24.5394 27.2709 25.1759 27.9074C25.8124 28.5438 26.6756 28.9014 27.5758 28.9014ZM27.5758 30.5984C28.926 30.5984 30.2209 30.062 31.1756 29.1073C32.1303 28.1526 32.6667 26.8577 32.6667 25.5075C32.6667 24.1573 32.1303 22.8624 31.1756 21.9077C30.2209 20.9529 28.926 20.4166 27.5758 20.4166C26.2256 20.4166 24.9307 20.9529 23.976 21.9077C23.0212 22.8624 22.4849 24.1573 22.4849 25.5075C22.4849 26.8577 23.0212 28.1526 23.976 29.1073C24.9307 30.062 26.2256 30.5984 27.5758 30.5984Z" fill="url(#paint3_linear_31_789)"/>
                                    </g>
                                    </g>
                                    <defs>
                                    <linearGradient id="paint0_linear_31_789" x1="16.1032" y1="16.407" x2="27.9294" y2="29.368" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                    <linearGradient id="paint1_linear_31_789" x1="17.4496" y1="23.9899" x2="25.1997" y2="46.2324" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                    <linearGradient id="paint2_linear_31_789" x1="23.936" y1="17.2337" x2="50.5736" y2="40.9334" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                    <linearGradient id="paint3_linear_31_789" x1="23.7392" y1="21.0736" x2="35.5654" y2="34.0346" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                    </defs>
                                </svg>
                                </div>
                                <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                                <div>
                                    <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Σύνολο Εργαζομένων</div>
                                    <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Γεν. Πληθυσμού</div>
                                </div>
                            </div>
                        </div>
                    </body>""")
            with col2:
                st.title("there")
                
        


    #         # Create the pie chart using Plotly Express
    #     fig = px.pie(dfgroup2, values=countlist, names='alias', hover_data=[dfgroup2['name']],labels={'alias':'User',
    #                                                                                                         'values':'Project count',
    #                                                                                                         'name':'Projects'})
    #     fig.update_traces(textposition='inside', textinfo='label+value')

    #     # Display the pie chart


    #     st.title("User Overview")
    #     st.plotly_chart(fig)

    #     rows,columnames = run_query(conn,sql2)

    #     # st.write(columnames)
    #     dfdata2=pd.DataFrame(rows,columns=columnames)
    #     dfdata2=dfdata2[dfdata2['alias']!='ADMINISTRATOR']
    #     st.write("All Data from Filter data2",dfdata2)
    #     dfdata2.loc[:, 'duration'] = dfdata2['duration'] // 3600
        
    #     dfdata2=dfdata2.sort_values('duration', ascending=False)
        
    #     st.write("All Data from Query",dfdata2)


    #     fig2 = go.Figure(go.Bar(
    #     x=dfdata2['duration'].tolist(),
    #     y=dfdata2['alias'].tolist(),
    #     orientation='h'))

    #     fig2.update_layout(title="Users Total Working Hours",yaxis=dict(autorange="reversed"))
    #     st.plotly_chart(fig2)

    #     st.title("Select User from the below list:")
    #         # List of options for the dropdown menu
    #     optionlist =dfdata2['alias'].tolist()
    #     options = optionlist

    #     # Display the dropdown menu
    #     selected_option = st.selectbox('Choose User', options)
    #     df1 = dfdata2[dfdata2['alias'] == selected_option]
    #     # df1['duration']=df1['duration']/3600
    #     # df1.loc[:, 'duration'] = df1['duration'] / 3600
    #     first_duration_value = df1['duration'].iloc[0]
    #     first_alias_value = df1['alias'].iloc[0]
    #     text="**Total** **duration** **is:** **"+str(first_duration_value)+"** **Hours** **\u23F0** "
    #     #st.write(first_alias_value)
    #     #st.markdown(text)
    #     st.title(text)
    #     userdf = dfdata.loc[dfdata['alias']==first_alias_value]
    #     userdf['cost']=userdf['value'].astype(float)*userdf['duration'].astype(float)
    #     st.write(userdf)

    #     fig3 = px.pie(userdf, values='duration', names='name',
    #             title='User Project durations',
    #             hover_data=['duration'], labels={'duration':'duration'})
    #     fig3.update_traces(textposition='inside', textinfo='percent+label')
    #     st.plotly_chart(fig3)


    #     st.write('Rate per Project for selected user')

    #     figrate= px.bar(userdf, y='cost', x='name', text_auto='.2s',title="Project Manager: "+str(selected_option)+" - Hourly projects duaration")
    #     figrate.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    #     st.plotly_chart(figrate)




    #     st.title("Select Project from the below list")
        
    #     optionlist =userdf['name'].tolist()
    #     options2 = optionlist
    #     selected_option = st.selectbox('Choose Project', options2)
    #     df2 = userdf[userdf['name'] == selected_option]
    #     #st.write(df2)
    #     first_name_value2 = df2['name'].iloc[0]
    #     first_alias_value2 = df2['alias'].iloc[0]

    # #     sql3=""" SELECT kimai2_users.alias,kimai2_projects.name,kimai2_timesheet.start_time,kimai2_timesheet.duration
    # # FROM `kimai2_timesheet`
    # # INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
    # # Inner JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
    # # WHERE kimai2_users.alias="""+str(first_alias_value2)+""" and kimai2_projects.name="""+str(first_name_value2)+""";"""
        
    #     sql3=""" SELECT kimai2_users.alias,kimai2_projects.name,kimai2_timesheet.start_time,kimai2_timesheet.duration
    # FROM `kimai2_timesheet`
    # INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
    # Inner JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
    # WHERE kimai2_users.alias='"""+str(first_alias_value2)+"""' AND kimai2_projects.name='"""+str(first_name_value2)+"""';"""

    #     rows,columnames = run_query(conn,sql3)

    #     # st.write(columnames)
    #     dfdata3=pd.DataFrame(rows,columns=columnames)
    #     st.write("All Data from Query",dfdata3)
        
    #     # Convert 'start_time' column to datetime
    #     dfdata3['start_time'] = pd.to_datetime(dfdata3['start_time'])
    #     dfdata3['year'] = dfdata3['start_time'].dt.year
    
    # # Apply the formatting function to the 'Year' column
    #     dfdata3['year'] = dfdata3['year'].apply(format_year)
    #     # dfdata3['year']=dfdata3['year'].str.replace(',', '').astype(int)
    #     st.write(dfdata3['year'].dtype)

    #     # Extract month from 'start_time' column
    #     dfdata3['month'] = dfdata3['start_time'].dt.month

    #     # Convert 'duration' column to numeric
    #     dfdata3['duration'] = (dfdata3['duration'] / 3600).astype(int)
    #     st.write("After Preprocessing Data from Query",dfdata3)



    #     # Group by month and calculate total duration
    #     dfdata3group = dfdata3.groupby('month')['duration'].sum().reset_index()

    #     # Create all 12 months
    #     all_months = list(range(1, 13))

    #     # Add missing months to the DataFrame with duration set to 0
    #     dfdata3group = dfdata3group.merge(pd.DataFrame({'month': all_months}), how='right')

    #     # Sort the DataFrame by month
    #     dfdata3group = dfdata3group.sort_values('month')

    #     # Fill missing duration values with 0
    #     dfdata3group['duration'] = dfdata3group['duration'].fillna(0)

    #     # Get the name of each month
    #     dfdata3group['month_name'] = dfdata3group['month'].apply(lambda x: calendar.month_name[x])

    #     # Create line chart
    #     fig = go.Figure()

    #     # Add line trace
    #     fig.add_trace(go.Scatter(
    #         x=dfdata3group['month_name'],
    #         y=dfdata3group['duration'],
    #         mode='lines',
    #         name='Duration'
    #     ))

    #     # Identify the months with non-zero sum duration
    #     non_zero_months = dfdata3group[dfdata3group['duration'] > 0]

    #     # Add dots for non-zero months
    #     fig.add_trace(go.Scatter(
    #         x=non_zero_months['month_name'],
    #         y=non_zero_months['duration'],
    #         mode='markers',
    #         marker=dict(
    #             color='green',
    #             size=10,
    #             symbol='circle',
    #             line=dict(
    #                 width=2,
    #                 color='green'
    #             )
    #         ),
    #         name='Non-Zero Months'
    #     ))

    #     # Set axis labels and chart title
    #     fig.update_layout(
    #         xaxis_title='Months',
    #         yaxis_title='Total Duration of Project:'+first_name_value2+" in Hours",
    #         title='Duration of the Project per Month'
    #     )

    #     # Display the chart
    #     st.plotly_chart(fig)






if __name__ == '__main__':
    main()


