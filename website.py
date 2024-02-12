import math
from ast import literal_eval

import pandas as pd
import altair as alt
import streamlit as st

st.title('Data Analyse')


@st.cache_data
def load_data() -> pd.DataFrame:
	data = pd.read_csv('repositories.csv', parse_dates=['Created At', 'Updated At'])
	# Reading the 'Topics' column as a list of strings
	data['Topics'] = data['Topics'].apply(literal_eval)
	return data


data_load_state = st.text('Chargement des données...')
data = load_data()
data_load_state.empty()

with st.expander('Voir les données brutes'):
	st.write("Voici un aperçu des données :")
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

st.divider()

st.markdown(
	"""
### GitHub, un pilier du monde du développement

1. 94 millions de développeurs dont 20,5 millions de nouvelles recrues en 2022
2. 1 milliard de $ de revenus en 2022
3. 3,5 milliards de contributions. 85,7 millions de nouveaux repos créés via GitHub en 2023
4. 90 % des contributeurs de projets open source proviennent de GitHub
5. Ancrée dans le monde des affaires, la filiale rencontre peu de difficultés pour s’imposer auprès de grands groupes.

### Que permet un repos GitHub populaire ?

1. **Visibilité accrue :** Les repos populaires attirent l'attention, meilleure visibilité du projet et intérêt communautaire.
2. **Contributions collaboratives :** Encouragent les contributions externes (pull requests), donc qualité du code et favorise une collaboration ouverte.
3. **Feedback et améliorations :** Les issues permettent d'identifier les bugs, demander des fonctionnalités et discuter des améliorations, favorisant ainsi le développement continu et la satisfaction des utilisateurs.
4. **Diversité des cas d'utilisation :** Avec les forks, les développeurs peuvent adapter le projet à divers besoins, fournissant des idées pour des fonctionnalités et améliorations pour rendre le projet plus polyvalent et adaptable.
5. **Réputation et validation :** Renforce la réputation du développeur en validant la qualité de son travail, peut avoir un impact positif sur sa carrière professionnelle et ses projets futurs.

Pour améliorer les statistiques d'un dépôt Github, il est crucial de comprendre différents aspects tels que l'engagement de la communauté, la qualité du code, la fréquence des mises à jour, etc.
Nous allons donc voir plusieurs aspects avec des graphiques et des analyses pour comprendre les statistiques d'un dépôt Github.

Pour ce faire, nous allons utiliser deux csv :
- `repositories.csv` : contient des informations sur les dépôts.
- `X.csv` : contient des informations sur les commits, les problèmes, les étoiles, les fourches, etc.
"""
)


st.header("1. Tendance des mises à jour au fil du temps.", divider='grey')

st.write('Graphique de la fréquence des mises à jour par rapport au temps (Updated At vs. Created At) :')
count_by_year = data.groupby([data['Created At'].dt.year]).size()
updated_by_counts = data.groupby([data['Updated At'].dt.year]).size()
st.line_chart(pd.concat([count_by_year, updated_by_counts], axis=1, keys=['Created At', 'Updated At']))

st.write('Graphique de la croissance de la taille du code en moyenne au fil du temps (Ko).')
data['Created At Year'] = data['Created At'].dt.year
created_by_year_size: pd.Series = data.groupby('Created At Year')['Size'].mean()
created_by_year_size /= 1024  # Convert to Ko
created_by_year_size.index = created_by_year_size.index.astype(str)
st.line_chart(created_by_year_size)


st.header('2. Engagement de la communauté', divider='grey')

st.write("Graphique du nombre d'étoiles (Stars) et de fourches (Forks) par rapport au temps.")
avg_stars_by_year = data.groupby('Created At Year')['Stars'].mean()
avg_forks_by_year = data.groupby('Created At Year')['Forks'].mean()
st.line_chart(pd.concat([avg_stars_by_year, avg_forks_by_year], axis=1, keys=['Stars', 'Forks']))


st.header('3. Analyse du code', divider='grey')

st.write('Graphique des 25 langages les plus utilisés :')


@st.cache_data
def get_github_colors() -> dict[str, str]:
	json = pd.read_json('colors.json')
	# json is an of [{[k: string]: {color: string}}]

	colors = {'Non-spécifié': 'grey'}
	item: str
	for item in json:
		colors[item] = json[item]['color']
	return colors


colors = get_github_colors()

none_value = 'Non-spécifié'
data['Language'] = data['Language'].fillna(none_value)
data_languages = data.groupby('Language').size().reset_index().sort_values(ascending=True, by=0).tail(25)

data_languages['color'] = data_languages['Language'].apply(lambda x: colors[x] if x in colors else colors[none_value])
data_languages.columns = ['Language', 'Nombre de dépôts', 'color']
chart = alt.Chart(data_languages).mark_bar().encode(
	x=alt.X('Language', sort='-y'),
	y=alt.Y('Nombre de dépôts:Q', title='Nombre de dépôts'),
	color=alt.Color('color', scale=None),
)
st.altair_chart(chart, use_container_width=True)


st.write("Graphique de l'évolution de l'utilisation des langages de programmation au fil du temps.")
data_languages_per_year = data.groupby('Language').filter(lambda x: len(x) > 10_000).groupby(
	['Created At Year', 'Language']
).size().unstack()

chart = alt.Chart(data_languages_per_year.reset_index().melt('Created At Year')).mark_line().encode(
	x=alt.X('Created At Year:O', title='Année'),
	y=alt.Y('value:Q', title='Nombre de dépôts'),
	color=alt.Color(
		'Language:N',
		scale=alt.Scale(range=[colors[lang] for lang in data_languages_per_year.columns])),
)
st.altair_chart(chart, use_container_width=True)

st.write('Graphique de la taille moyenne des fichiers par langage de programmation.')

data['Language'] = data['Language'].fillna(none_value)
data_languages = data.groupby('Language')['Size'].mean().reset_index().sort_values(ascending=True, by='Size').tail(25)
data_languages['Size'] /= 1024  # Convert to Ko

data_languages['color'] = data_languages['Language'].apply(lambda x: colors[x] if x in colors else colors[none_value])
data_languages.columns = ['Language', 'Taille moyenne des fichiers (Ko)', 'color']
chart = alt.Chart(data_languages).mark_bar().encode(
	x=alt.X('Language', sort='-y'),
	y=alt.Y('Taille moyenne des fichiers (Ko):Q', title='Taille moyenne des fichiers (Ko)'),
	color=alt.Color('color', scale=None),
)

st.altair_chart(chart, use_container_width=True)


st.header('4. Relation entre différentes métriques', divider='grey')

st.write("Corrélation entre le nombre d'étoiles (Stars) et le nombre de tickets (Issues).")
data['Stars'] = data['Stars'].fillna(0)
data['Issues'] = data['Issues'].fillna(0)
st.scatter_chart(data, x='Stars', y='Issues')


st.header('7. Analyse comparative', divider='grey')

st.write('Comparaison des métriques entre différents dépôts pour identifier les meilleures pratiques.')

metrics = ['Stars', 'Forks', 'Issues', 'Watchers', 'Size']
selected_repos = data.sample(n=5, random_state=42)

column1, column2 = st.columns(2)
columns = [column1, column2]

for i, metric in enumerate(metrics):
	columns[i % 2].write(f'Comparaison de `{metric}`')
	columns[i % 2].bar_chart(selected_repos, x='Name', y=metric)
