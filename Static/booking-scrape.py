from bs4 import BeautifulSoup 
from lxml import etree
import json

# Class for all kind of global constants
class Constants:
    # Change the file path form here.
    FILE_PATH = './GivenData/task 1 - Kempinski Hotel Bristol Berlin, Germany - Booking.com.html'

# For the HTML response from web pages
def html_source(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            web_data = f.read()
            return web_data

    except Exception as e:
        print("File not Found, Exception occured: " + str(e))
        return

# For the Data Extraction form the web pages
def data_extraction(web_data):

    # Parsing HTML response into the BeutifulSoup Object
    soup = BeautifulSoup(web_data, 'lxml')
    x_soup = etree.HTML(str(soup)) # For Xpath referencing

    hotel_name = x_soup.xpath('//*[@id="hp_hotel_name"]')[0].text.strip()
    address = x_soup.xpath('//*[@id="hp_address_subtitle"]')[0].text.strip()
    stars = len(x_soup.xpath('//*[@data-testid="rating-stars"]'))
    review_points = x_soup.xpath('//*[@id="js--hp-gallery-scorecard"]/a/span[2]/span[1]')[0].text.strip()
    total_reviews = x_soup.xpath('//*[@id="js--hp-gallery-scorecard"]/span/strong')[0].text.strip()
    description = "\n\n".join([ i.text.strip() for i in x_soup.xpath('//*[@id="summary"]/p') ])
    room_categories = [ i.text.strip() for i in x_soup.xpath('//*[@id="maxotel_rooms"]/tbody/tr/td[@class="ftd"]') ]

    alt_options = {}
    for i in x_soup.xpath('//*[@id="althotelsRow"]//a[@class="althotel_link"]'):
        alt_options[i.text.strip()] = i.get('href')

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

    return tmp

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

if __name__ == '__main__':

    web_data = html_source(file_path=Constants.FILE_PATH) # For getting HTML Source 
    ext_data = data_extraction(web_data=web_data) # Required Data Extraction from the HTML Source
    data_build(ext_data) # Exporting Data into a file.

    print("Checkout the present working directory, you'll get a Extracted-Data json file.")
