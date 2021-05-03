import synapseclient
import synapseutils
import os, json, shutil, tqdm
from secrets import username,password

syn = synapseclient.Synapse()
syn.login(username,password)

 # Obtain a pointer and download the data
#syn18435847 = syn.get(entity='syn18435847')
#syn18435847 = syn.get(entity='syn18418455')  ## Image Analysis Working Group Files

IAWGFilesEntity = 'syn18418455'
 # Get the path to the local copy of the data file

localSyncPath = '/nvmen1Scratch/MVP'

dataSetsToSync = [{'fullSynapseName':'HTAN TNP - SARDANA','localAbbrev':'HTAN_TNP_SARDANA','localSyncPath':'/nvmen1Scratch/HTAN_TNP_SARDANA',"SynID":"syn18434611"}]


## load image metadata file Sheila generated

with open("./testData/image-rel1-metadata-20210426-153033.json","r") as fp:
	imd = json.load(fp)

print(len(imd),"images are in the current image metadata file")


for i in tqdm.tqdm(imd):
	curSyncDir = os.path.join(localSyncPath,i['HTAN_Center'],i['Imaging_Assay_Type'])
#	print(curSyncDir)
	if not os.path.isdir( curSyncDir):
	    os.makedirs(curSyncDir)
	try:
		synapseutils.sync.syncFromSynapse(syn,i['SynapseID'],path=curSyncDir,ifcollision='overwrite.local')
	except:
		print("Problem with current file...")
		print(i)

#for dst in dataSetsToSync:
#	curSyncDir = os.path.join(localSyncPath,dst['localAbbrev'])


