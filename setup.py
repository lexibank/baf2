from setuptools import setup, find_packages
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)
setup(
    name='lexibank_baf2',
    version="0.1",
    description=metadata['title'],
    license=metadata.get('license', ''),
    packages=find_packages(where="."),
    url=metadata.get('url',  ''),
    py_modules=['lexibank_baf2'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'baf2=lexibank_baf2:Dataset',
        ],
        'cldfbench.commands': [
            'baf2=baf2commands'
            ]
    },
    extras_require={
        'test': [
            'pytest-cldf',
        ],
        "full": ["python-igraph"]
        },
    install_requires=[
        'pylexibank>=3.0',
        'lexibase',
        'pyedictor',
    ]
)
