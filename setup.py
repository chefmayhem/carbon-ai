from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="carbon_ai",
    version="0.1.0",
    author="chefmayhem",
    author_email="nope!",
    description="Use generative AI to calculate carbon emissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chefmayhem/carbon_ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "openai>=1.50"
    ],
    python_requires='>=3.10',
)