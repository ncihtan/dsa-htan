import os
import subprocess
import sys

compressionList = [
    [],
    ['--compression', 'none'],
    ['--compression', 'none', '--tile', '1024'],
    ['--compression', 'jpeg'],
    ['--compression', 'jpeg', '-q', '95'],
    ['--compression', 'jpeg', '-q', '90'],
    ['--compression', 'jpeg', '-q', '80'],
    ['--compression', 'jpeg', '-q', '70'],
    ['--compression', 'jpeg', '--tile', '1024'],
    ['--compression', 'jpeg', '-q', '95', '--tile', '1024'],
    ['--compression', 'jpeg', '-q', '90', '--tile', '1024'],
    ['--compression', 'jpeg', '-q', '80', '--tile', '1024'],
    ['--compression', 'jpeg', '-q', '70', '--tile', '1024'],
    ['--compression', 'deflate'],
    ['--compression', 'deflate', '--predictor', 'none'],
    ['--compression', 'deflate', '--predictor', 'horizontal'],
    ['--compression', 'deflate', '--tile', '1024'],
    ['--compression', 'deflate', '--level', '1'],
    ['--compression', 'deflate', '--level', '9'],
    ['--compression', 'lzw'],
    ['--compression', 'lzw', '--predictor', 'none'],
    ['--compression', 'lzw', '--predictor', 'horizontal'],
    ['--compression', 'lzw', '--tile', '1024'],
    ['--compression', 'zstd'],
    ['--compression', 'zstd', '--predictor', 'none'],
    ['--compression', 'zstd', '--predictor', 'horizontal'],
    ['--compression', 'zstd', '--tile', '1024'],
    ['--compression', 'zstd', '--level', '1'],
    ['--compression', 'zstd', '--level', '9'],
    ['--compression', 'zstd', '--level', '22'],
    ['--compression', 'packbits'],
    ['--compression', 'packbits', '--predictor', 'none'],
    ['--compression', 'packbits', '--predictor', 'horizontal'],
    ['--compression', 'packbits', '--tile', '1024'],
    ['--compression', 'jbig'],
    ['--compression', 'jbig', '--tile', '1024'],
    ['--compression', 'lzma'],
    ['--compression', 'lzma', '--tile', '1024'],
    ['--compression', 'webp'],
    ['--compression', 'webp', '-q', '0'],
    ['--compression', 'webp', '-q', '100'],
    ['--compression', 'webp', '-q', '95'],
    ['--compression', 'webp', '-q', '90'],
    ['--compression', 'webp', '-q', '80'],
    ['--compression', 'webp', '-q', '70'],
    ['--compression', 'webp', '--tile', '1024'],
    ['--compression', 'webp', '-q', '0', '--tile', '1024'],
    ['--compression', 'jp2k'],
    ['--compression', 'jp2k', '--psnr', '80'],
    ['--compression', 'jp2k', '--psnr', '70'],
    ['--compression', 'jp2k', '--psnr', '60'],
    ['--compression', 'jp2k', '--psnr', '50'],
    ['--compression', 'jp2k', '--psnr', '40'],
    ['--compression', 'jp2k', '--cr', '100', ''],
    ['--compression', 'jp2k', '--cr', '1000', ''],
    ['--compression', 'jp2k', '--cr', '10000'],
    ['--compression', 'jp2k', '--tile', '1024'],
    ['--compression', 'jp2k', '--psnr', '80', '--tile', '1024'],
    ['--compression', 'jp2k', '--psnr', '70', '--tile', '1024'],
    ['--compression', 'jp2k', '--psnr', '60', '--tile', '1024'],
    ['--compression', 'jp2k', '--psnr', '50', '--tile', '1024'],
    ['--compression', 'jp2k', '--psnr', '40', '--tile', '1024'],
    ['--compression', 'jp2k', '--cr', '100', '--tile', '1024'],
    ['--compression', 'jp2k', '--cr', '1000', '--tile', '1024'],
    ['--compression', 'jp2k', '--cr', '10000', '--tile', '1024'],
]
allOpts = ['-vw', '--stats']

if not len(sys.argv):
    print("""test_compression.py (output directory) (input file ...)""")
    sys.exit(0)
for input in sys.argv[2:]:
    root = os.path.join(sys.argv[1], os.path.splitext(os.path.basename(input))[0])
    for opts in compressionList:
        output = root + '.' + '.'.join(str(opt).strip('-') for opt in opts) + '.tiff'
        cmd = ['large_image_converter', input, output] + opts + allOpts
        print(' '.join(cmd))
        subprocess.check_call(cmd)
