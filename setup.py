from setuptools import setup
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)
                             
                             
setup(                       
    name='lexibank_baf2',    
    version="1.1.1",         
    description=metadata['title'],
    license=metadata.get('license', ''),
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
        ]},
    install_requires=[
        'pylexibank>=2.1',
        'lexibase',
        "pyedictor"
    ]
)
