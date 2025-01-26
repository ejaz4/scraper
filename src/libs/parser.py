from bs4 import BeautifulSoup
from src.libs.paths import extractBaseUrl


def handleLink(url: str, currentPath: list, hostname: str, myPath: list) -> str:
    scriptUrl = url
    mode = "absolute"

    if scriptUrl is None:
            return None

    if scriptUrl.startswith(hostname):
        mode = "full"
    elif scriptUrl.startswith("/"):
        mode = "absolute"
    elif scriptUrl.startswith("http"):
        mode = "retain"
    else: 
        mode = "relative"

    if mode == "full":
        scriptUrl = scriptUrl.split(hostname)[1]

    if mode == "relative":
        virtualPath = myPath[:]

        # Pop end if it's a file
        if "." in virtualPath[-1]:
            virtualPath.pop(-1)

        for seg in scriptUrl.split("/"):
            if seg == "..":
                virtualPath.pop(-1)
            else:
                virtualPath.append(seg)
        
        scriptUrl = "/" + "/".join(virtualPath)
    
    return scriptUrl

def parseHtml(html: str, itemToScrape: str):
    soup = BeautifulSoup(html, "html.parser")
    hostname = f"{itemToScrape.split("//")[0]}//{itemToScrape.split("//")[1].split("/")[0]}"

    myPath = itemToScrape.split("//")[1].split("/")

    myPath.pop(0)


    enqueue = []
    
    srcTags = soup.find_all(["script", "img", "image"])

    for tag in srcTags:
        if "src" not in tag.attrs:
            continue

        scriptUrl = tag["src"]
        
        if scriptUrl.startswith("data"):
            continue
        
        if scriptUrl.startswith("mailto"):
            continue

        parsedUrl = handleLink(scriptUrl, myPath, hostname, myPath)

        if parsedUrl not in enqueue:
            if not parsedUrl.startswith("http"):
                enqueue.append(hostname +  parsedUrl)
            else:
                enqueue.append(parsedUrl)

        tag["src"] = parsedUrl

    hrefTags = soup.find_all(["a", "link"])

    for tag in hrefTags:
        if "href" not in tag.attrs:
            continue

        hrefUrl = tag["href"]
        
        if hrefUrl.startswith("data"):
            continue
        
        if hrefUrl.startswith("mailto"):
            continue

        parsedUrl = handleLink(hrefUrl, myPath, hostname, myPath)

        if parsedUrl not in enqueue:
            if not parsedUrl.startswith("http"):
                enqueue.append(hostname +  parsedUrl)
            else:
                enqueue.append(parsedUrl)
        tag["href"] = parsedUrl

    return [str(soup), enqueue]
        
        

            
