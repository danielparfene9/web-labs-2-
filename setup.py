from setuptools import setup

setup(
    name="go2web",
    version="0.1",
    py_modules=["main"],
    packages=["utils"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "go2web = main:main"
        ]
    },
)
