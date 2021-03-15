from setuptools import setup

setup(
    name='api-tester-rokuten',
    version='0.0.1',
    description='API Testing to Rakuten Interview',
    author='Manuel Lara',
    author_email="lararojas.mr@gmail.com",
    packages=['specs'],
    install_requires=['pytest', 'pytest-easy-api', 'argparse', 'jsonschema', 'teamcity-messages'],
    keywords=['testing', 'pytest', 'api']
)
