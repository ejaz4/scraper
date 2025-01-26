from src.scraper import Scraper
import os
# This is the file where you should perform your scraping


def main():
    url = "https://intranet.ecs.westminster.ac.uk/modules/4COSC011W/examples"
    dir = os.path.join(os.getcwd(), "output")
    print(dir)
    scraper = Scraper(url, dir)

    while len(scraper.queue) > 0:
        scraper.scrape()

main()