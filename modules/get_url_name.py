from googlesearch import search
from urllib.parse import urlparse

def get_url(name):
    # Perform a Google search and get the first result
    search_results = list(search(name, num_results=5, lang="en"))
    if not search_results:
        return "No search results found."
    
    # If no relevant URL is found, return the first result as a fallback
    return search_results[0]

def get_company_name(url):
    # Parse the URL to extract the domain
    parsed_url = urlparse(url)
    
    # Get the domain (e.g., cohesive.ai)
    domain = parsed_url.netloc
    
    # Remove "www." if present
    if domain.startswith("www."):
        domain = domain[4:]
        
    # Extract company name (before the first dot)
    company_name = domain.split('.')[0]
    
    # Capitalize for better formatting
    return company_name.capitalize()

# Example usage


if __name__ == '__main__':
    name = input("Enter the name of the company: ").strip()
    url = get_url(name)
    print(f"The URL of the company '{name}' is: {url}")
    print(get_company_name(url))  # Output: "Cohesive"

