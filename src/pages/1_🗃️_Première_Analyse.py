import pandas as pd
import altair as alt
import streamlit as st

data: pd.DataFrame = st.session_state['data']
colors: dict[str, str] = st.session_state['colors']

st.header("Données brutes")

st.dataframe(data.head(1000), column_config={
    'Created At': st.column_config.DatetimeColumn(
        "Date de création",
        format="D/MM/YYYY à HH:mm",
    ),
    'Updated At': st.column_config.DatetimeColumn(
        "Date de mise à jour",
        format="D/MM/YYYY à HH:mm",
    ),
    'URL': st.column_config.LinkColumn(),
    'Homepage': st.column_config.LinkColumn(),
    'Topics': st.column_config.ListColumn(),
})

st.header("Analyse basique des données")

st.subheader("Nombre de repos dans le temps")

count_by_year = data.groupby('Created At Year').size()
count_by_year.name = 'Nombre de repos'
count_by_year = count_by_year.reset_index()

chart = alt.Chart(count_by_year).mark_bar().encode(
    x=alt.X('Created At Year:O', title='Année'),
    y=alt.Y('Nombre de repos:Q', title='Nombre de repos'),
    tooltip=['Created At Year', 'Nombre de repos']
).properties(
    width=800,
    height=400
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Nombre de repos par langage")

###
# - Parts de marché des 10 langages les plus populaires, à partir de la colonne `Language`
###
st.subheader("- Parts de marché des 10 langages les plus populaires, à partir de la colonne `Language`")
st.write("En analysant le nombre de repos par langage, nous pouvons comprendre les parts de marché des 10 langages "
         "les plus populaires, illustrées à partir de la colonne `Language`.")


none_value = 'Non-spécifié'
data['Language'] = data['Language'].fillna(none_value)
data_languages = data.groupby('Language').size().reset_index().sort_values(ascending=True, by=0).tail(10)

data_languages['color'] = data_languages['Language'].apply(lambda x: colors[x] if x in colors else colors[none_value])
data_languages.columns = ['Language', 'Nombre de dépôts', 'color']
chart = alt.Chart(data_languages).mark_bar().encode(
    x=alt.X('Language', sort='-y'),
    y=alt.Y('Nombre de dépôts:Q', title='Nombre de dépôts'),
    color=alt.Color('color', scale=None),
)
st.altair_chart(chart, use_container_width=True)

###
# - Nombre d'étoiles des projets cumulées par année
###
st.subheader("- Moyenne du nombre d'étoiles (Stars) gagnées chaque année")
st.write("Cette analyse des parts de marché nous permet ensuite d'examiner le nombre d'étoiles des projets cumulées par "
            "année, offrant une perspective sur la popularité des projets de la plateforme.")

cumulative_stars_by_year = data.groupby('Created At Year str')['Stars'].sum().cumsum()
st.line_chart(cumulative_stars_by_year)

###
# - Nombre de dépôts par licence (`License`) open source
###
st.subheader("- Nombre de dépôts par licence (`License`) open source")
st.write("La popularité des projets étant évaluée, nous pouvons ensuite examiner les données sur le nombre de dépôts "
         "par licence open source pour comprendre les préférences de licence des développeurs travaillant dans ces "
         "langages.")

data_licenses = data.groupby('License').size().reset_index().sort_values(ascending=True, by=0).tail(10)
data_licenses.columns = ['License', 'Nombre de dépôts']
chart = alt.Chart(data_licenses).mark_bar().encode(
    x=alt.X('License', sort='-y'),
    y=alt.Y('Nombre de dépôts:Q', title='Nombre de dépôts'),
)
st.altair_chart(chart, use_container_width=True)

###
# - Taux de croissance annuel du nombre de projets par domaine (`Topics`)
###
st.subheader("- Taux de croissance annuel du nombre de projets par domaine (`Topics`)")
st.write("En parallèle, l'étude du taux de croissance annuel du nombre de projets par domaine nous permet de détecter "
         "les tendances émergentes, potentiellement influencées par les choix de licence et la popularité des "
         "langages.")

# limite to topics having more than 1000 repos
growth_by_topic = data.explode('Topics').groupby([data['Created At'].dt.year, 'Topics']).size().unstack().fillna(0)
growth_by_topic = growth_by_topic[growth_by_topic.sum().sort_values(ascending=False).head(10).index]
growth_by_topic = growth_by_topic.diff(axis=0).fillna(0).cumsum()
st.line_chart(growth_by_topic)

###
# - Corrélation entre le nombre d'étoiles et le nombre de forks
###
st.subheader("- Corrélation entre le nombre d'étoiles et le nombre de forks")
st.write("Cette analyse des tendances émergentes nous amène à examiner la corrélation entre le nombre d'étoiles et le "
         "nombre de forks, pour comprendre l'impact des forks sur la popularité des projets, notamment dans les "
         "domaines en croissance.")

repositories_per_month = data.groupby(data['Created At'].dt.strftime('%Y-%m')).agg({'Stars': 'mean', 'Forks': 'mean'})
stars_chart = alt.Chart(repositories_per_month.reset_index()).mark_line().encode(
    x='Created At:T',
    y='Stars:Q',
    color=alt.value('yellow')
)
forks_chart = alt.Chart(repositories_per_month.reset_index()).mark_line().encode(
    x='Created At:T',
    y='Forks:Q',
)

st.altair_chart(stars_chart + forks_chart, use_container_width=True)

st.header("Ces graphiques permettront d'analyser:")

###
# - La croissance globale de **GitHub**
###
st.subheader("- La croissance globale de **GitHub**")
st.write(
    "Ces données, combinées à une analyse de la croissance globale de **GitHub**, fournissent un contexte plus large "
    "pour interpréter les tendances observées dans chaque domaine et langage.")

###
# - Les langages et domaines qui connaissent le plus de succès
###
st.subheader("- Les langages et domaines qui connaissent le plus de succès")
st.write("Les tendances observées dans la croissance globale de **GitHub** nous orientent vers une analyse plus "
         "approfondie des langages et domaines les plus populaires, pour comprendre ce qui contribue au succès sur la "
         "plateforme.")

###
# - L'impact des forks sur la popularité des projets
###
st.subheader("- L'impact des forks sur la popularité des projets")
st.write("En se basant sur ces analyses, l'impact des forks sur la popularité des projets peut être étudié de manière "
         "plus spécifique, en tenant compte des tendances observées dans les langages et domaines spécifiques.")

###
# - Les licences open source préférées des développeurs
###
st.subheader("- Les licences open source préférées des développeurs")
st.write("Enfin, l'analyse des licences open source préférées des développeurs offre une perspective supplémentaire "
         "sur les choix de licence dans la communauté, influencée par les tendances observées dans la popularité des "
         "langages et des projets.")

if st.button("Passer à l'analyse approfondie"):
    st.switch_page("pages/2_🔍_Analyse_Approfondie.py")
