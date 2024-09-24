--eBay Web Scraper--

This project is a Python Flask web application that automates product searches on eBay.
It uses Selenium WebDriver to interact with the eBay website, retrieves product details,
and displays them through the Flask app. The details include the product title, price,
image, and a link to the product.

--Table of Contents
Project Overview
Features
How to Run
Code Structure
Function Details
Dependencies


--Project Overview

The eBay web scraper allows you to search for products on eBay automatically using 
a search term. It uses Selenium to interact with the website and BeautifulSoup to extract
product information from the page. The results are shown on a web interface created with Flask.

--Features

Perform automated product searches on eBay.
Retrieve product title, price, image, and link.
Display results in a formatted web page.
Handle multiple pages of search results without duplicates.
Support for headless mode in Selenium.

--How to Run

-Prerequisites
Ensure you have the following installed:

Python 3.x
Flask
Selenium
BeautifulSoup
A browser like Chrome with its appropriate driver (e.g., chromedriver).

-Running the Application

Clone this repository.
Install the necessary dependencies.
Update the path to the Chrome driver (driver_path) in the Python file with the correct path on your machine.
Run the Flask server.
Open your browser and go to http://127.0.0.1:5000/ to search for products.

--Code Structure

app.py: Contains the server and logic for scraping eBay using Selenium and BeautifulSoup.
Templates: HTML pages are generated directly in the Flask file using render_template_string.

--Function Details

 (process_page(driver, products, product_ids))

   Description: Extracts product details such as title, price, image, and link from the current page.
   It checks for duplicates using a set of product_ids.
   Returns: The number of new products found and the parsed page content.
   
 (find_last_page(soup))

   Description: Finds the last page of search results by analyzing the pagination section.
   Returns: The last page number.

 (index())

   Description: Main function for the home route. It handles the search, uses Selenium to find products on eBay, 
   and displays them through the web interface.
   Returns: The HTML page with the search results.
   
--Dependencies

   This project depends on:

   Flask: For creating the web interface and handling requests.
   Selenium: For interacting with eBay.
   BeautifulSoup: For parsing the HTML content.
   Chrome WebDriver: Needed to run Selenium with Chrome.

--License
This project is licensed under the MIT License. You are free to use and modify it as needed.
