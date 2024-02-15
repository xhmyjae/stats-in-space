from ast import literal_eval

import pandas as pd
import altair as alt
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
	data = pd.read_csv('../repositories.csv', parse_dates=['Created At', 'Updated At'])
	# Reading the 'Topics' column as a list of strings
	data['Topics'] = data['Topics'].apply(literal_eval)
	return data


data = load_data()
st.session_state['data'] = data


st.title("L'évolution de l'open source sur GitHub")

st.header("Contexte et problématique")

st.write(
	"""
GitHub est aujourd'hui l'une des plateformes les plus utilisées pour héberger et développer des projets open source. Au fil des années, le nombre de dépôts et de contributeurs n'a cessé de croître.

Dans ce projet, nous allons analyser un jeu de données issues de GitHub afin de mieux comprendre les tendances récentes de l'open source sur cette plateforme. Plus précisément, nous chercherons à répondre aux questions suivantes:

- Quels sont les langages et domaines qui connaissent la plus forte croissance ces dernières années ?
- Comment évolue le nombre moyen de contributeurs par projet ?
- Certains types de licences open source sont-ils plus populaires ?

En explorant ces différents indicateurs, nous pourrons dégager les grandes tendances qui façonnent l'avenir du développement libre collaboratif sur GitHub.
"""
)

if st.button("Passer à l'analyse des données"):
	st.switch_page("pages/1_🗃️_Première_Analyse.py")
