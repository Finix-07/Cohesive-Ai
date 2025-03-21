from .content_fetch import scrape_content
import json
import os

def fetch_info(company_info, columns):
    def to_json(content, company_info):
        # Define the file path
        file_path = "C:\\Users\\anubh\\OneDrive\\Desktop\\Projects\\Cohesive-Ai\\website\\data.json"

        # Create a new entry
        new_entry = {
            "company": {
                "name": company_info["key"],
                "url": f"{company_info['value'].replace(' ', '').lower()}"
            },
            "columns": list(columns.keys()),
            "data": content
        }

        # Check if the file exists and is non-empty
        file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

        # Write the new entry without outer brackets
        with open(file_path, "w") as file:
            if file_exists:
                file.write(",\n")
            json.dump(new_entry, file, indent=4)

    # Extract column names and content
    content = {col: {"content": scrape_content(company_info["value"], columns[col], "llama3.2")} for col in columns}
    # content = {
    #     "Name": {"content": "Cohesive AI"},
    #     "Description": {"content": "An advanced AI platform for content automation."}
    # }


    # Store in updated JSON format (without outer square brackets)
    to_json(content, company_info)

# Sample example
if __name__ == '__main__':
    company_info = {'key': 'Cohesive AI', 'value': 'https://www.cohesive.ai'}
    columns = {'Name': 'h1', 'Description': 'p'}

    fetch_info(company_info, columns)
