import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def getFromLink(link):
    response = requests.get(link, headers=headers)
    newint = 58

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        laptop_data = []

        brand = "N/A"  # Set a default value
        processor="N/A"
        ram="N/A"
        ssd="N/A"
        hdd="N/A"
        weight="N/A"
        display="N/A"
        displagy="N/A"

        # Extract laptop information (modify as needed)s
        name = soup.find('h1', class_='bx-title').text
        price = soup.find('div', class_='item_current_price').text
        
       
        bx_detail = soup.find_all('dt', class_='bx_detail_chars_i_title')
        if bx_detail:
            details = soup.find_all('span', class_='glossary-term')
            for detail in details:
                glossary_term = detail.text.strip().lower()
                if glossary_term == 'производитель':
                    brand = detail.find_next('dd', class_='bx_detail_chars_i_field').text
                if glossary_term == 'процессор':
                    next_dd = detail.find_next('dd', class_='bx_detail_chars_i_field')
                    processor = next_dd.text if next_dd else "N/A"
                if glossary_term == 'объем оперативной памяти, гб':
                    next_dd = detail.find_next('dd', class_='bx_detail_chars_i_field')
                    ram = next_dd.text if next_dd else "N/A"
                if glossary_term == 'твердотельный накопитель':
                    next_dd = detail.find_next('dd', class_='bx_detail_chars_i_field')
                    ssd = next_dd.text if next_dd else "N/A"
                if glossary_term == 'жесткий диск':
                    next_dd = detail.find_next('dd', class_='bx_detail_chars_i_field')
                    hdd = next_dd.text if next_dd else "N/A"
                if glossary_term == 'вес, кг':
                    next_dd = detail.find_next('dd', class_='bx_detail_chars_i_field')
                    weight = next_dd.text if next_dd else "N/A"
                if glossary_term == 'вес, кг':
                    next_dd = detail.find_next('dd', class_='bx_detail_chars_i_field')
                    display = next_dd.text if next_dd else "N/A"     
        
       

        if name and price:
            laptop_data.append({
                'Name': name,
                'Price': price,
                'Brand': brand,
                'Processor':processor,
                'Ram':ram,
                'SSD':ssd,
                'HDD':hdd,
                'Weight':weight,
                'Display':display,

            })


        laptop_df = pd.DataFrame(laptop_data)

        return laptop_df

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        return None


# Example usage:
base_url = 'https://shop.kz/noutbuki/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
response_all = requests.get(base_url, headers=headers)

if response_all.status_code == 200:
    soup = BeautifulSoup(response_all.text, 'html.parser')
    catalog_list = soup.find('div', class_='bx_catalog_list_home')

    href_values = []

    if catalog_list:
        titles = catalog_list.find_all('div', class_='bx_catalog_item_title')

        for title in titles:
            a_tag = title.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href_values.append(a_tag['href'])
    all_data = pd.DataFrame()
   
    # Loop through the href values and scrape data from individual product listing pages
    for href in href_values:
        # Construct the complete URL using the base_url and href
        product_url = "https://shop.kz" + href
        scraped_data = getFromLink(product_url)
        if scraped_data is not None:
            print(scraped_data)
            all_data = pd.concat([all_data, scraped_data], ignore_index=True)

    # Save all scraped data to an XLSX file
    with open('laptop_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(all_data.columns)  # запись заголовков
        for row in all_data.values:
            writer.writerow(row)

else:
    print(f'Failed to retrieve the webpage. Status code: {response_all.status_code}')
