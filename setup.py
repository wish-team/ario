from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ario",
    version="0.3.6",
    packages=find_packages(),
    author="Wish Team",
    description="A Flask-Based Package for Web Development",
    install_requires=required,
    url="https://github.com/wish-team/ario",
)
