#!/bin/bash

cd sample-data
if [ -e small_sample-microdexed ]
then
  echo "Deleting old test output small_sample-microdexed/"
  rm -rf small_sample-microdexed
fi
python3 ../../smith-ywca-make-microdecies.py small_sample/
python3 ../../make-book-batch-ingest-folders.py --nocopy small_sample-microdexed/smith_ssc_324_r017_m001/
python3 ../../generate-derivatives.py --max-cpus 4 small_sample-microdexed/smith_ssc_324_r017_m001/

cd small_sample-microdexed/

echo "Number of OBJ* files"
find . -name "OBJ*" | wc -l
echo "Number of TN.jpg files"
find . -name "TN.jpg" | wc -l
echo "Number of JPG.jpg files"
find . -name "JPG.jpg" | wc -l
echo "Number of LARGE_JPG.jpg files"
find . -name "LARGE_JPG.jpg" | wc -l
echo "Number of JP2.jp2 files"
find . -name "JP2.jp2" | wc -l
echo "Number of HOCR.html files"
find . -name "HOCR.html" | wc -l
echo "Number of OCR.txt files"
find . -name "OCR.txt" | wc -l
echo "Number of TECHMD.xml files"
find . -name "TECHMD.xml" | wc -l
echo "Number of book/issue level TN.jpg files"
find . -maxdepth 1 -type d -name "smith_ssc_*" | xargs -n 1 -I % ls %/TN.jpg | wc -l
echo "Number of book/issue level OCR.txt files"
find . -maxdepth 1 -type d -name "smith_ssc_*" | xargs -n 1 -I % ls %/OCR.txt | wc -l

echo "Test sample output located in tests/sample-data/small_sample-microdexed/smith_ssc_324_r017_m001/"
