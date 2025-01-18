from src.scraper import Scraper
import os
# This is the file where you should perform your scraping


def main():
    url = "https://stella.hs.vc/en/index-d.html"
    dir = os.path.join(os.getcwd(), "output")
    print(dir)
    scraper = Scraper(url, dir)
    scraper.scrape()

main()