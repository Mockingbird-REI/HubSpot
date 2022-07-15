from setuptools import setup

setup(
    name='HubSpot',
    version='.1',
    packages=[
        'HubSpot',
        'HubSpot.CRM',
        "HubSpot.Files"
    ],
    url='',
    license='',
    author='tmcvety',
    author_email='tmcvety@mockingbirdrei.com',
    description='A Python interface to HubSpot',
    requires=[
        "requests"
    ]
)
