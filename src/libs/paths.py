import os
from src.const.urls import file_extensions

def createOrConnectPath(path: str, root: str) -> str:
    # Get the hostname from the path, without the protocol
    usablePath = path.split("//")[1].split("/")
    builtPath = root

    for i in range(len(usablePath)):
        currentSegment = usablePath[i]
        absolutePrediction = os.path.join(builtPath, currentSegment)

        if currentSegment.split("?")[0].split("#")[0].split(".")[-1] in file_extensions:
            break

        if not os.path.exists(absolutePrediction):
            os.mkdir(absolutePrediction)

        builtPath = absolutePrediction
        i =+ 1

    return builtPath

def extractBaseUrl(url: str) -> str:
   return f"{url.split("//")[0]}//{url.split("//")[1].split("/")[0]}"