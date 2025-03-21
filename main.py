# import the libraries

from modules.content_fetch import scrape_content
from modules.info_fetch import fetch_info
from modules.get_url_name import get_url, get_company_name
from modules.server import start_server

# main working code according to the flowchart
user = 'Finix'
print(f"Hello, {user}")

# Ask the user for either the company name or URL of the company
choice = input("Would you like to enter the company name or the URL of the company? (type 'name' or 'url'): ").strip().lower()

if choice == 'name':
    company_name = input("Enter the company name: ").strip()
    company_url = get_url(company_name)

elif choice == 'url':
    company_url = input("Enter the company URL: ").strip()
    company_name = get_company_name(company_url)

else:
    print("Invalid choice. Please restart the program.")
    exit()
if company_url == "No search results found." or company_name in ["", " "]:
    print("No search results found. Please restart the program.")
    exit()

company_info = {'key': company_name, 'value': company_url}

print(f"You have entered the company {company_info['key']}: {company_info['value']}")

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

start_server()

