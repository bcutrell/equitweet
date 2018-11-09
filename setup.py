import setuptools

REQUIRED = ['twitter']
REQUIRES_PYTHON = '>=3.6.0'

with open("README.md", "r") as fh:
      long_description = fh.read()

setuptools.setup(
  name="equitweet",
  version="0.0.1",
  author="",
  author_email="bcutrell13@gmail.com",
  description="A small package for collecting $finance tweets",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/bcutrell/equitweet",
  py_modules=['equitweet'],
  package_data={'': ['LICENSE']},
  install_requires=REQUIRED,
  python_requires=REQUIRES_PYTHON,
  include_package_data=True,
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)

