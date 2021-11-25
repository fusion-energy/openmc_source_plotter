import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openmc_source_plotter",
    version="develop",
    author="The Fusion Energy Development Team",
    author_email="mail@jshimwell.com",
    description="Extract data and create plots of OpenMC particle sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/openmc_source_plotter",
    packages=setuptools.find_packages(),
    classifiers=[
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "plotly>=5.1.0",
        "numpy>=1.21.1",
        "h5py"
    ])
