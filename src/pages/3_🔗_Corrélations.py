import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import streamlit as st
import seaborn as sns

data: pd.DataFrame = st.session_state['data']

st.title("Analyse des corrélations")

st.header("Corrélations multidimensionnelles")

st.subheader("Corrélation étoiles, forks, taille")
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

st.write(chart_stars | chart_forks | chart_size)

correlation = data[['Size', 'Stars', 'Forks']].corr()

st.write("Matrice de corrélation :")
st.write(correlation)

st.subheader("Corrélation Has Issues, Has Projects, Has Wiki, Has Pages, Has Downloads, Has Discussions")
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

st.header("Focus langages")

st.subheader("Corrélation Python variables")

st.subheader("Corrélation Java variables")

st.subheader("Corrélation JS variables")

st.header("Dynamique temporelle")

st.subheader("Évolution corrélations 2007-2022")

st.subheader("Impact nouveaux langages sur corrélations")


st.header("Conclusion")
st.write("""
L'analyse approfondie des données de GitHub révèle des tendances clés dans l'écosystème du développement open source. 
Les axes de recherche examinent le choix des langages, la popularité des projets, les licences préférées et la croissance sectorielle. Les insights obtenus permettent de comprendre les préférences des développeurs, l'impact de l'engagement sur la réussite des projets et les dynamiques de collaboration. 
Ces informations sont précieuses pour guider les décisions stratégiques, les choix technologiques et les analyses de marché.""")
