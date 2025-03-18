# import the libraries

from modules.content_fetch import scrape_content


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

# get html content of the company
summary = scrape_content(company_info, "200 words summary of the information in page", "llama3.2")

print(summary)

