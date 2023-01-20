# U-fynd-Scrapping-Task

This repository contains a Booking.com hotel scraping task completed for a U:Fynd technical assessment. It includes both a static HTML parser and a live web scraper designed to extract hotel metadata and room information.

## Project Overview

- `Static/booking-scrape.py`: Parses a saved Booking.com HTML page and extracts hotel details into `Booking-Extracted-Data.json`.
- `LiveWeb/booking-scrape.py`: Uses Selenium + Chrome WebDriver to scrape hotel listings from Booking.com in real time and export the results to `Booking-Extracted-Data.json`.
- `Static/GivenData/`: Contains the downloaded sample Booking.com hotel page used for static parsing.
- `ApproachDiagram/`: Includes a diagram of the scraping approach.

## Repository Structure

- `LICENSE` - License file for the repository.
- `README.md` - Project documentation.
- `requirments.txt` - Python dependencies required to run the scraper.
- `ApproachDiagram/` - Architecture and workflow diagram.
- `LiveWeb/` - Live Selenium-based scraper and sample output data.
- `Static/` - Static HTML parser and sample scraped output.
- `Ufynd-Assignment-Report.pdf` and `Web Scraper Assignment.pdf` - Assignment reports.

## Dependencies

Install the required Python packages before running either scraper.

```powershell
pip install -r requirments.txt
```

The key dependencies are:

- `beautifulsoup4==4.12.2`
- `bs4==0.0.1`
- `lxml==4.9.2`
- `python-dotenv==0.21.1`
- `selenium==4.9.0`
- `webdriver-manager==3.8.6`

## Usage

### Static Scraper

The static scraper reads a saved Booking.com hotel HTML file and exports extracted hotel details.

1. Confirm the file path in `Static/booking-scrape.py`:
   - `Constants.FILE_PATH = './GivenData/task 1 - Kempinski Hotel Bristol Berlin, Germany - Booking.com.html'`
2. Run the scraper:

```powershell
cd Static
python booking-scrape.py
```

3. Output will be written to `Booking-Extracted-Data.json` in the current working directory.

### Live Web Scraper

The live web scraper uses Selenium to load Booking.com pages and extract data from multiple hotels.

1. Ensure Chrome is installed on your machine.
2. Run:

```powershell
cd LiveWeb
python booking-scrape.py
```

3. The scraper will navigate through hotel listings, extract details, and save them to `Booking-Extracted-Data.json`.

## Output

Both scrapers produce a JSON file named `Booking-Extracted-Data.json` with fields such as:

- `Hotel Name`
- `Address`
- `Stars`
- `Ratings`
- `Total Reviews`
- `Description`
- `Room Categories`
- `Alternative Options`

## Notes

- The live scraper requires a working internet connection and a Chrome browser installation.
- The static scraper can be adapted to other saved Booking.com pages by updating the file path constant.
- The project is intended for technical assessment purposes and demonstrates HTML parsing, XPath extraction, and Selenium usage.

## License

See `LICENSE` for license details.
