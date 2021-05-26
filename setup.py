from distutils.core import setup

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SDMXThon',
    project_urls={
        'documentation': 'https://docs.sdmxthon.meaningfuldata.eu',
        'source': 'https://github.com/Meaningful-Data/sdmxthon'
    },
    packages=['SDMXThon'],
    description='Library with SDMX to Pandas, Pandas to SDMX, '
                'SDMX validation and SDMX metadata validation',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    package_data=dict(
        SDMXThon=['*.py', 'api/*.py', 'model/*.py', 'parsers/*.py',
                  'utils/*.py', 'schemas/*']),
    version='0.9.5',
    license='Apache 2.0',
    license_files='license.txt',
    author='MeaningfulData',
    author_email='javier.hernandez@meaningfuldata.eu',
    url='https://github.com/Meaningful-Data/sdmxthon',
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
)
