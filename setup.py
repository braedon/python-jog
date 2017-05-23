from setuptools import setup, find_packages

setup(
    name='jog',
    version='0.1.0b2',
    description='JSON Structured Logging for Python',
    url='https://github.com/Braedon/python-jog',
    author='Braedon Vickers',
    author_email='braedon.vickers@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
    keywords='logging log json structured logstash',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
)
