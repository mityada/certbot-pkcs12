from setuptools import setup
from setuptools import find_packages


setup(
    name='certbot-pkcs12',
    packages=find_packages(),
    install_requires=[
        'certbot',
        'zope.interface',
        'pem',
    ],
    entry_points={
        'certbot.plugins': [
            'pkcs12 = certbot_pkcs12.installer:PKCS12Installer',
        ],
    },
)
