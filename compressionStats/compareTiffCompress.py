import os, json, sys
import multiprocessing as mp
import numpy as np
import time
import subprocess as sp
import glob 
from pymongo import MongoClient
import shutil 
import psutil 
from random import shuffle
#from libtiff import TIFFfile, TIFFimage

c = MongoClient()

outputDir = "/nvmen1Scratch/origData/htan-tnp-sardana-hms-prerelease-phase-1-data/recompressed/"
omeTiffDir = "/s3FuseMounts/dgutman-htan-s3-synapse/htan-tnp-sardana-hms-prerelease-phase-1-data/*.ome.tif"
fileSet = glob.glob(omeTiffDir)

def generate_compression_options(fullFilePath,checkIfRun=True):
    compressStrings = ["lzw","zip","zip:2","jpeg:95","jpeg:90","jbig","zstd","ztsd:2"]  ## removed lzma  and ztsd and ztsd:2 and lzma is hidden again
    tileString = ["-8","-t","-w","256","-l","256","-L"]
    filename = os.path.basename(fullFilePath)
    csOptionsToRun = []

    for cs in compressStrings:
        outputFile = filename.replace("ome.tif","")
        outputFile = outputFile + cs + ".ome.tif"

        compressOptions = {'compressionMethod':cs,'filename':filename,'tileString':tileString,'outputFile':outputFile,'fullFilePath':fullFilePath}

        if checkIfRun:
            l = c['htanAnalytics']['compressionStats'].find_one({'origCompressionDict':compressOptions})
            if l:
                print(l['origFileName'],"Already compelted")
            else:
                csOptionsToRun.append(compressOptions)
    return csOptionsToRun

# https://www.machinelearningplus.com/python/parallel-processing-python/
#pool = mp.Pool(mp.cpu_count())

def get_tiff_stats( compressionDict ):
    start_time = time.time() ## Calculating run time
    cd = compressionDict

    print("Processing",cd['filename'])
    stats = os.stat(cd['fullFilePath'])

    cm = cd['compressionMethod']
    outputFileNameWpath = os.path.join(outputDir,cd['outputFile'])
    print(["tiffcp" ," ".join(cd['tileString']), "-c",cm,cd['fullFilePath'], outputFileNameWpath])
    tileString = cd['tileString']
    tiffCpData = sp.run(["tiffcp " + " ".join(cd['tileString'])+ " -c "+cm+" " +cd['fullFilePath']+ " " +outputFileNameWpath],shell=True)

    try:
        compressFileStats = os.stat(outputFileNameWpath)

        compressInfo = {'origFileName':cd['filename'],'origFileSize': stats.st_size, 
		'outputFileNamewPath': outputFileNameWpath, 'executionTime': time.time()-start_time, 'tileInfo':cd['tileString'],
                'compressedFileSize':compressFileStats.st_size, 'compressionMethod': cm , 'origCompressionDict':cd}
        c['htanAnalytics']['compressionStats'].insert_one(compressInfo)
    except:
        print("Something wrong with command string",cd)

    disk = psutil.disk_usage('/nvmen1Scratch')
    if (disk.percent > 80):
        os.remove(outputFileNameWpath)

    return(compressInfo)


#pool = mp.Pool(processes=2)
#print("Will be running on %d cores" % mp.cpu_count())

pool = mp.Pool(processes=4)
compressionOptionSet = []

for f in fileSet:
    compressionOptionSet += generate_compression_options(f)

shuffle(compressionOptionSet)

print(len(compressionOptionSet),"Options to be run")

results = pool.map(get_tiff_stats, [row for row in compressionOptionSet])
print(results)

pool.close()

