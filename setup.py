from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jarvis-ai",
    version="0.1.0",
    author="Jarvis AI Team",
    description="A comprehensive Jarvis-like AI system for automation, security, and development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "langchain>=0.1.0",
        "sentence-transformers>=2.2.2",
        "chromadb>=0.4.18",
        "redis>=5.0.0",
        "sqlalchemy>=2.0.0",
        "pyyaml>=6.0.0",
        "python-dotenv>=1.0.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.cli:main",
        ],
    },
)
