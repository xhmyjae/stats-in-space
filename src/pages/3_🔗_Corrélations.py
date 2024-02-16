import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import streamlit as st
import seaborn as sns

data: pd.DataFrame = st.session_state['data']
colors: dict[str, str] = st.session_state['colors']

st.title("Analyse des corrélations")

st.header("Corrélations multidimensionnelles")

st.subheader("- Corrélation étoiles, forks, taille")
st.write("Pour explorer les corrélations multidimensionnelles, nous nous penchons sur les corrélations spécifiques "
         "entre étoiles, forks et taille pour approfondir notre compréhension des relations entre ces métriques.")

data["Year"] = data["Created At"].dt.year
average_stats_by_year = data.groupby("Year").agg({
    "Stars": "mean",
    "Forks": "mean",
    "Size": "mean"
}).reset_index()

chart_stars = alt.Chart(average_stats_by_year).mark_bar(color='blue').encode(
    x='Year:N',
    y=alt.Y('Stars:Q', axis=alt.Axis(title='Nombre moyen')),
    tooltip=['Year:N', 'Stars:Q']
).properties(
    width=300,
    height=400,
    title='Nombre moyen de Stars par année'
)

chart_forks = alt.Chart(average_stats_by_year).mark_bar(color='green').encode(
    x='Year:N',
    y=alt.Y('Forks:Q', axis=alt.Axis(title='Nombre moyen')),
    tooltip=['Year:N', 'Forks:Q']
).properties(
    width=300,
    height=400,
    title='Nombre moyen de Forks par année'
)

chart_size = alt.Chart(average_stats_by_year).mark_bar(color='red').encode(
    x='Year:N',
    y=alt.Y('Size:Q', axis=alt.Axis(title='Nombre moyen')),
    tooltip=['Year:N', 'Size:Q']
).properties(
    width=300,
    height=400,
    title='Taille moyenne par année'
)

st.write(chart_stars, '\n', chart_forks, '\n', chart_size)

correlation = data[['Size', 'Stars', 'Forks']].corr()

st.write("Matrice de corrélation :")
st.write(correlation)

st.subheader("- Corrélation Has Issues, Has Projects, Has Wiki, Has Pages, Has Downloads, Has Discussions")
st.write("De plus, en complément de notre analyse précédente, nous examinons les corrélations entre Has Issues, "
         "Has Projects, Has Wiki, Has Pages, Has Downloads, Has Discussions pour saisir l'interconnexion entre les "
         "aspects fondamentaux des projets.")

variables = ['Has Issues', 'Has Projects', 'Has Wiki', 'Has Pages', 'Has Downloads', 'Has Discussions']

correlation_matrix = data[variables].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Corrélation entre les variables')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

st.pyplot(plt)

st.header("Dynamique temporelle")

st.subheader("- Évolution corrélations 2007-2022")
st.write(
	"Dans cette section sur la dynamique temporelle, nous examinons l'évolution des corrélations entre 2007 et "
	"2023, mettant en lumière les changements et les tendances au fil du temps."
)

variables = ['Size', 'Stars', 'Forks', 'Has Issues', 'Has Projects', 'Has Wiki', 'Has Pages', 'Has Downloads', 'Has Discussions', 'Year']
correlation_evolution = data[variables].groupby('Year').corr().reset_index()
correlation_evolution = correlation_evolution[correlation_evolution['level_1'] != 'Year']
correlation_evolution = correlation_evolution[correlation_evolution['level_1'] != 'Size']

chart = alt.Chart(correlation_evolution).mark_line().encode(
    x='Year:O',
    y='Size:Q',
    color='level_1:N',
    tooltip=['Year:O', 'Size:Q']
).properties(
    width=800,
    height=400,
    title='Évolution de la corrélation de la taille'
)

st.altair_chart(chart, use_container_width=True)

st.subheader("- Impact nouveaux langages sur corrélations")
st.write(
	"Ensuite, nous explorons l'impact des nouveaux langages sur ces corrélations. Cela nous permet de comprendre "
	"comment l'émergence de nouveaux outils influence les relations entre les différents paramètres analysés.")

# Filter languages with min repos
filtered_data = data.groupby('Language').filter(lambda x: len(x) > 10)

# Group by language
lang_groups = filtered_data.groupby('Language')

# Get first created date for each language
lang_first_created = lang_groups['Created At'].min().reset_index().sort_values('Created At', ascending=False)
# Sort by first created date and take last 12 languages
top_10_recent = lang_first_created.sort_values('Created At', ascending=False).head(10)['Language'].tolist()
data_top_languages = filtered_data[filtered_data['Language'].isin(top_10_recent)]

data_languages_per_year = data_top_languages.groupby(['Year', 'Language']).size().groupby(level='Language').cumsum().unstack()
chart = alt.Chart(data_languages_per_year.reset_index().melt('Year')).mark_line().encode(
    x=alt.X('Year:O', title='Année'),
    y=alt.Y('value:Q', title='Nombre de dépôts'),
    color=alt.Color(
        'Language:N',
        scale=alt.Scale(range=[colors.get(lang) or colors['Non-spécifié'] for lang in data_languages_per_year.columns])
    ),
)

st.altair_chart(chart, use_container_width=True)

data_top_languages['Has Issues'] = data_top_languages['Has Issues'].fillna(0)
data_top_languages['Has Projects'] = data_top_languages['Has Projects'].fillna(0)
data_top_languages['Has Wiki'] = data_top_languages['Has Wiki'].fillna(0)
data_top_languages['Has Pages'] = data_top_languages['Has Pages'].fillna(0)
data_top_languages['Has Downloads'] = data_top_languages['Has Downloads'].fillna(0)
data_top_languages['Has Discussions'] = data_top_languages['Has Discussions'].fillna(0)
correlation_matrix = data_top_languages[variables].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Corrélation entre les variables pour les 10 langages les plus récents')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

st.pyplot(plt)


st.header("Conclusion")
st.write("""
L'analyse approfondie des données de GitHub révèle des tendances clés dans l'écosystème du développement open source. 
Les axes de recherche examinent le choix des langages, la popularité des projets, les licences préférées et la croissance sectorielle. Les insights obtenus permettent de comprendre les préférences des développeurs, l'impact de l'engagement sur la réussite des projets et les dynamiques de collaboration. 
Ces informations sont précieuses pour guider les décisions stratégiques, les choix technologiques et les analyses de marché.""")
