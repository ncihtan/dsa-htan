import girder_client
from dsaSecrets import dsaApiKey
import girder_utils as gu
import tqdm

## Connect to the girder Client
gc = girder_client.GirderClient(apiUrl="https://imaging.htan.dev/girder/api/v1")
gc.authenticate(apiKey=dsaApiKey)

## The DCC buckets are currently all folders in the DCCBucketSync collection on the HTAN DSA instance
dccFolderList = gc.listFolder('5fa99a0051de21dd08ca7dfa',parentFolderType='collection')

## I am scanning these extensions as they are very likely image files
imgExtensions = ['.tif','.svs','.ndpi','.tiff']
dccImageStats = {}

def listChildItems(gc, path, params=None, limit=None, offset=None,pageSize=1000):
    """
    This is a generator that will yield records using the given path and
    params until exhausted. Paging of the records is done internally, but
    can be overriden by manually passing a ``limit`` value to select only
    a single page. Passing an ``offset`` will work in both single-page and
    exhaustive modes.
    """
    params = dict(params or {})
    params['offset'] = offset or 0
    params['limit'] = pageSize
    while True:
        recordSet = gc.get(path, params)
        for r in recordSet:
            yield(r)
        n = len(recordSet)
 
        if limit or n < params['limit']:
            # Either a single slice was requested, or this is the last page
            break
        params['offset'] += pageSize




allImageFileList = []


for dccId in dccFolderList:
	print("Analyize %s " % dccId['name'])
	itemSet = listChildItems(gc,"resource/%s/items?type=folder" % (dccId['_id']))

	largeImageCount = 0
	totalItems = 0
	probablyImageFile = 0

	for i in tqdm.tqdm(itemSet):
		totalItems+=1
		if 'largeImage' in i:
			largeImageCount +=1
		likelyImgFile = any([ext in i['name'] for ext in imgExtensions])
		if likelyImgFile:
			probablyImageFile +=1
			allImageFileList.append(i)
	dccImageStats[dccId['name']] = { "largeImageCount": largeImageCount, "totalItems": totalItems, "probablyImageFile": probablyImageFile}

	print("\t",largeImageCount,totalItems,probablyImageFile)
