
# setup.py
from setuptools import setup
from setuptools import find_packages

packages= find_packages(exclude=["test"])

print(f"""
#######
PACKAGES:
        {"\n\t".join(packages)}
#######
""")

setup(
    name='CallGraph',
    version='25.4.21',
    packages=packages,
    install_requires=[
        'graphviz'
    ],
    author='Jonathan Graf',
    author_email='jonathangraf@outlook.de',
    description='Visualize the calls of python functions',
    long_description='',
    license='MIT',
    keywords=['visualize' 'programming' 'Dynamic Programming','Education'],
    url='https://https://github.com/JohnyJohnJohnson/tillingPuzzles'
)