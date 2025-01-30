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
        SELECT kimai2_projects.name, kimai2_users.alias,kimai2_users.enabled, SUM(kimai2_timesheet.duration) as duration,
            MIN(kimai2_timesheet.start_time) as startime, MAX(kimai2_timesheet.start_time) as lasttime,
            kimai2_projects.visible, kimai2_user_preferences.name as rate, kimai2_user_preferences.value
        FROM `kimai2_timesheet`
        INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
        INNER JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
        INNER JOIN `kimai2_user_preferences` ON kimai2_users.id=kimai2_user_preferences.user_id
        WHERE DATE(start_time) >= '{startdate}' AND DATE(start_time) <= '{enddate}'
            AND kimai2_user_preferences.name = 'hourly_rate' AND ({filter_condition})
        GROUP BY kimai2_users.alias, kimai2_projects.name, kimai2_projects.visible,
                kimai2_user_preferences.name, kimai2_user_preferences.value,kimai2_users.enabled;
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
        with open("animated_counter.js", "r") as file:
            js_code = file.read()

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                val=len(dfdata['name'].unique())
                html_content1 = html_button1(js_code,val)
                html(html_content1,height=250)
            with col2:
                val=len(dfdata['alias'][dfdata['enabled']==1].unique())
                html_content2 = html_button2(js_code,val)
                html(html_content2,height=250)

        with st.container():
            col1,col2 = st.columns(2)
            with col1:

                dfgroup=dfdata.groupby('name')['duration'].sum()
                dfgroup=dfgroup.to_frame().reset_index()
                # st.write(dfgroup['duration'])
                # st.write(dfdata.groupby('name')['duration'].sum())

                fig = px.pie(dfgroup, values='duration', names='name',
                title='% Διάρκεια ανα Project επί του Συνόλου  ',
                hover_data=['duration'], labels={'duration':'duration'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                
            with col2:
                pass

                # Display the dropdown menu
               # List of options for the dropdown menu
        st.plotly_chart(fig)
        optionlist =dfdata['name'].unique().tolist()
        options = optionlist
        selected_option2 = st.selectbox('Select Project', options)
        df1 = dfdata[dfdata['name'] == selected_option2]
        st.write(df1)

        with st.container():
            col1, col2,col3,col4 = st.columns(4)
            with col1:
                pass
  
            with col2:
                # st.write(df1)
                val=len(df1['alias'][dfdata['enabled']==1].unique())
                
                # st.write(val2)
                html_content3 = html_button3(js_code,val)
                
                html(html_content3, height=250)
                
            with col3:
                df1['value'] = pd.to_numeric(df1['value'], errors='coerce')
                df1['duration'] = pd.to_numeric(df1['duration'], errors='coerce')
                val2 = (df1['value'] * df1['duration']).sum()
                html_content4 = html_cost5(js_code, val2)
                html(html_content4, height=250, width=300)
               
                # val=len(dfdata['name'].unique())
                # html_content1 = html_button1(js_code,val)
                # html(html_content1,height=250)
            with col4:
                pass
        
        with st.container():
            col1,col2 = st.columns(2)
            with col1:
                st.write('Rate per Project for selected user')
                # df1['cost']=df1['value'].astype(float)*df1['duration'].astype(float)
                figrate= px.bar(df1, y='duration', x='alias', text_auto='.2s',title="Project Manager: "+str(selected_option2)+" - Hourly projects duration")
                figrate.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
                df1['Total_cost'] = df1['duration'] * df1['value']
                figrate2 = px.bar(df1, y='Total_cost', x='alias', text_auto='.2s',title="Project Manager: "+str(selected_option2)+" - Cost projects per hour")
                figrate2.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
                
                



            with col2:
                pass
        st.plotly_chart(figrate)
        st.plotly_chart(figrate2)
            

        sql = f""" SELECT kimai2_users.alias,kimai2_projects.name,kimai2_timesheet.start_time,kimai2_timesheet.duration
    FROM `kimai2_timesheet`
    INNER JOIN `kimai2_users` ON kimai2_users.id=kimai2_timesheet.user
    Inner JOIN `kimai2_projects` ON kimai2_projects.id=kimai2_timesheet.project_id
    WHERE kimai2_projects.name='"""+str(selected_option2)+"""';"""
            
        rows,columnames = run_query(conn,sql)

    # st.write(columnames)
        dfdata3=pd.DataFrame(rows,columns=columnames)
        st.write("All Data from Query",dfdata3)
        
        # Convert 'start_time' column to datetime
        dfdata3['start_time'] = pd.to_datetime(dfdata3['start_time'])
        dfdata3['year'] = dfdata3['start_time'].dt.year
    
    # Apply the formatting function to the 'Year' column
        dfdata3['year'] = dfdata3['year'].apply(format_year)

        options = dfdata3['year'].unique().tolist()

        # Display the dropdown menu
        selected_option = st.selectbox('Επιλέξτε έτος', options)
        # dfdata3['year']=dfdata3['year'].str.replace(',', '').astype(int)
        st.write(dfdata3['year'].dtype)

        # Extract month from 'start_time' column
        dfdata3['month'] = dfdata3['start_time'].dt.month

        # Convert 'duration' column to numeric
        dfdata3['duration'] = (dfdata3['duration'] / 3600).astype(int)
        dfdata3_filtered = dfdata3[dfdata3['year']==selected_option]
        st.write("After Preprocessing Data from Query",dfdata3_filtered)



        # Group by month and calculate total duration
        dfdata3group = dfdata3_filtered.groupby('month')['duration'].sum().reset_index()

        # Create all 12 months
        all_months = list(range(1, 13))

        # Add missing months to the DataFrame with duration set to 0
        dfdata3group = dfdata3group.merge(pd.DataFrame({'month': all_months}), how='right')

        # Sort the DataFrame by month
        dfdata3group = dfdata3group.sort_values('month')

        # Fill missing duration values with 0
        dfdata3group['duration'] = dfdata3group['duration'].fillna(0)

        # Get the name of each month
        dfdata3group['month_name'] = dfdata3group['month'].apply(lambda x: calendar.month_name[x])

        # # Create line chart
        # fig = go.Figure()

        # # Add line trace
        # fig.add_trace(go.Scatter(
        #     x=dfdata3group['month_name'],
        #     y=dfdata3group['duration'],
        #     mode='lines',
        #     name='Duration'
        # ))

        # # Identify the months with non-zero sum duration
        # non_zero_months = dfdata3group[dfdata3group['duration'] > 0]

        # # Add dots for non-zero months
        # fig.add_trace(go.Scatter(
        #     x=non_zero_months['month_name'],
        #     y=non_zero_months['duration'],
        #     mode='markers',
        #     marker=dict(
        #         color='green',
        #         size=10,
        #         symbol='circle',
        #         line=dict(
        #             width=2,
        #             color='green'
        #         )
        #     ),
        #     name='Non-Zero Months'
        # ))

        # # Set axis labels and chart title
        # fig.update_layout(
        #     xaxis_title='Months',
        #     yaxis_title='Total Duration of Project:'+" in Hours",
        #     title='Duration of the Project per Month'
        # )

        # # Display the chart
        # st.plotly_chart(fig)

        # Group by alias and month and sum duration
        dfdata3group = dfdata3_filtered.groupby(['alias', 'month'])['duration'].sum().reset_index()

# Create all 12 months DataFrame
        all_months = pd.DataFrame({'month': list(range(1, 13))})

# Ensure every alias has all months
        unique_aliases = dfdata3group['alias'].unique()
        expanded_df = pd.concat([
            all_months.assign(alias=alias) for alias in unique_aliases
        ], ignore_index=True)

# Merge to ensure all months exist for each alias, filling missing durations with 0
        dfdata3group = expanded_df.merge(dfdata3group, on=['alias', 'month'], how='left').fillna({'duration': 0})

# Get the name of each month
        dfdata3group['month_name'] = dfdata3group['month'].apply(lambda x: calendar.month_name[x])

# Create line chart
        fig = go.Figure()

# Add a line for each unique alias
        for alias in dfdata3group['alias'].unique():
            alias_data = dfdata3group[dfdata3group['alias'] == alias]
            fig.add_trace(go.Scatter(
                x=alias_data['month_name'],
                y=alias_data['duration'],
                mode='lines+markers',
                name=str(alias)
            ))

# Set axis labels and chart title
        fig.update_layout(
            xaxis_title='Months',
            yaxis_title='Total Duration in Hours',
            title='Duration of the Project ' + selected_option2 +  ' per Month of Year ' + selected_option,
            legend_title="Users"
        )

# Display the chart
        st.plotly_chart(fig)


        ##### Nice Try #############

#         for alias, df in dfdata3.items():
#     # Add line trace for each project
#             fig.add_trace(go.Scatter(
#             x=df['month_name'],
#             y=df['duration'],
#             mode='lines',
#             name=f'Duration ({alias})'
#         ))

#     # Identify the months with non-zero sum duration
#         non_zero_months = df[df['duration'] > 0]

#     # Add dots for non-zero months
#         fig.add_trace(go.Scatter(
#             x=non_zero_months['month_name'],
#             y=non_zero_months['duration'],
#             mode='markers',
#             marker=dict(
#                 size=10,
#                 symbol='circle',
#                 line=dict(width=2),
#             ),
#             name=f'Non-Zero Months ({alias})'
#         ))

# # Set axis labels and chart title
#         fig.update_layout(
#             xaxis_title='Months',
#             yaxis_title='Total Duration of Project (in Hours)',
#             title='Duration of the Project per Month',
#             legend_title="Project Alias"
#         )

# # Display the chart in Streamlit
#         st.plotly_chart(fig)




        




                
        


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


