### This will sync metadata for the MVP image set for the DSA HTAN image portal
import girder_client
import secrets as s
import sys, os,json

### Adding girder_utils path
sys.path.insert(0,"../loadBucketData")
import girder_utils as gu

gc = girder_client.GirderClient(apiUrl=s.apiUrl)
gc.authenticate(apiKey=s.dsaApiKey)

MVPCollectionId = '604a39fa8dfee73ac067d126'

#source/%s/items?type=folder" % ("604a544f8dfee73ac067d126"))
itemSet = gu.listChildItems(gc,"resource/%s/items?type=collection" % (MVPCollectionId))

with open("./imagesWithMetadata.v1.json","r") as fp:
	htanMeta = json.load(fp)


htanMetaToFile = { os.path.basename(m['Bucket_url']): m for m in htanMeta}


def createLargeImage(gc,itemId,force=True):
	### Hit the endpoint to create a largeImage, this defaults
	## To using the force option to transcode images
	#https://imaging.htan.dev/girder/api/v1/item/604ffde157d3801bcf839f97/tiles?force=true&notify=true&tileSize=256&quality=90
	gc.post("item/%s/tiles?force=%s" % (itemId,force))

needsLargeImage = 0
createLargeImages = False
addedMeta = 0
## I may not want to try and generate largeImages for every file
## and/or I may want to add additional logic to detect failed files


for i in itemSet:
	if 'largeImage' not in i:
		needsLargeImage+=1
		if createLargeImages: createLargeImage(gc,i['_id'])
	if 'htanMeta' not in i['meta']:
		if i['name'] in htanMetaToFile:
			gc.addMetadataToItem(i['_id'],{'htanMeta': htanMetaToFile[i['name']]})
			addedMeta +=1
print("Creating large image for %d images and added metadata to %d images" % (needsLargeImage,addedMeta))


