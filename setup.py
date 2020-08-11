
import setuptools
with open("README.md", "r") as fh:
  long_description = fh.read()

print(setuptools.find_packages(where="src"))

setuptools.setup(
  name="pyrfdata_your_username",
  version="0.0.1",
  author="Your Name",
  author_email="your_email@example.com",
  description="Short description of pyrfdata",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/your_username/pyrfdata",
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  entry_points={
    'console_scripts': [
      'pyrfdata=pyrfdata.pyrfdata:main',
    ],
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
