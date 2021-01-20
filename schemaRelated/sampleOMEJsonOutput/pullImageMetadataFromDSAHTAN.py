### This will pull all of the imaging metadata for any items living in the DSA HTAN Instance

import girder_client
import secrets, os, json

apiURL = "https://imaging.htan.dev/girder/api/v1"

gc = girder_client.GirderClient(apiUrl=apiURL)
gc.authenticate(apiKey=secrets.apiToken)


## I am going to build a dictionary of every image item below the following path on the DSA HTAN instance
rootImageFolder = gc.get('resource/lookup?path=%s' % "/collection/SARDANA_S3_Sync/htan-tnp-sardana-hms-prerelease-phase-1-data")


# I want to dump all the metadata, internal metadata, and tile level metadata to assist with validation


imageMetadataDict = {}

for i in gc.listItem(rootImageFolder['_id']):
    if 'largeImage' in i:
        internalMetadata = gc.get('item/%s/tiles/internal_metadata' % i['_id'])
        imageMetadataDict[i['name']] = { 'internalMetadata': internalMetadata }


with open("sampleHTANImageMetadata.json","w") as fp:
    json.dump(imageMetadataDict,fp,indent=2)
