from setuptools import setup, find_packages

setup(
    name='py-cli-suite',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'cachetools',
        'beautifulsoup4',
        'python-dotenv',
        'pytubefix',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'suite = suite.cli:cli',
        ],
    },
    python_requires='>=3.6',
)
