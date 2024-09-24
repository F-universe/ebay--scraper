from flask import Flask, render_template_string, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# Set the path for the browser driver (in this case for Chrome)
driver_path = r'C:\Users\fabio\OneDrive\Desktop\webdriver\chromedriver.exe'

def process_page(driver, products, product_ids):
    # Get the page content
    page_content = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Check for the presence of the class "srp-results srp-list clearfix"
    results_section = soup.find(class_="srp-results srp-list clearfix")

    if results_section:
        # Find all items with the class "s-item__wrapper clearfix"
        items = results_section.find_all(class_="s-item__wrapper clearfix")

        for item in items:
            title = item.find(class_="s-item__title").get_text(strip=True)
            price = item.find(class_="s-item__price").get_text(strip=True)
            link = item.find('a', class_="s-item__link")['href']
            product_id = link.split("/")[-1]

            # Avoid adding duplicates by checking the product ID
            if product_id not in product_ids:
                product_ids.add(product_id)

                # Find the image element and get the image URL that starts with "https://i.ebayimg.com"
                img_tag = item.find('img', src=True)
                image = img_tag['src'] if img_tag and img_tag['src'].startswith('https://i.ebayimg.com') else None

                products.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'image': image
                })

    return len(products), soup

def find_last_page(soup):
    # Find the last available page
    pagination = soup.find(class_="pagination__items")
    if pagination:
        pages = pagination.find_all('a')
        last_page = max([int(page.get_text()) for page in pages if page.get_text().isdigit()])
        return last_page
    return 1

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    products = []
    product_ids = set()  # Used to track already counted product IDs
    total_products = 0
    page_number = 1

    if request.method == 'POST':
        search_term = request.form['search_term']

        # Set Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run the browser in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering

        # Initialize the service for ChromeDriver with headless options
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Go to the eBay homepage
            driver.get('https://www.ebay.com')

            # Find the search bar
            search_box = driver.find_element('name', '_nkw')

            # Enter the search term
            search_box.send_keys(search_term)

            # Press the enter button to perform the search
            search_box.send_keys(Keys.RETURN)

            # Wait for the page to load
            time.sleep(5)

            # Process the first page and determine the number of the last page
            num_products, soup = process_page(driver, products, product_ids)
            total_products += num_products
            last_page = find_last_page(soup)

            # Continue processing all subsequent pages
            while page_number < last_page:
                page_number += 1
                next_page_url = f'https://www.ebay.it/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&_pgn={page_number}'
                driver.get(next_page_url)

                # Wait for the page to load
                time.sleep(5)

                # Process the current page
                num_products, _ = process_page(driver, products, product_ids)
                total_products += num_products

            # Final message with the total number of products found
            message = f"Total number of items found: {len(product_ids)}"
        
        finally:
            # Close the browser
            driver.quit()

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>eBay Search</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 50px;
                background-color: #f4f4f4;
            }
            h1 {
                color: #333;
            }
            form {
                margin-bottom: 20px;
            }
            input[type="text"] {
                width: 300px;
                padding: 10px;
                margin-right: 10px;
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #28a745;
                color: white;
                border: none;
                cursor: pointer;
            }
            .message {
                margin-top: 20px;
                font-size: 18px;
                color: #333;
            }
            .products {
                margin-top: 20px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .product {
                flex: 0 0 calc(20% - 10px); /* Five products per row */
                box-sizing: border-box;
                border: 1px solid #ccc;
                background-color: #fff;
                padding: 10px;
                text-align: center;
            }
            .product img {
                max-width: 100%;
                height: auto;
            }
            .product h2 {
                font-size: 16px;
                margin: 10px 0;
            }
            .product p {
                margin: 5px 0;
                font-size: 14px;
                color: #555;
            }
            .product a {
                text-decoration: none;
                color: #0073bb;
            }
            .product a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>eBay Search</h1>
        <form method="POST">
            <input type="text" name="search_term" placeholder="Enter the product to search">
            <input type="submit" value="Search">
        </form>
        <div class="message">{{ message }}</div>
        <div class="products">
            {% for product in products %}
            <div class="product">
                {% if product.image %}
                <img src="{{ product.image }}" alt="{{ product.title }}">
                {% endif %}
                <h2>{{ product.title }}</h2>
                <p>{{ product.price }}</p>
                <a href="{{ product.link }}" target="_blank">View on eBay</a>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    ''', message=message, products=products)

if __name__ == '__main__':
    app.run(debug=True)
