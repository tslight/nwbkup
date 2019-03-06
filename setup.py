import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nwbkup",
    version="0.0.1",
    description="Backup network device configs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['netmiko', 'columns'],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'nwbkup = nwbkup.__main__:main',
        ],
    }
)
