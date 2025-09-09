from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tailor_management/__init__.py
from tailor_management import __version__ as version

setup(
	name="tailor_management",
	version=version,
	description="Custom ERPNext app for managing bespoke tailoring business",
	author="siijjas",
	author_email="",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)