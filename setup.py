from setuptools import setup, find_packages

setup(
    name="named_entity_evaluator",
    version="0.2.0",
    author="Mohammed Abdelmegeed",
    author_email="m.maguid9@hotmail.com",
    description="A Python package for Named Entity Recognition Evaluation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/M-Abdelmegeed/named_entity_evaluator",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
