from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mgit",
    author="Greg Answer",
    author_email="greganswer@gmail.com",
    description="Run Git work flows for GitHub with issue tracking ticket numbers from issue tracking services like Jira.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greganswer/mgit",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "setuptools_scm"],
    entry_points="""
        [console_scripts]
        mgit=mgit.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
