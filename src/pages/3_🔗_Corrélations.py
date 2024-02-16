import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import streamlit as st

data: pd.DataFrame = st.session_state['data']

st.title("Analyse des corrélations")

st.header("Corrélations multidimensionnelles")

st.subheader("Corrélation étoiles, forks, taille")

# à faire : histogramme

st.subheader("Corrélation langages, topics, licences")

st.subheader("Corrélation commits, pull requests, issues")

st.subheader("Corrélation taille, étoiles, langages, topics")


st.header("Focus langages")


st.subheader("Corrélation Python variables")

st.subheader("Corrélation Java variables")

st.subheader("Corrélation JS variables")


st.header("Focus domaines")


st.subheader("Corrélation données, machine learning, variables")

st.subheader("Corrélation dévéloppement, tests, variables")


st.header("Dynamique temporelle")


st.subheader("Évolution corrélations 2007-2022")

st.subheader("Impact nouveaux langages sur corrélations")


st.header("Conclusion")
