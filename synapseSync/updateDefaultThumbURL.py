# This will sync metadata for the MVP image set for the DSA HTAN image portal
import girder_utils as gu
import girder_client
import secrets as s
import sys, os, json, time, tqdm
import urllib.parse
# Adding girder_utils path
sys.path.insert(0, "../loadBucketData")

updateMetadata = False


## Connect to the girder instance -- the apiToken is in the secrets file
gc = girder_client.GirderClient(apiUrl=s.apiUrl)
gc.authenticate(apiKey=s.dsaApiKey)

MVPCollectionId = '604a39fa8dfee73ac067d126'

# source/%s/items?type=folder" % ("604a544f8dfee73ac067d126"))
itemSet = gu.listChildItems(
    gc, "resource/%s/items?type=collection" % (MVPCollectionId))


def createDefaultThumbUrl(itemInfo):
    # This will use a heuristic to set a spiffy thumbnail url for a mltichannel image
    simpleThumb = {'bands': [
        {'frame': 0, 'palette': ['#000000', '#0000ff'],
            'min': 'auto', 'max': 'auto'},
        {'frame': 1, 'palette': ['#000000', '#00ff00'], 'max': 'auto'},
        {'frame': 2, 'palette': ['#000000', '#ff0000'], 'max': 'auto'}]}
    return simpleThumb

def formatChannelData(internal_metadata):
    # Reformmating internal channel metadata for the omeSceneDescription tag
    # that the DSA uses for rendering scenes
    if 'frames' in internal_metadata or 'channelmap' in internal_metadata:
        imgChannelList = []

        for f in internal_metadata['frames']:
            if 'Name' in f:
                name = f['Name']
            else:
                name = f['Frame']

            fd = {'channel_name': f['Frame'],
                  'channel_number': f['Frame'],
                  'label': name,
                  'marker_name': name}
            imgChannelList.append(fd)

        return imgChannelList
    return None


## Some files do not have a channel map in their header and I have to grab this externally
## from the HTAN data model and/or CSV file
with open("./testData/channelMapInfo.json","r") as fp:
    htanChannelMapInfo = json.load(fp)


##if 'hist' in ioparams:
## Delete the histograms.. it's just irritating

channelMapData = {}

for c in htanChannelMapInfo:
    hdfID = c['HTAN_Data_File_ID']
    if hdfID not in channelMapData:
        channelMapData[hdfID] = {'origChannelInfo': [], 'channelmap': {}}
    channelMapData[hdfID]['origChannelInfo'].append(c)
    if c['LAYER']:
        channelMapData[hdfID]['channelmap'][c['MARKERNAME']] = int(c['LAYER'])

    # print(c['CHANNEL'],c['MARKERNAME'],c['LAYER'])
        
        ### Now seeing if the channelinfo is actually useful.. i.e. not an RGB image
        # print(c)
        # if c['LAYER']:
#       channelMapData[hdfID]['channelmap'].append({})
#    'MARKERNAME' and 'LAYER'  maps to channel_name   and channel_number goes to LAYER  to marker_name


itemData = []

hasThumbnailUrl = 0
hasGroupSets = 0
hasBoth = 0


def createThumbUrlFromDSASceneSet(dsaItem):
    # Given the dsaItem there should be a field in dsaItem.meta.DSAGroupSet ... take the longest one
    # print(dsaItem['meta'].keys())
    if 'DSAGroupSet' in dsaItem['meta']:
        DSAGroupSet = dsaItem['meta']['DSAGroupSet']
        # print(len(DSAGroupSet))

        styleInfo = {"bands": []}

        if len(DSAGroupSet) > 0:

            for c in DSAGroupSet[0]['channels']:
                # print(c)
                styleInfo['bands'].append({"min": c['min'],
                                           "max": c['max'],
                                           "palette": ["rgb(0,0,0)", c['color']],
                                           "frame": c["index"]})
        return(styleInfo)


# I need to also identify multiframe images that do not have a channel map that is useful i.e. just numbers

for i in tqdm.tqdm(itemSet):
    itemData.append(i)

    hasDefaultThumb = False
    hasCuratedSceneSet = False

    if 'thumbnailUrl' in i['meta']['ioparams']:
        hasThumbnailUrl += 1
        hasDefaultThumb = True
    if 'DSAGroupSet' in i['meta']:
        hasGroupSets += 1
        hasCuratedSceneSet = True
        # print(i['name'], i['meta']['htanMeta']['HTAN_Center'],
        #       i['meta']['htanMeta']['Imaging_Assay_Type'])
        # print(urllib.parse.unquote(i['meta']['ioparams']['thumbnailUrl']))

    ioparams = i['meta']['ioparams']

    if ('frameCount' in ioparams and ioparams['frameCount'] >= 3):
        # print(hasDefaultThumb, hasCuratedSceneSet,
        #       ioparams['frameCount'], i['name'])

        if hasCuratedSceneSet:
            # Going to update the defaultThumbURL because i
            sceneData = createThumbUrlFromDSASceneSet(i)
            thumbnailString = urllib.parse.quote_plus(json.dumps(sceneData))

            # Only update the metadata if theres a new scene defintion
            if ('thumbnailUrl' not in ioparams) or (ioparams['thumbnailUrl'] != thumbnailString):
                ioparams['thumbnailUrl'] = thumbnailString
                gc.addMetadataToItem(i['_id'], {'ioparams': ioparams})
        else:
            # Set the default thumb using the other funct
            simpleSceneData = createDefaultThumbUrl(i)
            thumbnailString = urllib.parse.quote_plus(
                json.dumps(simpleSceneData))
            if ('thumbnailUrl' not in ioparams) or (ioparams['thumbnailUrl'] != thumbnailString):
                ioparams['thumbnailUrl'] = thumbnailString
                gc.addMetadataToItem(i['_id'], {'ioparams': ioparams})
        # break

print("Images with a default thumbnail", hasThumbnailUrl,
      "and %d have Group Sets" % hasGroupSets)

for i in itemData:
    if 'channelmap' not in i['meta']['ioparams']:
        hdfID = i['meta']['htanMeta']['HTAN_Data_File_ID']
        if hdfID in channelMapData and len(channelMapData[hdfID]['channelmap']) > 0:
            ioparams = i['meta']['ioparams']
            ioparams['channelmap'] = channelMapData[hdfID]['channelmap']
            gc.addMetadataToItem(i['_id'],{'ioparams':ioparams})


    else:
        pass
        # print("Found channel map")
        # print(i['meta']['ioparams']['channelmap'], i['name'])
# Imaging_Assay_Type  HTAN_Center


# 		if 'omeSceneDescription' not in i['meta']:

