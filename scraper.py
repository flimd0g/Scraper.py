import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the page containing PDF links
url = 'https://www.datasheetarchive.com/?q=plva'
response = requests.get(url)
if response.status_code == 200:
    page_content = response.text
else:
    raise Exception('Failed to load page')

# Parse the HTML and extract PDF links
soup = BeautifulSoup(page_content, 'html.parser')
pdf_links = []

for a_tag in soup.find_all('a', class_='secondary-button is-small is-buy-now'):
    href = a_tag.get('href')
    if 'pdf' in a_tag.text.lower():
        pdf_url = urljoin(url, href)
        pdf_links.append(pdf_url)

# Specify the directory to save the PDF files
save_directory = r'C:\Users\User\Documents\Python\Datasheets'

# Ensure the save directory exists
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Download the PDF files
for pdf_url in pdf_links:
    pdf_response = requests.get(pdf_url)
    if pdf_response.status_code == 200:
        filename = os.path.join(save_directory, pdf_url.split('=')[1] + '.pdf')
        with open(filename, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f'Successfully downloaded {filename}')
    else:
        print(f'Failed to download PDF from {pdf_url}')
