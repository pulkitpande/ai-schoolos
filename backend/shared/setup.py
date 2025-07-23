from setuptools import setup, find_packages

setup(
    name="ai-schoolos-shared",
    version="0.1.0",
    description="Shared utilities and models for AI SchoolOS",
    author="AI SchoolOS Team",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-dotenv>=1.0.0",
        "structlog>=23.2.0",
    ],
) 