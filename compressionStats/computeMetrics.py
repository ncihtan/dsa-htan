import pymongo
import json
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

for r in c['htanAnalytics']['compressionStats'].find():
    #print(r) 
#    print(r['executionTime'],r['compressedFileSize'],r['compressionMethod'],r['origFileSize'],r['compressedFileSize']/r['origFileSize']*100)
       
    r['compressionRate'] = r['compressedFileSize']/r['origFileSize']*100

    print('{executionTime:0.2f};{compressionMethod};{compressionRate:0.2f};{origFileSize};{compressedFileSize}'.format(**r))
    
    docsFound +=1
    compressData.append(r)

with open("compressionMetrics.json","w") as fp:
    json.dump(JSONEncoder().encode(compressData),fp)

print(docsFound)
