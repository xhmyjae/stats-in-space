import time

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
	repo = g.get_repo(repo_slug, lazy=True)
	try:
		contributors = repo.get_stats_contributors()
	except GithubException as e:
		print(f"Error fetching contributors for '{repo_slug}': {e}")
		return []
	return contributors or []


repos = pd.read_csv('repositories.csv', parse_dates=['Created At', 'Updated At'])
repos['Slug'] = repos['URL'].apply(lambda x: x.removeprefix('https://github.com/').removesuffix('/'))

FETCH_COUNT = 1000
repos_to_fetch: list[str] = repos['Slug'].head(FETCH_COUNT).tolist()

# We want to only store the total number of commits per week per repository
commits = pd.DataFrame(columns=['repo_slug', 'total_commits', 'week', 'week_next'])

for i, repo_slug in enumerate(repos_to_fetch):
	contributors = fetch_commits(repo_slug)
	commits_count = sum([c.total for c in contributors])

	if g.rate_limiting[0] < 100:
		print(f"Rate limit reached, remaining: {g.rate_limiting[0]}, sleeping for 1 minute.")
		time.sleep(60)

	print(f"{i + 1}/{len(repos_to_fetch)} Fetched {len(contributors)} contributors for '{repo_slug}', total commits: {commits_count}, remaining rate limit: {g.rate_limiting[0]}")

	# If there are no contributors, skip to the next repository
	if not contributors:
		continue

	try:
		oldest_date = min([c.weeks[0].w for c in contributors])
		latest_date = max([c.weeks[-1].w for c in contributors])
		weeks = pd.date_range(oldest_date, latest_date, freq='W')
	except GithubException:
		print(f"Error generating date range for '{repo_slug}', skipping.")
		continue
	except ValueError:
		print(f"Error generating date range for '{repo_slug}', skipping.")
		continue
	except BaseException as e:
		print(f"Error generating date range for '{repo_slug}', skipping: {e}")
		continue

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
	if commits.empty:
		commits = commits_df
	else:
		commits = pd.concat([commits, commits_df], ignore_index=True)


commits.to_csv('commits.csv', index=False)
commits.info()
