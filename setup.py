from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bhojpuripy",
    version="1.0.0",
    author="Open Source Community",
    author_email="developer@bhojpuripy.org",
    description="Universal Multilingual Translation Library for Bhojpuri (भोजपुरी)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/bhojpuripy",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "bhojpuripy": ["data/*.json"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Indic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "server": ["fastapi>=0.100.0", "uvicorn>=0.20.0"],
        "neural": ["torch>=2.0.0", "transformers>=4.30.0", "sentencepiece"],
        "dev": ["pytest", "black"],
    },
    entry_points={
        "console_scripts": [
            "bhojpuri=bhojpuripy.cli:main",
        ],
    },
)
