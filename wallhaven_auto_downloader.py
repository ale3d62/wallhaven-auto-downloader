import collections
from requests import get
from os import path
from math import ceil

username = "ale3d62"
collectionId = "1591884"
outDir = "G:\Mi unidad\Mis Archivos\Personal\Wallpapers"

#Downloads the wallpapers from the selected wallhaven collection
#**The collection has to be public for the script to work**

def downloadWallpapers():
    #get collection size
    apiResponse = get("https://wallhaven.cc/api/v1/collections/" + username)
    if("error" in apiResponse.json()):
        print("Error during the api request, check the username and the collection Id")
        return

    collectionSize = 0

    userCollections = apiResponse.json()['data']
    for collection in userCollections:
        if str(collection['id']) == collectionId:
            collectionSize = collection['count']

    #there is a maximum of 24 wallpapers per page
    nCollectionPages = ceil(collectionSize % 24)

    print("")

    #download wallpapers
    for currentPage in range(nCollectionPages):
        apiResponse = get("https://wallhaven.cc/api/v1/collections/" + username + "/" + collectionId + "?page=" + str(currentPage+1))

        if("error" in apiResponse.json()):
            print("Error during the api request, check the username and the collection Id")
            return

        collectionWalls = apiResponse.json()['data']
        currentWallIndex = 1
        

        for wall in collectionWalls:
            
            print("\033[FDownloading " + str(currentWallIndex + currentPage*24) + "/" + str(collectionSize))
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





downloadWallpapers()