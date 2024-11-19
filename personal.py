import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu



dfp = pd.read_csv("./Player.csv")
dfa = pd.read_csv("./Player_Attributes.csv")



# Replace 0 with 'low', 1 with 'low', 2 with 'low'
dfa['defensive_work_rate'] = dfa['defensive_work_rate'].replace([0, 1, 2], 'low')

# Replace 3 with 'medium', 4 with 'medium', 5 with 'medium', 6 with 'medium', 7 with 'medium'
dfa['defensive_work_rate'] = dfa['defensive_work_rate'].replace([3, 4, 5, 6, 7], 'medium')

# Replace everything else with 'high'
dfa['defensive_work_rate'] = dfa['defensive_work_rate'].replace(dfa['attacking_work_rate'].unique(), 'high')

df = pd.merge(dfa, dfp, on='player_api_id', how='left')
df.to_csv('merged.csv', index=False)

# Remove duplicates based on 'player_name'
df.drop_duplicates(subset='player_name', keep='first', inplace=True)



# Sort the dataframe by 'overall_rating' in descending order
df_sorted = df.sort_values('overall_rating', ascending=False)

menu_selected = option_menu(None, ["Home", "KPIs", "Insights", "Data Analysis"], 
    icons=['house', 'star', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
        "container": {"background-color": "#16537e"},
        "icon": {"color": "#black", "font-size": "16px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#1c1c84"},
        "nav-link-selected": {"background-color": "#1c1c84"},
    }
)

if menu_selected == "Home":
    st.title("Football Stats Analysis")
    st.write("Welcome to the Home Page, in here you can find the data of the players")
    st.write(df)

    st.write("Summary Statistics:")
    st.write(df.describe())

elif menu_selected == "KPIs":
    st.header("Key Performance Indicators")
    st.write("Welcome to the KPIs Page")
    st.markdown("Here are some key performance indicators (KPIs):")
    st.markdown("- Average overall rating: **7.5**")
    st.markdown("- Maximum potential: **95**")
    st.markdown("- Minimum potential: **40**")

        # Add a header
    st.header("Top 10 Highest Players")

    # Select the top 10 players with the highest overall rating
    top_10_players = df.nlargest(10, 'overall_rating')

    # Create a bar chart showing the top 10 highest overall players
    fig = px.bar(top_10_players, x='player_name', y='overall_rating', title='Top 10 Highest Overall Players', labels={'player_name':'Player Name', 'overall_rating':'Overall Rating'}, color='overall_rating')
    st.plotly_chart(fig)

elif menu_selected == "Insights":
    st.header("Insights")
    st.write("Welcome to the Insights Page")
    
    def scatter():
        fil = px.scatter(df, x='potential', y='overall_rating', color='preferred_foot', title='Potential vs Overall Rating', labels={'potential':'Potential', 'overall_rating':'Overall Rating'})
        st.write(fil)

    def parallel_categories():
        fig = px.parallel_categories(df, dimensions=['preferred_foot', 'attacking_work_rate', 'defensive_work_rate'], color='overall_rating', title='Parallel Categories', labels={'preferred_foot':'Preferred Foot', 'attacking_work_rate':'Attacking Work Rate', 'defensive_work_rate':'Defensive Work Rate', 'overall_rating':'Overall Rating'}, color_continuous_scale=px.colors.sequential.Inferno)
        st.write(fig)

    def histogram():
        fig = px.histogram(df, x='overall_rating', title='Overall Rating Histogram', labels={'overall_rating':'Overall Rating'})
        st.write(fig)

    def box():
        fig = px.box(df, x='preferred_foot', y='overall_rating', title='Preferred Foot vs Overall Rating', labels={'preferred_foot':'Preferred Foot', 'overall_rating':'Overall Rating'})
        st.write(fig)


    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        scatter()
    with c2:
        parallel_categories()
    with c3:
        histogram()
    with c4:
        box()

elif menu_selected == "Data Analysis":
    st.header("Data Analysis")
    preferred_foot_filter = st.selectbox('Filter by Preferred Foot', df['preferred_foot'].unique())

    # Filter the dataframe based on the selected preferred foot
    filtered_df = df[df['preferred_foot'] == preferred_foot_filter]

    # Add a range filter for overall rating
    overall_rating_range = st.slider('Filter by Overall Rating Range', min_value=df['overall_rating'].min(), max_value=df['overall_rating'].max(), value=(df['overall_rating'].min(), df['overall_rating'].max()))

    # Filter the dataframe based on the selected overall rating range
    filtered_df = filtered_df[(filtered_df['overall_rating'] >= overall_rating_range[0]) & (filtered_df['overall_rating'] <= overall_rating_range[1])]

    # Add a checkbox to show/hide high attacking work rate column
    show_high_attacking_work_rate = st.checkbox('Show High Attacking Work Rate')

    # Display the filtered dataframe
    if show_high_attacking_work_rate:
        st.write(filtered_df)
    else:
        st.write(filtered_df.drop(columns='attacking_work_rate'))

    # Create a histogram based on the filtered dataframe
    fig = px.histogram(filtered_df, x='overall_rating', title='Overall Rating Distribution', labels={'overall_rating':'Overall Rating'})
    st.plotly_chart(fig)

    # Create a scatter plot based on the filtered dataframe
    fig = px.scatter(filtered_df, x='potential', y='overall_rating', color='preferred_foot', title='Potential vs Overall Rating', labels={'potential':'Potential', 'overall_rating':'Overall Rating'})
    st.plotly_chart(fig)




st.caption("Created by Hector Marquez 😎")













