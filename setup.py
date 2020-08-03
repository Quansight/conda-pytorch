import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="conda-pytorch",
    version="0.0.0",
    author="Quansight",
    description="Conda PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quansight/conda-pytorch",
    packages=['conda_pytorch'],
    license="BSD",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'conda-pytorch = conda_pytorch.main:main',
        ],
    }
)
