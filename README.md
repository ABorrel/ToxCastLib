# ToxCast-lib (beta2)
Python library to load the Tox21-ToxCast assays from the invitroDB effort

# Dependencies
- Python 3.9


# Data
Using the invitroDB3.3 and the filtering from ICE for activities cleaning - Data needs to be unziped
- EPA invitroDB3.3 dataset (https://www.epa.gov/chemical-research/exploring-toxcast-data-downloadable-data)
- ICE invitroDB cleaning (https://ice.ntp.niehs.nih.gov/downloads/DataonICE/cHTS2021_invitrodb33_20210128.zip)
- Specify file from invritoDB in the invitroDB class



# Updates
- 8-22-19: init lib for bodymap project
- 8-23-19: Add function to wrtie AC50 chem by chem and add R script used to clean the assays data
- 9-02-19: Add top10 active chemicals extraction for one assay
- 10-30-19: Add function to analysis and extract assays and chem
- 04-21-20: add option to save by chemicals the number of assays tested
- 7-14-21: update using invitroDB 3.3 and ICE
- 7-19-21: push in the testpipy


## Usefull command lines
$python -m unittest tests/TestToxCastLib.py #unit test on Chemical class
$python setup.py sdist bdist_wheel
$python -m twine upload --repository testpypi dist/* #upload on testpypi and precise the version