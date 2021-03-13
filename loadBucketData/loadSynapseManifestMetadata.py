import girder_client
import pandas as pd
import glob
import os
from secrets import apiKey
import girder_utils as gu
import tqdm

## Connect to the girder Client
gc = girder_client.GirderClient(apiUrl="https://imaging.htan.dev/girder/api/v1")
gc.authenticate(apiKey=apiKey)



manifestDir = "../../htan-portal/data/manifests"

csvManifests = os.listdir(manifestDir)

hasImagingData = []

htanMeta = {}




for csv in csvManifests:
	print(csv)
	manifestDF = pd.read_csv(os.path.join(manifestDir,csv))
	try:
		imageData = manifestDF[manifestDF.Component.str.contains('Imag')]
		if imageData.size>0:
			imageData['baseFileName'] = imageData.Filename.apply(lambda x: x.split("/")[-1])
			hasImagingData.append({"csv":csv, "dataFrame":imageData})
			for r in imageData.to_dict(orient="records"):
				htanMeta[r['baseFileName']] = r



		print(imageData.size,manifestDF.size)
	except:
		print("Issues processing",csv)





itemSet = gu.listChildItems(gc,"resource/%s/items?type=folder" % ("604a544f8dfee73ac067d136"))


for i in itemSet:
	if i['name'] in htanMeta:
		print(htanMeta[i['name']])
