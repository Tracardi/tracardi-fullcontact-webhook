from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-fullcontact-webhook',
    version='0.6.0',
    description='This plugin reads data from FullContact service about the provided e-mail.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['tracardi_fullcontact_webhook'],
    install_requires=[
        'tracardi-plugin-sdk>=0.6.18',
        'tracardi',
        'tracardi-dot-notation',
        'pydantic',
        'aiohttp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)