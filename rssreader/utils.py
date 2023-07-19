import re

def parse_content(content):
    # Extract the description
    description_pattern = r'(.*?)(?=<b>(Hourly Range|Budget|Posted On))'
    description_match = re.search(description_pattern, content)
    description = description_match.group(1) if description_match else None

    # Check for Hourly Range, Budget, or neither
    if 'Hourly Range' in content:
        range_pattern = r'Hourly Range</b>: (.*?)\n'
        range_match = re.search(range_pattern, content)
        pay_range = range_match.group(1) if range_match else None
        job_type = 'Hourly'
    elif 'Budget' in content:
        range_pattern = r'Budget</b>: (.*?)\n'
        range_match = re.search(range_pattern, content)
        pay_range = range_match.group(1) if range_match else None
        job_type = 'Fixed'
    else:
        pay_range = None
        job_type = 'Hourly'

    # Extract the Category
    category_pattern = r'Category</b>: (.*?)<br /><b>Skills</b>'
    category_match = re.search(category_pattern, content)
    category = category_match.group(1) if category_match else None

    # Extract the Skills
    skills_pattern = r'Skills</b>:(.*?)\n'
    skills_match = re.search(skills_pattern, content)
    skills = skills_match.group(1) if skills_match else None

    # Extract the Country
    country_pattern = r'Country</b>: (.*?)\n'
    country_match = re.search(country_pattern, content)
    country = country_match.group(1) if country_match else None

    return description, pay_range, job_type, category, skills, country
