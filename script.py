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
        <h1 class="title">💀 Life Expectancy Story 💀</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Fix SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Load and prepare the data
uploaded_file = 'Data.csv' 
df = pd.read_csv(
    uploaded_file, encoding='ISO-8859-1',
    dtype={'Year': str},
)

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

    # Slide 1: No. of people with the same sex, born in the same year, same country
    slide1 = Slide(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}' && record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'x': 'Life Expectancy',
                    'y': 'Title',
                    'color': 'Title',
                    'label': 'Life Expectancy',
                    'title': f"Your Age Compared to Your Life Expectancy at Birth ({abr_country})"
                }
            ),
            Style(
                {
                    "plot": {
                        "xAxis": {"label": {"fontSize": 9, "angle": 0.0}},
                        "yAxis": {"label": {"fontSize": 9, "angle": 0.0}},
                        "marker": {
                            "colorPalette": "#FFD700 #1E90FF"
                        },
                    }
                }
            ),
        )
    )
    story.add_slide(slide1)

    slide2 = Slide(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}' && record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}'"),
             Config(
                {
                    'x': 'Title',
                    'y': 'Pecent',
                    'coordSystem': 'polar',
                    'title': 'Percent of Your Life Completed'
                }
            )
        )
    )
    story.add_slide(slide2)

    slide3 = Slide(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}' && record['Country'] == '{selected_country}' && record['Title'] == 'Life Expectancy'"),
            Config(
                {
                    'x': 'Life Expectancy',
                    'y': 'Gender',
                    'color': 'Gender',
                    'title': f"Life Expectancy for Men and Women at birth in {selected_year} ({abr_country})"
                }
            ),
            Style(
                {
                    "plot": {
                        "xAxis": {"label": {"fontSize": 9, "angle": 0.0}},
                        "yAxis": {"label": {"fontSize": 9, "angle": 0.0}},
                        "marker": {
                            "colorPalette": "#FFD700 #1E90FF"
                        },
                    }
                }
            ),
        )
    )
    story.add_slide(slide3)

    slide4 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}' && record['Title'] == 'Life Expectancy'"),
            Config.bar(
                {
                    'x': 'Year',
                    'y': 'Life Expectancy',
                    'color': 'Year',
                    'title': f"Life Expectancy for {selected_gender}s Over the Years ({abr_country})"
                }
            ),
            Style(
                {
                    "plot": {
                        "xAxis": {"label": {"fontSize": 7.5, "angle": 2.0}},
                        "yAxis": {"label": {"fontSize": 9, "angle": 0.0}},
                        "marker": {
                            "colorPalette": "#FFD700 #1E90FF"
                        },
                    }
                }
            ),
        )
    )
    story.add_slide(slide4)

    slide5 = Slide(
        Step(
            Data.filter(f"record['Subregion'] == '{subregion}' && record['Gender'] == '{selected_gender}' && record['Year'] == '{selected_year}' && record['Title'] == 'Life Expectancy'"),
            Config.bar(
                {
                    'x': 'Country',
                    'y': 'Life Expectancy',
                    'color': 'Country',
                    'label': 'ISO3_code',
                    'sort': 'byValue',
                    'title': f"Life Expectancy in {subregion} for {selected_gender}s ({selected_year})"
                }
            ),
            Style(
                {
                    "plot": {
                        "xAxis": {"label": {"fontSize": 7.5, "angle": 2.0}},
                        "yAxis": {"label": {"fontSize": 9, "angle": 0.0}}
                    }
                }
            ),
        )
    )
    story.add_slide(slide5)

    slide6 = Slide(
        Step(
            Data.filter(f"record['Continent'] == '{continent}' && record['Gender'] == '{selected_gender}' && record['Year'] == '{selected_year}' && record['Title'] == 'Life Expectancy'"),
            Config.bar(
                {
                    'x': 'Country',
                    'y': 'Life Expectancy',
                    'color': 'Country',
                    'sort': 'byValue',
                    'title': f"Life Expectancy in {continent} for {selected_gender}s ({selected_year})"
                }
            )
        )
    )
    story.add_slide(slide6)

    slide7 = Slide(
        Step(
            Data.filter(f"record['Gender'] == '{selected_gender}' && record['Year'] == '{selected_year}' && record['Title'] == 'Life Expectancy'"),
            Config.bar(
                {
                    'x': 'Country',
                    'y': 'Life Expectancy',
                    'color': 'Country',
                    'sort': 'byValue',
                    'title': f"Life Expectancy Worldwide for {selected_gender}s ({selected_year})"
                }
            )
        )
    )
    story.add_slide(slide7)

    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'Life-Expectancy-{selected_country}.html', mime='text/html')

    # Close the centered div
    st.markdown('</div>', unsafe_allow_html=True)
