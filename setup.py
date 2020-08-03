from setuptools import setup, find_packages

setup(
        name='price_downloader',
        version='1.1.1',
        packages=find_packages(include=['price_downloader', 'price_downloader.*']),
        install_requires=[
            'pandas',
            'yfinance',
            'sqlalchemy',
            'psycopg2',
            'python-dotenv',
            'click'
            ],
        entry_points={
            'console_scripts':['price_downloader = price_downloader.app:test'] 
            }
)
