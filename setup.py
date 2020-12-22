# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup
from setuptools import find_packages

# Minimum allowed version
MIN_PYTHON = (3, 7)

# Get package version
package_name = "giovanni"
try:
    version_path = Path(__file__).parent / package_name / 'VERSION'
    package_version = version_path.read_text().strip()
except FileNotFoundError:
    package_version = '0.0.0'

with open('requirements.txt', 'r') as req:
    req_file = [line for line in req.read().split() if line]

print("Requirements:\n" + '\n'.join(req_file))

with open("README.md", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()

# setup library
setup(
    name=package_name,
    version=package_version,
    description="Simulate the odds/time required to SR for a shiny",
    long_description=LONG_DESCRIPTION,
    author="Taylor Smith",
    project_urls={
        'Source Code': f'https://github.com/tgsmith61591/{package_name}',
    },
    author_email="taylor.smith@alkaline-ml.com",
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=req_file,
    python_requires=f'>={MIN_PYTHON[0]}.{MIN_PYTHON[1]}',
)
