from setuptools import setup, find_packages

__version__ = "0.1"


setup(
    name="mesclan",
    author="Gregory Rehm",
    author_email="grehm87@gmail.com",
    version=__version__,
    description="Viva Mexico",
    packages=find_packages(),
    package_data={"*": ["*.html"]},
    entry_points={
        "console_scripts": [
            "mesclan=mesclan.main:main",
        ],
    },
    install_requires=[
        "flask",
        "flask-heroku",
        "flask-sqlalchemy",
        "hiredis",
        "ProxyTypes>=0.9,<1.0",
        "psycopg2",
        "redis",
        "requests",
        "ujson",
    ],
)
