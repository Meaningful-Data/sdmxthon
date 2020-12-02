from distutils.core import setup

setup(
    name='SDMXThon',
    packages=['SDMXThon'],
    package_data={
        'SDMXThon': ['*.py', 'common/*.py', 'data/*.py', 'message/*.py', 'metadata/*.py', 'model/*.py', 'query/*.py',
                     'registry/*.py',
                     'structure/*.py', 'test/*.py', 'utils/*.py']},
    version='0.0.5.8',
    license='MIT',
    description='Library with SDMX to Pandas, Pandas to SDMX, SDMX validation and SDMX metadata validation',
    author='Ruben Cardoso/Javier Hernandez',
    author_email='javier.hernandez@meaningfuldata.eu',
    url='https://github.com/RubensHouse/sdmxthon',
    download_url='',
    keywords=['SDMX', 'Pandas', 'Validation'],
    install_requires=[
        'lxml',
        'pandas',
        'numpy'
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
