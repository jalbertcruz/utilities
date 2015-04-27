from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='GitFlowUtilities',

    version='0.0.1',

    description='Git utilities',
    long_description=long_description,

    url='https://github.com/jalbertcruz/',

    # Author details
    author='José Albert Cruz Almaguer',
    author_email='jalbertcruz@gmail.com',

    license='AGPL',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control Tools',

        'License :: OSI Approved :: AGPL License',

        'Programming Language :: Python :: 3.4',
    ],

    keywords='git development',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['GitPython', 'tornado'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={
    },

    data_files=[],

    entry_points={
    },
)