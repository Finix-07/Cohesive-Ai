from .content_fetch import scrape_content
import json

def fetch_info(company_info, columns):
    def to_json(content, company_info):
    
        with open(f"C:\\Users\\anubh\\OneDrive\\Desktop\\Projects\\Cohesive-Ai\\data.json", "a") as file:
            json.dump({'Company': [company_info, content]}, file, indent=4)

    table_col = list(columns.keys())
    content = {}
    for col in table_col:
        content[col] = (scrape_content(company_info["value"], columns[col], "llama3.2"))
    
    to_json(content, company_info)

# convert dictionary to .json file

# sample example
if __name__ == '__main__':
    company_info = {'type': 'name', 'value': 'Cohesive AI'}
    columns = {'Name': 'h1', 'Description': 'p'}

    fetch_info(company_info, columns)


