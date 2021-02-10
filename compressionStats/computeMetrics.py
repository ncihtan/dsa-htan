import pymongo
import json
import tifftools 

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

c = pymongo.MongoClient()
stats ={ }

docsFound = 0

compressData = []

## top level keys for this database are filename, fileSize,  fullFilePath, recType and recompressionInfo

#for r in c['htanAnalytics']['compressionStats'].find():
for r in c['dsaCompressionStats']['tiffData'].find():
    #print(r) 
#    print(r['executionTime'],r['compressedFileSize'],r['compressionMethod'],r['origFileSize'],r['compressedFileSize']/r['origFileSize']*100)
    ci = {}
    tiffTag = json.loads(r['recompressionInfo']['ifds'][0]['tags']['270']['data'])
    
    lic = tiffTag['large_image_converter']

    if 'conversion_stats' not in lic:
        print("Missing conversion stats for %s" % r['filename'])
    else:

        ci['conversion_stats'] = lic['conversion_stats']
        ci['frames'] = lic['frames']
        ci['compressionArguments'] =  lic['arguments']
        ci['filename'] = r['filename']
        ci['fileSize'] = r['fileSize']
        ci['recType'] = r['recType']
#    ci['tileSize'] = lic['arguments']['tileSize']
    print(ci)
#    r['compressionRate'] = r['compressedFileSize']/r['origFileSize']*100

#    print('{executionTime:0.2f};{compressionMethod};{compressionRate:0.2f};{origFileSize};{compressedFileSize}'.format(**r))
    docsFound +=1
    compressData.append(ci)

with open("compressionMetrics.json","w") as fp:
    json.dump(JSONEncoder().encode(compressData),fp)

print(docsFound)
