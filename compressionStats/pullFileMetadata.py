import json, pickle
import tifftools
import os, glob
import pymongo

dbCon = pymongo.MongoClient('localhost')
statsDbCon = dbCon['dsaCompressionStats']

def encode_json( z):
    if isinstance(z, bytes):
        return (str(z))

### I am just going to use a JSON dictionary as the database instead of going
### down the mongoDB route

''' To keep things simple, if the directory to be scanned does NOT have
recompressed in the path name, I am assuming it's an original input file'''

dirsToScan = ['/nvmen1Scratch/HTAN_TNP_SARDANA/Phase 1 Data/HMS pre-release sample data/*-0?.ome.tif',
			  '/nvmen1Scratch/recompress_testing/*.tiff']

recCount =  statsDbCon['recompressionStats'].count_documents({})
print("There are currently %d files in the tiffData directory" % recCount)

#https://weknowinc.com/blog/how-remove-duplicates-mongodb
for d in dirsToScan:
	for f in glob.glob(d):
		filename = os.path.basename(f)
		checkDbForFile = statsDbCon['recompressionStats'].find({'filename':filename})
		if 'recompress' not in f:
			rt = "original"
		else:
			rt = "recompressed"

		if not checkDbForFile.count():
			tto = tifftools.read_tiff(f)
			try:
				statsDbCon['recompressionStats'].insert_one({'filename':filename, 'fileSize': os.path.getsize(f), 'fullFilePath':f, 'recType': rt, 'recompressionInfo': json.loads(json.dumps(tto,default=encode_json))})
			except:
				print("Unable to load %s" % filename)
				continue

		deleteFiles = False
		if rt == 'recompressed' and deleteFiles:
			print("Trying to remove %s " %f )
			#os.remove(f)
		else:
			pass
			#print("Skipping original file %s" % f)
#os.remove()

#`json.loads(tifftools.read_tiff(<input file>)['ifds'][0][tifftools.Tag.ImageDescription.value]['data'])` 

'''		if filename not in ttod:
			print("Source file being scanned -- %s" % filename)
			tto = tifftools.read_tiff(f)
			
			if ft == 'original':
				ttod[filename] = { 'src': tto}
			else:
				ttod[filename] = {'recompressed' : tto}'''

