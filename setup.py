from setuptools import setup


def readme_file():
    with open('README.md') as readme:
        data = readme.read()
    return data


setup(
    name='networkconfigutility',
    version='1.0.0',
    description='Utility for pushing configuration data to network devices and retrieving state data',
    long_description=readme_file(),
    long_description_content_type='text/markdown',
    author='naonder',
    author_email='nate.a.onder@gmail.com',
    license='MIT',
    packages=['networkconfigutility'],
    zip_safe=False,
    install_requires=['nornir']
)
