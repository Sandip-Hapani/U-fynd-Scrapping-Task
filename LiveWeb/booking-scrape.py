# To get Javascript rendered pages
#------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from time import sleep
from lxml import etree
import json
# -----------------------------------------


# Class for all kind of global constants
class Constants:

    OFFSET = 0 # Flag variable for the listed hotels on page

    # URL for listed all hotels in desired area.
    URL = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAsoO0IWa2VtcGluc2tpYnJpc3RvbGJlcmxpbkgJWARoO4gBAZgBCbgBBMgBBNgBAegBAfgBC6gCA9gCAw&sid=d231c888cb3d2d2ebe4e3904a4b41541&district=5846&offset='

    SITE = 'https://www.booking.com' # Base address of target site

# To generate Web Driver - Which works as client browser
def create_driver():

    # Creating a chrome driver
    chrome_options = webdriver.ChromeOptions()

    # Chrome options for better experience and low load on memory
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    return driver

# Collect all listed hotels links from the desired area
def all_listed_hotels():

    all_hotels = [] # List for all listed hotels
    driver = create_driver() # Creating Web driver
    driver.get(Constants.URL)
    pages = int(driver.find_element(By.XPATH, '//*[@id="search_results_table"]//ol/li[last()]/button').text)

    for counter in range(1, pages+1):
        driver.get(Constants.URL + str(Constants.OFFSET))
        sleep(1.5) # Time for processing web page in browser (Depends on internet speed)
        hotel_links = driver.find_elements(By.XPATH, '//*[@data-testid="property-card"]//a[@data-testid="title-link"]')
        for hotel in hotel_links: all_hotels.append(hotel.get_attribute('href'))
        Constants.OFFSET += 25

    Constants.OFFSET = 0
        
    return (driver, all_hotels)

# For the Data Extraction form the web pages
def data_extraction():

    driver, all_hotels = all_listed_hotels()
    final_data = []

    for hotel in all_hotels:

        # Iterating all listed hotels link step by step
        driver.get(hotel) 
        sleep(1.5)

        # Parsing HTML response into the BeutifulSoup Object
        soup = BeautifulSoup(driver.page_source, 'lxml')
        x_soup = etree.HTML(str(soup)) # For Xpath referencing

        # Scraping all desired fields from the individual page
        try:
            alt_options = {}
            hotel_name = x_soup.xpath('//*[@id="hp_hotel_name"]//h2')[0].text.strip()
            address = x_soup.xpath('//*[@id="showMap2"]/span[1]')[0].text.strip()
            stars = len(x_soup.xpath('//*[@data-testid="rating-stars"]//span'))
            review_points = x_soup.xpath('//a[@rel="reviews"]//div[starts-with(@aria-label,"Scored")]')[0].text.strip()
            total_reviews = x_soup.xpath('//a[@rel="reviews"]//div[contains(text(),"review")]')[0].text.strip()
            description = "\n\n".join([ i.text.strip() for i in x_soup.xpath('//div[@class="hp_desc_main_content"]//*[text()]')[:-1] ]).strip()
            room_categories = [ i.text.strip() for i in x_soup.xpath('//*[@id="maxotelRoomArea"]/section/div//a//span') ]
            name = x_soup.xpath('//ul[@data-bui-ref="carousel-container"]/li//h3')
            link = x_soup.xpath('//ul[@data-bui-ref="carousel-container"]/li//a')
            for i in range(len(name)): 
                alt_options[name[i].text.strip()] = Constants.SITE + str(link[i].get('href'))

            tmp = {
                "Hotel Name": hotel_name,
                "Address": address,
                "Stars": stars,
                "Ratings": review_points,
                "Total Reviews": total_reviews,
                "Description": description,
                "Room Categories": room_categories,
                "Alternative Options": alt_options 
            }
            final_data.append(tmp)
        except:
            pass


        # break # For trial based
    driver.close()

    return final_data

# Exporting Extracted data
def data_build(data):

    # Jsonifying the extracted data
    data_json = json.dumps(data, indent=4, ensure_ascii=False)

    # Writing into a json file
    try:
        with open("Booking-Extracted-Data.json", 'w', encoding='utf-8') as f_out:
            f_out.write(data_json)
    except Exception as e:
        print("Exception occured: " + str(e))
        return

# Main Function
if __name__ == '__main__':

    ext_data = data_extraction() # Required Data Extraction from the HTML Source
    data_build(ext_data) # Exporting Data into a file.
    print("Checkout the present working directory, you'll get a Extracted-Data json file.")
