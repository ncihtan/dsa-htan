import girder_client
import secrets as s

gc = girder_client.GirderClient(apiUrl="https://imaging.htan.dev/girder/api/v1")
gc.authenticate(apiKey=s.dsaApiKey)


dccDSABucketKeys=  ['htan-dcc-chop','htan-dcc-dfci','htan-dcc-hms','htan-dcc-htapp','htan-dcc-mask','htan-dcc-ohsu','htan-dcc-pcapp',
		'htan-dcc-stanford','htan-dcc-tma-tnp','htan-dcc-vanderbilt','htan-dcc-washu','htan-dcc-bu','htan-dcc-duke']


for bucketKey in dccDSABucketKeys:
	print("Importing data from %s" % bucketKey)
	gc.post("htan/reimport/%s" % bucketKey)
