import girder_client
from secrets import apiKey

gc = girder_client.GirderClient(apiUrl="https://imaging.htan.dev/girder/api/v1")
gc.authenticate(apiKey=apiKey)

dccFolderList = gc.listFolder('5fa99a0051de21dd08ca7dfa',parentFolderType='collection')


for dccId in dccFolderList:
	print("Analyize %s " % dccId['name'])
