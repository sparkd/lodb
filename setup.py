from setuptools import setup

setup(
    name='lodb',
    version='0.0.1',
    description='Linked Open Database',
    author='Ben Scott',
    author_email='ben@benscott.co.uk',
    packages=[
        'lodb',
        'lodb.api',
        'lodb.schema',
        'lodb.application'
    ],
    install_requires=[],
)
