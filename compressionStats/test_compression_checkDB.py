import itertools
import os
import subprocess
import sys

## This will also check mongo to see if the file name already exists...
import pymongo
dbCon = pymongo.MongoClient('localhost')['dsaCompressionStats']

allOpts = ['-vw', '--stats']
matrix = [[
    [],
    ['--compression', 'none'],
    ['--compression', 'jpeg'],
    ['--compression', 'jpeg', '-q', '95'],
    ['--compression', 'jpeg', '-q', '90'],
    ['--compression', 'jpeg', '-q', '80'],
    ['--compression', 'jpeg', '-q', '70'],
    ['--compression', 'deflate'],
    ['--compression', 'deflate', '--predictor', 'none'],
    ['--compression', 'deflate', '--predictor', 'horizontal'],
    ['--compression', 'deflate', '--level', '1'],
    ['--compression', 'deflate', '--level', '9'],
    ['--compression', 'lzw'],
    ['--compression', 'lzw', '--predictor', 'none'],
    ['--compression', 'lzw', '--predictor', 'horizontal'],
    ['--compression', 'zstd'],
    ['--compression', 'zstd', '--predictor', 'none'],
    ['--compression', 'zstd', '--predictor', 'horizontal'],
    ['--compression', 'zstd', '--level', '1'],
    ['--compression', 'zstd', '--level', '9'],
    ['--compression', 'zstd', '--level', '22'],
    ['--compression', 'packbits'],
    ['--compression', 'packbits', '--predictor', 'none'],
    ['--compression', 'packbits', '--predictor', 'horizontal'],
    # ['--compression', 'jbig'],
    # ['--compression', 'lzma'],
    ['--compression', 'webp'],
    ['--compression', 'webp', '-q', '0'],
    ['--compression', 'webp', '-q', '100'],
    ['--compression', 'webp', '-q', '95'],
    ['--compression', 'webp', '-q', '90'],
    ['--compression', 'webp', '-q', '80'],
    ['--compression', 'webp', '-q', '70'],
    ['--compression', 'jp2k'],
    ['--compression', 'jp2k', '--psnr', '80'],
    ['--compression', 'jp2k', '--psnr', '70'],
    ['--compression', 'jp2k', '--psnr', '60'],
    ['--compression', 'jp2k', '--psnr', '50'],
    ['--compression', 'jp2k', '--psnr', '40'],
    ['--compression', 'jp2k', '--cr', '100', ''],
    ['--compression', 'jp2k', '--cr', '1000', ''],
    ['--compression', 'jp2k', '--cr', '10000'],
], [
    [],  # 256
    ['--tile', '512'],
    ['--tile', '1024'],
]]



matrixV2 = [[
    ['--compression', 'jpeg'],
    ['--compression', 'jpeg', '-q', '95'],
    ['--compression', 'jpeg', '-q', '90'],
    ['--compression', 'jpeg', '-q', '80'],
    ['--compression', 'jpeg', '-q', '70'],
    ['--compression', 'deflate'],
    ['--compression', 'zstd'],
    ['--compression', 'zstd', '--level', '1'],
    ['--compression', 'zstd', '--level', '9'],
    ['--compression', 'zstd', '--level', '22'],
    ['--compression', 'packbits'],
    ['--compression', 'jp2k'],
    ['--compression', 'jp2k', '--psnr', '80'],
    ['--compression', 'jp2k', '--psnr', '70'],
    ['--compression', 'jp2k', '--psnr', '60'],
    ['--compression', 'jp2k', '--psnr', '50'],
    ['--compression', 'jp2k', '--psnr', '40'],
    ['--compression', 'jp2k', '--cr', '100', ''],
    ['--compression', 'jp2k', '--cr', '1000', ''],
    ['--compression', 'jp2k', '--cr', '10000'],
], [
    [],  # 256
    ['--tile', '512'],
#    ['--tile', '1024'],
]]

if not len(sys.argv):
    print("""test_compression.py (output directory) (input file ...)""")
    sys.exit(0)

for input in sys.argv[2:]:
    root = os.path.join(sys.argv[1], os.path.splitext(os.path.basename(input))[0])
    for optList in itertools.product(*matrixV2):
        opts = [opt for subList in optList for opt in subList]

        output = root+ '.' + '.'.join(str(opt).strip('-') for opt in opts) + '.tiff'

        print(output,os.path.basename(output))
		### Check if file has been run
        checkDb = dbCon['recompressionStats'].find({'filename': os.path.basename(output)})		
        print(checkDb.count())
#        if checkDb.count():
        if False:
            print("Already ran %s" % output)		
        else:
            cmd = ['large_image_converter', input, output] + opts + allOpts
            print(' '.join(cmd))
            subprocess.call(cmd)
