from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='PCM2Wav',
    version='1.2',
    packages=find_packages(),
    description="A PCM data to Wav audio format converter",
    long_description=readme(),
    url="https://github.com/roel0/PCM2Wav-py",
    author="Roel Postelmans",
    author_email="postelmansroel@gmail.com",
    license="GPL-2.0",
    classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering",
            "Topic :: Software Development :: Embedded Systems",
            "Topic :: Utilities",
            ],
    keywords='PCM I2S sigrok saleae wav audio',
    install_requires=['wave'],
    include_package_data=True,
)
