from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="carbon_ai",
    version="0.1.0",
    author="chefmayhem",
    author_email="your_email@example.com",
    description="Use generative AI to calculate carbon emissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chefmayhem/carbon_ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)