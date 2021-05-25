from distutils.core import setup

with open('Readme.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SDMXThon',
    packages=['SDMXThon'],
    description='Library with SDMX to Pandas, Pandas to SDMX, SDMX validation and SDMX metadata validation',
    long_description=long_description,
    package_data=dict(
        SDMXThon=['*.py', 'api/*.py', 'model/*.py', 'parsers/*.py',
                  'utils/*.py', 'schemas/*']),
    version='0.9.4',
    license='Apache 2.0',
    license_files='license.txt',
    author='MeaningfulData',
    author_email='javier.hernandez@meaningfuldata.eu',
    url='https://docs.sdmxthon.meaningfuldata.eu/',
    keywords=['SDMX', 'Pandas', 'Validation'],
    install_requires=[
        'lxml',
        'pandas',
        'numpy',
        'validators',
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    project_urls={
        'Documentation': 'https://docs.sdmxthon.meaningfuldata.eu/',
        'Source': 'https://github.com/RubensHouse/sdmxthon',
    }
)
