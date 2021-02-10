## Description

Some of the TIFF Files I am ingesting seem to have no level of compression.  I am running some comparisons between
various encoding schemes using tiffcp to see if theres an optimal compressor given tradeoff between compression time and
cost savings.

# Install latest version of libtiff from a wheel
pip3 install -U pip

pip3 install libtiff --find-links https://girder.github.io/large_image_wheels  --force-reinstall --no-cache-dir -I

 python3 -m pip install  --find-links https://girder.github.io/large_image_wheels  --force-reinstall --no-cache-dir -I libtiff


pip uninstall large_image_source-bioformats
