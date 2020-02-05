__author__ = 'Paul Severance'

from setuptools import setup

setup(
    name='charles-elasticsearch',
    version='0.0.1',
    author='Paul Severance',
    author_email='paul.severance@gmail.com',
    url='https://github.com/sugarush/charles-elasticsearch',
    packages=[
        'charles_elasticsearch'
    ],
    description='An Elasticsearch proxy for Sanic.',
    install_requires=[
        'fire_asynctest@git+https://github.com/sugarush/fire-asynctest@master#egg=fire-asynctest'
    ]
)
