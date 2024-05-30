from requests import get
from os import path, makedirs
from math import ceil
from PIL import Image
import PIL
import platform


#Detect if running on windows or linux
runningOs = platform.system()

#Set path separator
if(runningOs == "Windows"):
	pSlash = "\\"
else:
	pSlash = "/"


#PAREMETERS
#------------------------------------------------------------

username = "ale3d62"
collections = [
    {
        "collectionId": "1591884",
        "collectionName": "Default"
    },
    {
        "collectionId": "1610358",
        "collectionName": "browser"
    }
]

if(runningOs == "Linux"):
	outDir = "/home/ale/Wallpapers"
else:
	outDir = "G:\Mi unidad\Mis Archivos\Personal\Wallpapers"

thumbWidth = 180

#------------------------------------------------------------



#Downloads the wallpapers from the selected wallhaven collection
#**The collection has to be public for the script to work**

def downloadWallpapers(collection):

    collectionId = collection['collectionId']
    collectionName = collection['collectionName']


    #get collection size
    try:
        apiResponse = get("https://wallhaven.cc/api/v1/collections/" + username)
        if("error" in apiResponse.json()):
            print("Error during the api request, check the username and the collection Id")
            return
    except:
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
            realWallIndex = currentWallIndex + currentPage*24
            print("\033[FDownloading " + str(realWallIndex) + "/" + str(collectionSize) + "[" + str(int(realWallIndex/collectionSize*100)) + "%]")
            currentWallIndex += 1
            
            #Obtain the wall name and extension
            wallId = wall["id"]
            wallUrl = wall["path"]
            wallFileExtension = wallUrl.split('.')[-1]

            wallFullPath = outDir + pSlash + collectionName + pSlash + "wallhaven-" + wallId + "." + wallFileExtension

            #If collection directory doesnt exists, create it
            collectionPath = outDir + pSlash + collectionName

            if(not path.isdir(collectionPath)):
                makedirs(collectionPath)

            
            #Check if wall is already downloaded
            if(not path.isfile(wallFullPath)):
                #Download the wall
                wallContent = get(wallUrl).content
                with open(wallFullPath, 'wb') as f:
                    f.write(wallContent)
                    f.close()
                
            #If the wall is for the browser, make a thumb
            if(collectionName == "browser"):

                if(not path.isdir(outDir + pSlash + "browser" + pSlash + "thumbs")):
                    makedirs(outDir + pSlash + "browser" + pSlash + "thumbs")

                wallThumbPath = outDir + pSlash + collectionName + pSlash + "thumbs" + pSlash + "wallhaven-" + wallId + "." + wallFileExtension

                if(not path.isfile(wallThumbPath)):
                    image = PIL.Image.open(wallFullPath)
                    widthPercent = (thumbWidth / float(image.size[0]))
                    thumbHeight = int((float(image.size[1]) * float(widthPercent)))
                    image = image.resize((thumbWidth, thumbHeight), PIL.Image.LANCZOS)
                    image.save(wallThumbPath)


    print("\033[FWallpapers successfully downloaded!")




for collection in collections:
    print("--"+collection['collectionName']+"--")
    downloadWallpapers(collection)
    print("")
