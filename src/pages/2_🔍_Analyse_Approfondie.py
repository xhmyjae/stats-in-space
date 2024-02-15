import pandas as pd
import altair as alt
import streamlit as st

data: pd.DataFrame = st.session_state['data']

st.title("L'évolution de l'open source sur **GitHub**")

st.header("Analyse avancée des données")

###
# - Évolution du nombre de dépôts par langage
###
st.subheader("- Évolution du nombre de dépôts par langage")
st.write("En examinant l'évolution de l'open source sur **GitHub**, nous pouvons mieux comprendre comment le nombre de "
         "dépôts par langage a évolué au fil du temps.")

###
# - Corrélations entre langages et topics
###
st.subheader("- Corrélations entre langages et topics")
st.write("Cette évolution du nombre de dépôts par langage nous permet d'approfondir notre analyse en examinant les "
         "corrélations entre langages et topics, pour comprendre les tendances émergentes dans différents domaines.")

###
# - Popularité relative des langages sur 1 an et 5 ans, par topic
###
st.subheader("- Popularité relative des langages sur 1 an et 5 ans, par topic")
st.write("En analysant les données sur la popularité relative des langages sur 1 an et 5 ans, par topic, nous pouvons "
         "identifier les langages qui gagnent en traction dans des domaines spécifiques sur différentes périodes de "
         "temps.")

###
# - Corrélation entre taille, licences, langages, topics
###
st.subheader("- Corrélation entre taille, licences, langages, topics")
st.write("Cette analyse nous conduit ensuite à explorer la corrélation entre la taille des projets, les licences "
         "utilisées, les langages et les topics, pour comprendre les facteurs qui influencent la croissance et la "
         "popularité des projets open source sur **GitHub**.")

metrics = ['Stars', 'Forks', 'Issues', 'Watchers', 'Size']
selected_repos = data.sample(n=5, random_state=42)

column1, column2 = st.columns(2)
columns = [column1, column2]

for i, metric in enumerate(metrics):
    columns[i % 2].write(f'Comparaison de `{metric}`')
    columns[i % 2].bar_chart(selected_repos, x='Name', y=metric)

###
# - Nombre de commits hebdomadaires des 1000 premiers dépôts
###
st.subheader("- Nombre de commits hebdomadaires des 1000 premiers dépôts")
st.write("Le nombre de commits hebdomadaires des 1000 premiers dépôts offre un aperçu précieux de l'activité de "
         "développement au sein de la communauté GitHub.")

###
# - Analyse de l'activité des commits par langages
###
st.subheader("- Analyse de l'activité des commits par langages")
st.write("En analysant l'activité des commits par langages, nous pouvons dégager des tendances significatives qui "
         "reflètent les préférences et les pratiques des développeurs dans différents langages de programmation.")

st.header("- Tendances de l'activité des dépôts populaires")
st.write("En résumé, en examinant l'évolution du nombre de dépôts par langage, nous pouvons ensuite explorer les "
         "corrélations entre langages et topics, ce qui nous permet d'analyser la popularité relative des langages "
         "sur différentes périodes de temps et enfin d'étudier la corrélation entre plusieurs facteurs clés dans "
         "l'écosystème open source de **GitHub**.")
