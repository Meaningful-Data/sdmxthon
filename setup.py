import setuptools

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='SDMXthon',
    description='Library with SDMX to Pandas, Pandas to SDMX, '
                'SDMX validation and SDMX metadata validation',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=setuptools.find_packages(),
    include_package_data=True,
    version='1.0.2',
    license='Apache 2.0',
    license_files='license.txt',
    author='MeaningfulData',
    author_email='javier.hernandez@meaningfuldata.eu',
    project_urls={
        'Bug Tracker': 'https://github.com/Meaningful-Data/sdmxthon/issues',
        'Documentation': 'https://docs.sdmxthon.meaningfuldata.eu',
        'Source Code': 'https://github.com/Meaningful-Data/sdmxthon',
        'Changelog': 'https://github.com/Meaningful-Data/sdmxthon/blob'
                     '/master/Changelog.rst '
    },
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
    ]
)
