import pandas as pd
import altair as alt
import streamlit as st

data: pd.DataFrame = st.session_state['data']


st.header("Données brutes")

st.dataframe(data, column_config={
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

count_by_year = data.groupby([data['Created At'].dt.year]).size()
count_by_year.name = 'Nombre de repos'
count_by_year = count_by_year.reset_index()

chart = alt.Chart(count_by_year).mark_bar().encode(
	x=alt.X('Created At:O', title='Année'),
	y=alt.Y('Nombre de repos:Q', title='Nombre de repos'),
	tooltip=['Created At', 'Nombre de repos']
).properties(
	width=800,
	height=400
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Nombre de repos par langage")

st.subheader("- Parts de marché des 10 langages les plus populaires, à partir de la colonne `Language`")

st.subheader("- Moyenne du nombre d'étoiles (Stars) gagnées chaque année")

st.subheader("- Nombre de dépôts par licence (License) open source")

st.subheader("- Taux de croissance annuel du nombre de projets par domaine (Topics)")

st.subheader("- Corrélation entre le nombre d'étoiles et le nombre de forks")


st.header("Ces graphiques permettront d'analyser:")


st.subheader("- La croissance globale de GitHub")

st.subheader("- Les langages et domaines qui connaissent le plus de succès")

st.subheader("- L'impact des forks sur la popularité des projets")

st.subheader("- Les licences open source préférées des développeurs")

if st.button("Passer à l'analyse approfondie"):
	st.switch_page("pages/🔍_Analyse_Approfondie.py")
