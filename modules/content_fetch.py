from scrapegraphai.graphs import SmartScraperGraph

def scrape_content(page, query, model):
    graph_config = {
        "llm": {
            "model": f"ollama/{model}",
            "temperature": 0,
            "format": "json",  # Ollama needs the format to be specified explicitly
            "base_url": "http://localhost:11434",  # set Ollama URL
        },
        "embeddings": {
            "model": "ollama/nomic-embed-text",
            "base_url": "http://localhost:11434",  # set Ollama URL
        }
    }

    smart_scraper_graph = SmartScraperGraph(
        prompt= f"{query}",
        # also accepts a string with the already downloaded HTML code
        source=f"{page}",
        config=graph_config
    )

    return smart_scraper_graph.run()

if __name__ == "__main__":
    
    model = "llama3.2"
    query = "Give me a small summary of the information provided in the page in 200 words or less."
    source = "https://summerofcode.withgoogle.com/"

    result = scrape_content(source,query,model)
    print(result['content'])
