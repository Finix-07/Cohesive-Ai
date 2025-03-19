# import the libraries

from modules.content_fetch import scrape_content
from modules.info_fetch import fetch_info

# main working code according to the flowchart
user = 'Finix'
print(f"Hello, {user}")

# Ask the user for either the company name or URL of the company
choice = input("Would you like to enter the company name or the URL of the company? (type 'name' or 'url'): ").strip().lower()

if choice == 'name':
    company_name = input("Enter the company name: ").strip()
    company_info = {'type': 'name', 'value': company_name}

elif choice == 'url':
    company_url = input("Enter the company URL: ").strip()
    company_info = {'type': 'url', 'value': company_url}

else:
    print("Invalid choice. Please restart the program.")
    exit()

print(f"You have entered the company {company_info['type']}: {company_info['value']}")

# Request user to input column names and their associated formats
columns = {}
while True:
    column_name = input("Enter column name (or type 'done' to finish): ")
    if column_name.lower() == 'done':
        break
    column_format = input(f"Enter the format/description for column '{column_name}': ")
    columns[column_name] = column_format

print("You have entered the following columns and formats:")
print("Column\t\tFormat")
print("------\t\t------")
for col, fmt in columns.items():
    print(f"{col}\t\t{fmt}")

# scrape content from the website url for each column with a structured prompt given by the user
fetch_info(company_info, columns)
