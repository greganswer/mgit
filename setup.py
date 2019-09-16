from setuptools import setup, find_packages

setup(
    name="mgit",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        mgit=mgit.cli:cli
    """,
)
