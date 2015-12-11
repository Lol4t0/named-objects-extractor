from distutils.core import setup


def requirements():
    with open('requirements.txt') as f:
        for x in f.readlines():
            yield x[:-1]

setup(
    name='named-objects-extractor',
    version='snapshot',
    packages=['named_objects_extractor'],
    url='https://github.com/Lol4t0/named-objects-extractor/',
    license='MIT',
    author='lol4t0',
    author_email='sidorov.ij@gmail.com',
    description='Extracting named entities: people, places, and organizations from text',
    install_requires=list(requirements())
)
