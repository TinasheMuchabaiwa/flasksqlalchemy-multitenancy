from setuptools import setup, find_packages

setup(
    name="name",
    description="description",
    version="1.0.0",
    author="Tinashe Muchabaiwa",
    author_email="muchabaiwatinashe@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "python-dotenv",
        "flask",
        "flask-restx",
        "flask-sqlalchemy",
        "flask-migrate",
        "flask-login",
        "werkzeug==2.1.2",
        "flask-httpauth",
        "python-keycloak",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8<5",
            "pre-commit",
            "pydocstyle",
            "pytest",
            "pytest-black",
            "pytest-clarity",
            "pytest-dotenv",
            "pytest-flake8",
            "pytest-flask",
            "tox",
        ],
        "test": ["coverage"],
    },
)
