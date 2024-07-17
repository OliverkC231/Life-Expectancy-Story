import pandas as pd
import ssl
import streamlit as st
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
from streamlit.components.v1 import html

# Set the app title and configuration
st.set_page_config(page_title='Life Expectancy Streamlit Story', layout='centered')

# Center the title using HTML and CSS
st.markdown(
    """
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        width: 100%;
    }
    .title {
        font-size: 2.5em;
        margin-top: 0;
        margin-bottom: 0.5em;
    }
    </style>
    <div class="centered">
        <h1 class="title">You in the World</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Fix SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Load and prepare the data
uploaded_file = '/mnt/data/Life Expectancy Data.csv'  # Adjusted path for the uploaded file
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Create columns for the selections
col1, col2, col3 = st.columns(3)

with col1:
    country_list = df['Country'].drop_duplicates()
    selected_country = st.selectbox('Country:', country_list)

abr_country = df['ISO3_code'].loc[df['Country'] == selected_country].values[0]

# Determine the subregion for the selected country
subregion = df['Subregion'].loc[df['Country'] == selected_country].drop_duplicates().values[0]

continent = df['Continent'].loc[df['Country'] == selected_country].drop_duplicates().values[0]

with col2:
    gender_list = df['Gender'].drop_duplicates()
    selected_gender = st.radio('Gender:', gender_list)

g_type = df['G_Type'].loc[df['Country'] == selected_country].values[0]

with col3:
    # Number input for year with automatic generation matching
    selected_year = st.slider('Year Born', min_value=1950, max_value=2024, value=1980)
    age = 2024 - selected_year  # Calculate age based on the selected year

if st.button('Create Story'):

    # Wrap the presentation in a centered div
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    # Define the dimensions for the visualization
    width = 600
    height = 450

    # Initialize the ipyvizzu Data object
    vizzu_data = Data()
    vizzu_data.add_df(df)  # Use the updated DataFrame directly

    # Initialize the story
    story = Story(data=vizzu_data)

    # (Optional) Add slides to the story
    slide = Slide(
        Step(
            Config({
                "x": "Year",
                "y": "LifeExpectancy",
                "color": "Country",
                "label": "LifeExpectancy"
            }),
            Style({"plot": {"xAxis": {"label": {"angle": "45deg"}}}})
        )
    )
    story.add_slide(slide)

    # Display the story using Streamlit's HTML component
    html(story.to_html(width=width, height=height))

    # Close the centered div
    st.markdown('</div>', unsafe_allow_html=True)