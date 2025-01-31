from setuptools import setup

__version__ = "0.1"

setup(
    name="mle3112",
    version=__version__,
    author="Zeyu Deng",
    author_email="dengzeyu@gmail.com",
    maintainer="Zeyu Deng",
    maintainer_email="dengzeyu@gmail.com",
    install_requires=[
        "git+https://github.com/dengzeyu/NUS_experiment.git",
    ],
    license="MIT License",
    long_description=open("README.md").read(),
    python_requires=">=3.8",
    package_dir={"mle3112": "mle3112"},
)