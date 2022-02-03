import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ToxCastLib", # Replace with your own username
    version="0.3.2",
    author="Alexandre Borrel",
    author_email="a.borrel@gmail.com",
    description="Load in python the invitroDB3.3 with ToxCast assay results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ABorrel/ToxCastLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)
