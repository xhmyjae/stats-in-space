from ast import literal_eval
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

data: pd.DataFrame = st.session_state['data']
commits: pd.DataFrame = st.session_state['commits']
colors: dict[str, str] = st.session_state['colors']
data['Slug'] = data['URL'].apply(lambda x: x.removeprefix('https://github.com/').removesuffix('/'))

st.title("L'évolution de l'open source sur **GitHub**")

st.header("Analyse avancée des données")

###
# - Évolution du nombre de dépôts par langage
###
st.subheader("- Évolution du nombre de dépôts par langage")
st.write("En examinant l'évolution de l'open source sur **GitHub**, nous pouvons mieux comprendre comment le nombre de "
         "dépôts par langage a évolué au fil du temps.")

# take only the 10 most popular languages, do not filter
top_10_languages = data['Language'].value_counts().nlargest(10).index
data_top_languages = data[data['Language'].isin(top_10_languages)]

data_languages_per_year = data_top_languages.groupby(['Created At Year', 'Language']).size().groupby(level='Language').cumsum().unstack()

chart = alt.Chart(data_languages_per_year.reset_index().melt('Created At Year')).mark_line().encode(
    x=alt.X('Created At Year:O', title='Année'),
    y=alt.Y('value:Q', title='Nombre de dépôts'),
    color=alt.Color(
        'Language:N',
        scale=alt.Scale(range=[colors[lang] for lang in data_languages_per_year.columns])
    ),
)
st.altair_chart(chart, use_container_width=True)

###
# - Corrélations entre langages et topics
###
st.subheader("- Corrélations entre langages et topics")
st.write("Cette évolution du nombre de dépôts par langage nous permet d'approfondir notre analyse en examinant les "
         "corrélations entre langages et topics, pour comprendre les tendances émergentes dans différents domaines.")

# Plot qui compare 'Language' avec le nombre de repositories, récupère top 8 des langages les plus présents dans les topics et liste les langages
expanded_topics = data.explode('Topics')

none_value = 'Non-spécifié'
top_topics = expanded_topics['Topics'].value_counts().head(10).index
filtered_repositories = expanded_topics[expanded_topics['Topics'].isin(top_topics)]
filtered_repositories.loc[:, 'Language'] = filtered_repositories['Language'].fillna(none_value)
top_used_languages = filtered_repositories['Language'].value_counts().head(10).index
filtered_repositories = filtered_repositories[filtered_repositories['Language'].isin(top_used_languages)]

# 1 Horizontal stacked bar plot
top_languages_grouped_with_topics: pd.DataFrame = filtered_repositories.groupby(['Language', 'Topics']).size().unstack()
top_languages_grouped_with_topics['sum'] = top_languages_grouped_with_topics.sum(axis=1)
# Sorted by the sum number of repositories of each language
top_languages_grouped_with_topics.sort_values(by='sum', ascending=True, inplace=True)
top_languages_grouped_with_topics.drop(columns='sum', inplace=True)


chart = alt.Chart(top_languages_grouped_with_topics.reset_index().melt('Language')).mark_bar().encode(
    x=alt.X('value:Q', title='Nombre de dépôts'),
    y=alt.Y('Language:N', sort='-x'),
    color=alt.Color('Topics:N', scale=alt.Scale(scheme='tableau20')),
    tooltip=['Language', 'Topics']
)

st.altair_chart(chart, use_container_width=True)



# A VOIR POUR VIRER
###
# - Popularité relative des langages sur 1 an et 5 ans, par topic
###
st.subheader("- Popularité relative des langages sur 1 an et 5 ans, par topic")
st.write("En analysant les données sur la popularité relative des langages sur 1 an et 5 ans, par topic, nous pouvons "
         "identifier les langages qui gagnent en traction dans des domaines spécifiques sur différentes périodes de "
         "temps.")

year = 2020
# Filtrer sur les top 10 topics
top_topics = expanded_topics['Topics'].value_counts().head(10).index
filtered_repos = expanded_topics[expanded_topics['Topics'].isin(top_topics)]

# Remplir les valeurs manquantes de Language
filtered_repos['Language'].fillna(none_value, inplace=True)

# Garder les 10 langages principaux
top_langs = filtered_repos['Language'].value_counts().head(10).index
filtered_repos = filtered_repos[filtered_repos['Language'].isin(top_langs)]

# Popularité relative sur 1 an
one_year = filtered_repos[filtered_repos['Created At'] >= pd.to_datetime(f'{year}-01-01').tz_localize('UTC')]
lang_pop_1yr = one_year.groupby('Topics')['Language'].value_counts(normalize=True)

# Popularité relative sur 5 ans
five_years = filtered_repos[filtered_repos['Created At'] >= pd.to_datetime(f'{year - 5}-01-01').tz_localize('UTC')]
lang_pop_5yr = five_years.groupby('Topics')['Language'].value_counts(normalize=True)

chart_1yr = alt.Chart(lang_pop_1yr.reset_index(name='Popularity')).mark_bar().encode(
    x='Popularity:Q',  # 'Popularity:Q', title='Popularité relative
    y=alt.Y('Language:N', sort='-x'),
    color='Topics:N',
    tooltip=['Language', 'Topics', 'Popularity']
).properties(
    title=f'Popularité relative des langages par topic en {year}'
)

chart_5yr = alt.Chart(lang_pop_5yr.reset_index(name='Popularity')).mark_bar().encode(
    x='Popularity:Q',  # 'Popularity:Q', title='Popularité relative
    y=alt.Y('Language:N', sort='-x'),
    color='Topics:N',
    tooltip=['Language', 'Topics', 'Popularity']
).properties(
    title=f'Popularité relative des langages par topic en {year - 5}'
)

st.altair_chart(chart_1yr, use_container_width=True)
st.altair_chart(chart_5yr, use_container_width=True)

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
monthly_total_commits = commits.groupby(pd.Grouper(key='week', freq='ME')).agg({'total_commits': 'sum'}).reset_index()
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

data['repo_slug'] = data['Slug']
# Jointure sur repo_slug
df = commits.merge(data[['repo_slug', 'Language']], on='repo_slug')
commits_lang = df.groupby(['Language', df['week'].dt.year])['total_commits'].sum().reset_index()

# Trier et prendre les 15 premiers langages
top_langs = commits_lang['Language'].value_counts().index[:15]
commits_lang = commits_lang[commits_lang['Language'].isin(top_langs)]
commits_lang = commits_lang.sort_values(by='total_commits', ascending=False)

pivot = commits_lang.pivot_table(index='Language', columns='week', values='total_commits', aggfunc='sum')
pivot = pivot.fillna(0)

chart = alt.Chart(pivot.reset_index().melt('Language')).mark_rect().encode(
    x=alt.X('week:O', title='Année'),
    y=alt.Y('Language:N', sort='-x'),
    color=alt.Color('value:Q', title='Nombre de commits')
).properties(
    width=800,
    height=500,
    title='Nombre de commits mensuel par langage'
)


st.write(chart)

st.header("- Tendances de l'activité des dépôts populaires")
st.write("En résumé, en examinant l'évolution du nombre de dépôts par langage, nous pouvons ensuite explorer les "
         "corrélations entre langages et topics, ce qui nous permet d'analyser la popularité relative des langages "
         "sur différentes périodes de temps et enfin d'étudier la corrélation entre plusieurs facteurs clés dans "
         "l'écosystème open source de **GitHub**.")

if st.button("Passer aux corrélations"):
    st.switch_page("pages/3_🔗_Corrélations.py")
