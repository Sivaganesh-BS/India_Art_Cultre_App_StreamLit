import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
import base64

st.set_page_config(
    page_title="Traditional Art, Cultural Experiences, and Tourism in India",
    layout="wide",
    initial_sidebar_state="expanded",
)
IMAGE_PATH = "image_atr_cultre.png"
BACKGROUND_IMAGE = os.path.join(IMAGE_PATH)


def set_background(image_path):
    """
    Set a single background image for the entire app.
    """
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    encoded_img = base64.b64encode(img_bytes).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply Background
set_background(BACKGROUND_IMAGE)


# Sidebar Navigation
st.sidebar.title("Navigation")
pages = [
    "Home", "Art Forms Analysis", "Experience Analysis", "Tourism Analysis", 
    "State-wise Art Popularity", "Experience Categories", "Tourism by Type",
     "Top 5 Experiences", "Top 5 Destinations"
]
page = st.sidebar.radio("Select a Section", pages)

# Load Data Function
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

# Paths to data files
art_forms_path = "data/art_forms.csv"
tourism_data_path = "data/tourism_data.csv"
experiences_path = "data/experiences.csv"

# Load data
art_data = load_data(art_forms_path)
tourism_data = load_data(tourism_data_path)
experiences_data = load_data(experiences_path)

# Home Page
if page == "Home":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Traditional Art, Cultural Experiences, and Tourism in India")
        st.markdown("### Explore the cultural heritage of India through interactive visualizations.")
    with col2:
        image = Image.open(BACKGROUND_IMAGE)
        st.image(image, use_container_width=True)

# Art Forms Analysis
elif page == "Art Forms Analysis":
    st.title("Art Forms Analysis")
    st.markdown("### Table of Contents")
    st.markdown("- Overview")
    st.markdown("- Data Analysis")
    st.markdown("- Visualizations")
    if not art_data.empty:
        col1, col2 = st.columns([2, 1])  # Larger table, smaller graph
        with col1:
            st.markdown("### Data Overview")
            st.dataframe(art_data, use_container_width=True)
        with col2:
            fig = px.bar(art_data, x='Type', y='Art Form', color='State', title="Distribution of Art Forms by Type")
            st.plotly_chart(fig, use_container_width=True)

elif page == "Experience Analysis":
    st.title("Experience Analysis")
    if not experiences_data.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Experience Data")
            st.dataframe(experiences_data, use_container_width=True)
        with col2:
            fig = px.bar(experiences_data, x='Category', y='Experience', color='State', title="Distribution of Experiences by Category")
            st.plotly_chart(fig, use_container_width=True)

elif page == "Tourism Analysis":
    st.title("Tourism Analysis")
    if not tourism_data.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Tourism Data")
            st.dataframe(tourism_data, use_container_width=True)
        with col2:
            fig = px.bar(tourism_data, x='Type', y='Tourist Destination', color='State', title="Tourism Analysis by Type")
            st.plotly_chart(fig, use_container_width=True)

elif page == "State-wise Art Popularity":
    st.title("State-wise Art Popularity")
    if not art_data.empty:
        st.markdown("### Art Forms by State")
        fig = px.bar(art_data, x='State', y='Art Form', color='Type', title="Art Forms by State")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Experience Categories":
    st.title("Experience Categories")
    if not experiences_data.empty:
        st.markdown("### Experience Categories Distribution")
        fig = px.bar(experiences_data, x='Category', y='Experience', color='State', title="Experiences by Category")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Tourism by Type":
    st.title("Tourism by Type")
    if not tourism_data.empty:
        st.markdown("### Tourism Analysis by Type")
        fig = px.pie(tourism_data, names='Type', title="Distribution of Tourism Types")
        st.plotly_chart(fig, use_container_width=True)


elif page == "Top 5 Experiences":
    st.title("Top 5 Experiences")
    if not experiences_data.empty:
        # Convert 'Popularity' to numeric
        experiences_data['Popularity'] = pd.to_numeric(experiences_data['Popularity'], errors='coerce')
        top_5_experiences = experiences_data.nlargest(5, 'Popularity')
        st.dataframe(top_5_experiences, use_container_width=True)

elif page == "Top 5 Destinations":
    st.title("Top 5 Destinations")
    if not tourism_data.empty:
        # Convert 'Popularity' to numeric
        tourism_data['Popularity'] = pd.to_numeric(tourism_data['Popularity'], errors='coerce')
        top_5_destinations = tourism_data.nlargest(5, 'Popularity')
        st.dataframe(top_5_destinations, use_container_width=True)