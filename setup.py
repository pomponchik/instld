from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="installed",
    version="0.0.1",
    author="Evgeniy Blinov",
    author_email="zheni-b@yandex.ru",
    description="The simplest package management from the source code",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pomponchik/installed",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)
