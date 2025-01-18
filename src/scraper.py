from src.libs.paths import createOrConnectPath, extractBaseUrl
from src.libs.parser import parseHtml
import os
import requests

class Scraper:
    def __init__(self, url, dir):
        self.url = url
        self.targetDir = dir
        self.queue = [url, f"{extractBaseUrl(url)}/"]
        self.scraped = []

    def scrape(self):
        itemToScrape = self.queue.pop(0)
        
        usablePath = createOrConnectPath(itemToScrape, self.targetDir)
        hostname = extractBaseUrl(itemToScrape)
        ogHostname = extractBaseUrl(self.url)

        if itemToScrape not in self.scraped:
            self.scraped.append(itemToScrape)

            if hostname != ogHostname:
                print("Hostname mismatch")
                print(ogHostname)
            else:
                print("Now scraping: " +  itemToScrape)
                fullFileName = itemToScrape.split("/")[-1].split("?")[0].split("#")[0]
                fileName = fullFileName.split(".")[0]
                if fileName == "":
                    fileName = "index"
                extension = fullFileName.split(".")[-1] if "." in fullFileName else "html"

                request = requests.get(itemToScrape)

                if request.status_code == 200:
                    if "text/html" in request.headers['content-type']:
                        [sanitsed, newQueue] = parseHtml(request.text, itemToScrape)

                        file = open(os.path.join(usablePath, fileName + "." + extension), "w+", encoding="utf-8")

                        file.write(sanitsed)

                        file.close()

                        self.queue += newQueue
                    else:
                        file = open(os.path.join(usablePath, fileName + "." + extension), "wb+")

                        file.write(request.content)

                        file.close()
                else:
                    print(f"Failed to fetch {request.status_code}: " + itemToScrape)



        if len(self.queue) > 0:
            self.scrape()
        else:
            print("Scraping complete")


