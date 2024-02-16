from ast import literal_eval
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

data: pd.DataFrame = st.session_state['data']
commits: pd.DataFrame = st.session_state['commits']
data['Slug'] = data['URL'].apply(lambda x: x.removeprefix('https://github.com/').removesuffix('/'))

st.title("L'évolution de l'open source sur **GitHub**")

st.header("Analyse avancée des données")

###
# - Évolution du nombre de dépôts par langage
###
st.subheader("- Évolution du nombre de dépôts par langage")
st.write("En examinant l'évolution de l'open source sur **GitHub**, nous pouvons mieux comprendre comment le nombre de "
         "dépôts par langage a évolué au fil du temps.")
merged_df = pd.merge(data, commits, left_on='Name', right_on='repo_slug')

# Groupement des données par langage et semaine
lang_week_df = merged_df.groupby(['Language', 'week']).size().reset_index(name='count')

# Créer un graphique Altair
chart = alt.Chart(lang_week_df).mark_line().encode(
    x='week:T',
    y='count:Q',
    color='Language:N',
    tooltip=['week:T', 'count:Q']
).properties(
    width=800,
    height=400
).interactive()

# Titre de l'application Streamlit
st.title('Évolution du nombre de dépôts par langage')

# Affichage du graphique Altair dans l'application Streamlit
st.altair_chart(chart)

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
st.subheader("- Nombre de commits mensuel des 1000 premiers dépôts")
st.write("Le nombre de commits mensuel des 1000 premiers dépôts offre un aperçu précieux de l'activité de "
         "développement au sein de la communauté GitHub.")

commits['commits_per_week'] = commits['total_commits'] / ((commits['week_next'] - commits['week']).dt.days / 7)
monthly_total_commits = commits.groupby(pd.Grouper(key='week', freq='M')).agg({'total_commits': 'sum'}).reset_index()
monthly_total_commits.rename(columns={'week': 'month'}, inplace=True)
chart = alt.Chart(monthly_total_commits).mark_line().encode(
    x=alt.X('month:T', title='Mois'),
    y=alt.Y('total_commits:Q', title='Nombre total de commits'),
    tooltip=[alt.Tooltip('month', title='Month'), alt.Tooltip('total_commits', title='Sommes des commits', format='.0f')]
).properties(
    width=800,
    height=400,
    title='Nombre total de commits mensuel pour tous les dépôts'
).interactive()
st.altair_chart(chart, use_container_width=True)

###
# - Analyse de l'activité des commits par langages
###
st.subheader("- Analyse de l'activité des commits par langages")
st.write("En analysant l'activité des commits par langages, nous pouvons dégager des tendances significatives qui "
         "reflètent les préférences et les pratiques des développeurs dans différents langages de programmation.")

df = commits.merge(data[['repo_slug', 'Language']], on='repo_slug')
commits_lang = df.groupby(['Language', df['week'].dt.year])['total_commits'].sum().reset_index()
top_langs = data['Language'].value_counts().index[:15]
top_repos = data[data['Language'].isin(top_langs)]
pivot = top_repos.pivot_table(index='Language', columns=top_repos['Created At'].dt.year, values='Name', aggfunc='count')
pivot = pivot.fillna(0)
pivot = pivot.reset_index().melt(id_vars='Language', var_name='Year', value_name='Repo Count')
chart = alt.Chart(pivot).mark_rect().encode(
    x='Year:O',
    y='Language:O',
    color='Repo Count:Q',
    tooltip=['Language', 'Year', 'Repo Count']
).properties(
    width=800,
    height=500,
    title='Nombre de repos par langage et année'
)

st.write(chart)

st.header("- Tendances de l'activité des dépôts populaires")
st.write("En résumé, en examinant l'évolution du nombre de dépôts par langage, nous pouvons ensuite explorer les "
         "corrélations entre langages et topics, ce qui nous permet d'analyser la popularité relative des langages "
         "sur différentes périodes de temps et enfin d'étudier la corrélation entre plusieurs facteurs clés dans "
         "l'écosystème open source de **GitHub**.")
