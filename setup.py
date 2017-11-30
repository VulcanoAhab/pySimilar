from distutils.core import setup

setup(
    name="pySimilar",
    version='0.1.0',
    author="VulcanoAhab",
    packages=["pySimilar"],
    url="https://github.com/VulcanoAhab/pySimilar.git",
    description="Similar Web API client",
    install_requires=[
        "requests==2.13.0"
        ]
)
