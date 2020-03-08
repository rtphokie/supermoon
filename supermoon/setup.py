import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supermoon",
    version="0.0.1",
    author="Tony Rice",
    author_email="tony@rtphokie.org",
    description="calculates when a full moon coincides with lunar perigee",
    install_requires = ['skyfield'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rtphokie/supermoon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
