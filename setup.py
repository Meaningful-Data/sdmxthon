from distutils.core import setup

setup(
    name='SDMXThon',
    packages=['SDMXThon'],
    package_data=dict(
        SDMXThon=['*.py', 'api/*.py', 'model/*.py', 'parsers/*.py', 'utils/*.py']),
    version='0.8.12',
    license='Apache 2.0',
    license_files='license.txt',
    description='Library with SDMX to Pandas, Pandas to SDMX, SDMX validation and SDMX metadata validation',
    author='MeaningfulData',
    author_email='javier.hernandez@meaningfuldata.eu',
    url='https://github.com/RubensHouse/sdmxthon',
    download_url='',
    keywords=['SDMX', 'Pandas', 'Validation'],
    install_requires=[
        'lxml',
        'pandas',
        'numpy',
        'validators',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
