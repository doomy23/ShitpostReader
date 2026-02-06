from setuptools import setup, find_packages

setup(
    name="shitpost-reader",
    version="0.1.0",
    description="A Python project that scrapes specific texts from websites and reads them out loud",
    author="doomy23",
    packages=find_packages(),
    install_requires=[
        "scrapy>=2.11.0",
        "pyttsx3>=2.90",
        "requests>=2.31.0",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "shitpost-reader=shitpost_reader.main:main",
        ],
    },
)
