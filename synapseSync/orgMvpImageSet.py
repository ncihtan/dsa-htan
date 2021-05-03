### This will sync metadata for the MVP image set for the DSA HTAN image portal
import girder_client
import secrets as s
import sys, os,json
from collections import Counter

### Adding girder_utils path
sys.path.insert(0,"../loadBucketData")
import girder_utils as gu

gc = girder_client.GirderClient(apiUrl=s.apiUrl)
gc.authenticate(apiKey=s.dsaApiKey)

MVPCollectionId = '604a39fa8dfee73ac067d126'

#source/%s/items?type=folder" % ("604a544f8dfee73ac067d126"))
itemSet = gu.listChildItems(gc,"resource/%s/items?type=collection" % (MVPCollectionId))


itemList = list(itemSet)


## HTAN_Center is the prettier version , CENTER has the HTAN_ in it 

## For now will organize the MVP data by Center, Modality and then Subject ID?

orgKeys = [ 'Center',  'File_Format',  'HTAN_Center', 'HTAN_Participant_ID',  'Imaging_Assay_Type', 'Primary_Diagnosis',  'Tissue_or_Organ_of_Origin']


for o in orgKeys:
	print(o)
	keySet = [x['meta']['htanMeta'][o] for x in itemList]
	print(Counter(keySet))
## I may not want to try and generate largeImages for every file
## and/or I may want to add additional logic to detect failed files

CenterNames = []


HTAN_CenterNames = set([x['meta']['htanMeta']['HTAN_Center'] for x in itemList])

Imaging_Assay_Type = set([x['meta']['htanMeta']['Imaging_Assay_Type'] for x in itemList])

byAssayType = '6053934dea6bf85de36a7b0c'


mvpCollectionId = '604a39fa8dfee73ac067d126'


for assayName in Imaging_Assay_Type:

	params = { "parentType": "folder",
			"parentId": byAssayType,
			   "reuseExisting": True,
				"name": assayName,
			"description": "Virtual Folder by assay Type for %s " % assayName,
			"isVirtual": True,
			"virtualItemsQuery": json.dumps({"meta.htanMeta.Imaging_Assay_Type": assayName})}

	print(params)
	gc.post("folder",parameters=params)
