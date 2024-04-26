import pandas as pd
import requests

# Function to check for YAML files in the .github/workflows directory and dependabot.yml in the .github directory
def check_repository_files(owner, repo, github_token):
    workflows_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows"
    dependabot_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.github/dependabot.yml"
    headers = {"Authorization": f"token {github_token}"}
    has_yaml_in_workflows = False
    has_dependabot = False

    # Check for YAML files in the workflows directory
    try:
        response = requests.get(workflows_api_url, headers=headers)
        response.raise_for_status()
        for file in response.json():
            if file['name'].endswith('.yml') or file['name'].endswith('.yaml'):
                has_yaml_in_workflows = True
                break  # Found a YAML file, no need to check further
    except requests.HTTPError as e:
        print(f"Error checking workflows in {owner}/{repo}: {e}")

    # Check for dependabot.yml file in the .github directory
    try:
        response = requests.get(dependabot_api_url, headers=headers)
        if response.status_code == 200:
            has_dependabot = True
    except requests.HTTPError as e:
        print(f"Error checking dependabot.yml in {owner}/{repo}: {e}")

    return has_yaml_in_workflows, has_dependabot

# Replace 'your_github_token_here' with your GitHub Personal Access Token
github_token = 'Put your own token'

# Assuming you have a DataFrame 'df' loaded from an Excel file as before
# Update the path to your actual Excel file path
input_file_path = 'chrome_checked.xlsx'
df = pd.read_excel(input_file_path)

# Adding columns for the check results
df['Has YAML in Workflows'] = False
df['Has Dependabot'] = False

# Iterate over each row in the DataFrame and update the check results
for index, row in df.iterrows():
    repo_url = row['URL']
    owner_repo = repo_url.replace("https://github.com/", "").split('/')
    if len(owner_repo) == 2:
        owner, repo = owner_repo
        has_yaml, has_dependabot = check_repository_files(owner, repo, github_token)
        df.at[index, 'Has YAML in Workflows'] = has_yaml
        df.at[index, 'Has Dependabot'] = has_dependabot

# Specify the output Excel file path and save the updated DataFrame
output_file_path = 'processed_repos_chrome.xlsx'
df.to_excel(output_file_path, index=False)

print("Process completed. Check the output Excel file for results.")

