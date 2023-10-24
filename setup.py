import setuptools

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open('sdmxthon/__version__.py', 'r') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['project'],
    version=about['version'],
    author=about['author'],
    author_email=about['author_email'],
    description=about['description'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=setuptools.find_packages(exclude=["testSuite"]),
    include_package_data=True,
    license='Apache 2.0',
    license_files='license.txt',
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
        'requests',
        'xmltodict'
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
