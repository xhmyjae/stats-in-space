import dotenv
import os
import pandas as pd
from github import *
from github.StatsContributor import StatsContributor

dotenv.load_dotenv()

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')

GITHUB_API_URL = 'https://api.github.com'

auth = Auth.Token(GITHUB_API_TOKEN)

g = Github(auth=auth)


def fetch_commits(repo_slug: str) -> list[StatsContributor]:
	repo = g.get_repo(repo_slug)
	contributors = repo.get_stats_contributors()
	return contributors or []


repos = pd.read_csv('repositories.csv', parse_dates=['Created At', 'Updated At'])
repos['Slug'] = repos['URL'].apply(lambda x: x.removeprefix('https://github.com/').removesuffix('/'))

first_10_repos = repos['Slug'].head(10)

# We want to only store the total number of commits per week per repository
commits = pd.DataFrame(columns=['repo_slug', 'total_commits', 'week', 'week_next'])
# Store as [repo_slug, week, total_commits]
index = 0
for repo_slug in first_10_repos:
	contributors = fetch_commits(repo_slug)
	print(f"Fetched {len(contributors)} contributors for '{repo_slug}', total commits: {sum([c.total for c in contributors])}")

	oldest_date = min([c.weeks[0].w for c in contributors])
	latest_date = max([c.weeks[-1].w for c in contributors])
	weeks = pd.date_range(oldest_date, latest_date, freq='W')

	# Pre-process contributors weeks and store data in a dictionary with week as the key
	contributor_dict = {}
	for contributor in contributors:
		for week in contributor.weeks:
			if week.w not in contributor_dict:
				contributor_dict[week.w] = week.c
			else:
				contributor_dict[week.w] += week.c

	# Create a DataFrame with total commits per week
	commits_df = pd.DataFrame.from_dict(contributor_dict, orient='index', columns=['total_commits'])

	# Reset the index of the dataframe
	commits_df.reset_index(inplace=True)

	# Rename the columns
	commits_df.columns = ['week', 'total_commits']

	# Generating the other fields
	commits_df['repo_slug'] = repo_slug
	commits_df['week_next'] = commits_df['week'] + pd.DateOffset(weeks=1)

	# Reordering the columns
	commits_df = commits_df[['repo_slug', 'total_commits', 'week', 'week_next']]

	# Appending the dataframe to the commits dataframe

	commits = pd.concat([commits, commits_df], ignore_index=True)


commits.to_csv('commits.csv', index=False)
print(commits)
