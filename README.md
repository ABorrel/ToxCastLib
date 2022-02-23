# ToxCast-lib (beta2)
Python library to load the Tox21-ToxCast assays from the invitroDB effort

# Dependencies
- Python 3.9


# Data
Using the invitroDB3.3 and the filtering from ICE for activities cleaning - Data needs to be unziped
- EPA invitroDB3.3 dataset (https://www.epa.gov/chemical-research/exploring-toxcast-data-downloadable-data)
- ICE invitroDB cleaning (https://ice.ntp.niehs.nih.gov/downloads/DataonICE/cHTS2021_invitrodb33_20210128.zip)
- Specify file from invritoDB in the invitroDB class
- Add in the package the mapping between the KC and the ToxCast assays


## Usefull command lines
>$python -m unittest tests/TestToxCastLib.py #unit test on Chemical class<br>
$python setup.py sdist bdist_wheel <br>
$python -m twine upload --repository testpypi dist/ToxCastLib-* #upload on testpypi and precise the version<br>
$pip install -i https://test.pypi.org/simple/ ToxCastLib==0.2.5