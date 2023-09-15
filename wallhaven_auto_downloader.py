from requests import get
from os import path

username = "ale3d62"
collectionId = "1591884"
outDir = "G:\Mi unidad\Mis Archivos\Personal\Wallpapers"

#Downloads the wallpapers from the selected wallhaven collection
#**The collection has to be public for the script to work**


apiResponse = get("https://wallhaven.cc/api/v1/collections/" + username + "/" + collectionId)

if("error" in apiResponse.json()):
    print("Error during the api request, check the username and the collection Id")
    exit()

collectionWalls = apiResponse.json()['data']
currentWallIndex = 1
collectionSize = len(collectionWalls)
print("")

for wall in collectionWalls:
    
    print("\033[FDownloading " + str(currentWallIndex) + "/" + str(collectionSize))
    currentWallIndex += 1
    
    #Obtain the wall name and extension
    wallId = wall["id"]
    wallUrl = wall["path"]
    wallFileExtension = wallUrl.split('.')[-1]
    
    #Check if wall is already downloaded
    if(not path.isfile(outDir + "\\wallhaven-" + wallId + "." + wallFileExtension)):
        #Download the wall
        wallContent = get(wallUrl).content
        with open(outDir + "\\wallhaven-" + wallId + "." + wallFileExtension, 'wb') as f:
            f.write(wallContent)
            f.close()

print("\033[FWallpapers successfully downloaded!")
