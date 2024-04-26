import requests
import pandas as pd
from github import Github

from bs4 import BeautifulSoup

def convert_to_number(s):
    # Define a dictionary for suffix multipliers
    multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}

    # Check if the last character is a digit
    if s[-1].isdigit():
        return int(s)
    
    # Extract the numeric part and the suffix
    numeric_part, suffix = s[:-1], s[-1].lower()
    
    # Convert the numeric part to a float
    numeric_value = float(numeric_part)
    
    # Multiply the numeric value by the corresponding multiplier
    if suffix in multipliers:
        return int(numeric_value * multipliers[suffix])
    else:
        raise ValueError(f"Unknown suffix '{suffix}' in input.")

def get_star_count(repo_url):
    try:
        response = requests.get(repo_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the <a> element that contains the '/stargazers' in its href attribute
        # and is closest to the actual star count display
        star_element = soup.find('a', href=lambda href: href and 'stargazers' in href)
        
        # Assuming the star count is the next sibling or closely following the found element,
        # often the actual star count might be in a span or directly within the <a> tag but needs to be visible
        # so we look for the parent and then for the element that contains the star count if not directly found.
        if star_element:
            star_count_text = star_element.get_text(strip=True)
            if not star_count_text.isdigit():
                # If the direct text is not a digit, try finding a span or sibling that contains digits
                star_count_span = star_element.find_next_sibling('span')
                if star_count_span:
                    star_count_text = star_count_span.get_text(strip=True)
                
            # Convert the star count text to an integer
            star_count_text = star_count_text.split('star')[0].strip()
            star_count_text = convert_to_number(star_count_text)
            star_count = int(star_count_text)
            print(f"{repo_url} has {star_count} stars.")
            # star_count = int(star_count_text.replace(',', ''))
            return star_count
        else:
            print("Star element not found.")
            return None
    except Exception as e:
        print(f"Error getting star count for {repo_url}: {e}")
        return None


# Read the Excel file into a DataFrame
excel_file = 'Omega Top 10,000 Projects.xlsx' # Replace with your Excel file path
df = pd.read_excel(excel_file)

df = df.drop_duplicates(subset=['URL'])
# Authenticate to GitHub API with a personal access token
# g = Github('your_github_token') # Replace with your GitHub token

# Iterate over the 'URL' column and check for workflow files
# df['Has_Workflow'] = df['URL'].apply(has_workflow_yaml_files)

# Get the star count for each repository
df['Star_Count'] = df['URL'].apply(lambda x: get_star_count(x))

# Sort the DataFrame by star count in descending order
df_sorted = df.sort_values(by='Star_Count', ascending=False)

# Identify the top 50 starred repositories
top_50_starred = df_sorted.head(750)

# Save the results to new Excel files
# df.to_excel('repos_with_workflow_info.xlsx', index=False)
top_50_starred.to_excel('top_750_starred_repos.xlsx', index=False)
