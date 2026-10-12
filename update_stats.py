import scholarly
from scholarly import ProxyGenerator
import re

# Your Google Scholar Author ID
AUTHOR_ID = 'yMBfKlQAAAAJ'
HTML_FILE = 'index.html'

print("Fetching data from Google Scholar...")

try:
    # Setup a free proxy to avoid blocking
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)
    
    # Search for the author and fill the profile with indices
    search_query = scholarly.search_author_id(AUTHOR_ID)
    author = scholarly.fill(search_query, sections=['indices'])
    
    citations = author['citedby']
    h_index = author['hindex']
    
    print(f"Found: Citations = {citations}, h-index = {h_index}")

    # Read the current HTML file
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the numbers between the markers
    content = re.sub(r'<!-- CITATIONS_START -->.*?<!-- CITATIONS_END -->', 
                     f'<!-- CITATIONS_START -->{citations}<!-- CITATIONS_END -->', 
                     content)
    
    content = re.sub(r'<!-- HINDEX_START -->.*?<!-- HINDEX_END -->', 
                     f'<!-- HINDEX_START -->{h_index}<!-- HINDEX_END -->', 
                     content)

    # Write the updated HTML back to the file
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated index.html!")

except Exception as e:
    # If Google blocks the bot, we exit gracefully so the website doesn't break
    print(f"Failed to fetch data (Google Scholar blocked the request): {e}")
    print("Keeping existing numbers.")
    # Exit with 0 so GitHub doesn't mark it as a failure
    exit(0)
