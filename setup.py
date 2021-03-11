from distutils.core import setup

setup(
    name='SDMXThon',
    packages=['SDMXThon'],
    package_data=dict(
        SDMXThon=['*.py', 'api/*.py', 'model/*.py', 'parsers/*.py', 'utils/*.py']),
    version='0.8.9',
    license='MIT',
    description='Library with SDMX to Pandas, Pandas to SDMX, SDMX validation and SDMX metadata validation',
    author='Javier Hernandez/Ruben Cardoso',
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
