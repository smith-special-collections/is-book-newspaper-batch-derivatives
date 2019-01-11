Description
===========
Tools for pre-generating derivatives, OCR, and FITS TECHMD for Islandora Book and Newspaper objects. Supports multiprocessing so that multiple processors can be leveraged.

If you have an ingest project of hundreds of thousands pages of materials that need to be ingested into an Islandora system this method of pre-generation can increase ingest rates by a factor of ten or more.

Make sure that you disable derivative generation and OCR in Islandora before you ingest the batches. Otherwise Islandora will create them even though you have provided derivatives!

Setting up paths
================
For most systems you will need to set the path to Kakadu and Fits. Copy config.py-example to config.py and edit as needed. You will also need to download and install them of course.

Usage
=====
```
python3 generate-derivatives.py --max-cpus 4 [Book Batch Folder]
```

`generate-derivatives.py` assumes a standard Islandora book/newspaper issue folder structure:

```
issue/book 1:
  MODS.xml (optional)
  00001:
    OBJ.tif
    MODS.xml (optional)
  00002:
    OBJ.tif
    MODS.xml (optional)
  00003:
    OBJ.tif
    MODS.xml (optional)
...

issue/book 2:
  MODS.xml (optional)
  00001:
    OBJ.tif
    MODS.xml (optional)
  00002:
    OBJ.tif
    MODS.xml (optional)
  00003:
    OBJ.tif
    MODS.xml (optional)
...

etc...
```

Tuning concurrent processes
===========================
Use the `--max-cpus` command line option to set how many concurrent processes should be run at a time in the multiprocessing pool. You can see the CPUs on your system using the `top` command. Press '1' to display all of the CPUs on the system.

Checking OCR output
===================
`tests/check-ocr-derivatives.py` can be used for a very rough assessment of OCR output. It will scan the pages of a book/issue and raise an error if greater than 90% of the pages of OCR output don't contain common English words. This litmus test can be useful for checking if the OCR is working at all on a given batch.

Usage
-----
```
python3 tests/check-ocr-derivatives.py [Book Batch Folder]
```

Requirements
============

GNU/Linux
---------
It is strongly recommended that this code be run on GNU/Linux. This code relies on several command line tools. GNU versions are assumed. The BSD versions that ship with Mac OS X may behave differently.

Python 3
--------
This code assumes Python version 3. Use 2 at your own risk.

Kakadu
------
For generated JPEG2000 JP2 derivatives:

http://kakadusoftware.com/downloads/

FITS
----
For generating TECHMD.xml:

https://projects.iq.harvard.edu/fits/home

Tesseract
---------
For generating HOCR and OCR:

Use your distro's package repository.

imagemagick
-----------
For converting files into different sizes and qualities

Use your distro's package repository.

Automated tests
===============

```
cd tests/
./test-all.sh
```

At the time of writing the test results should read:

```
Number of OBJ* files
      10
Number of TN.jpg files
      11
Number of JPG.jpg files
      10
Number of LARGE_JPG.jpg files
      10
Number of JP2.jp2 files
      10
Number of HOCR.html files
      10
Number of OCR.txt files
      11
Number of TECHMD.xml files
      10
Number of book/issue level TN.jpg files
       1
Number of book/issue level OCR.txt files
       1
```
Note that the number of TN.jpg and OCR.txt files is one greater than the number of pages, which accounts for the top level copies of one per book/issue.

As oddball images are discovered and the code updated to accommodate them, they should be added to the `tests/sample-data/small_sample directory` and documented in the README.md file in that directory.
