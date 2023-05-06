from setuptools import setup, find_packages


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="instld",
    version="0.0.14",
    author="Evgeniy Blinov",
    author_email="zheni-b@yandex.ru",
    description="The simplest package management in runtime",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pomponchik/instld",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    entry_points = {
        'console_scripts': [
            'instld = installed.__main__:start'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)
