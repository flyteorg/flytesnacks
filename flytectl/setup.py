from setuptools import find_packages, setup  # noqa

plugin_requires = ["flytekit>=0.18.0,<1.0.0"]

__version__ = "v0.1.2"

print(find_packages())

setup(
    name="yt-flyte-playground-flytectl",
    version=__version__,
    author="wily-coyote",
    author_email="queen@borg.hive",
    description="This is a demo only.",
    packages=find_packages(exclude=["tests*"]),
    install_requires=plugin_requires,
    license="apache2",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
