from setuptools import setup

setup(name='gitlines',
      version='0.1',
      description='Very simple tool for analysing the size of a project.',
      author='Allan Clark',
      author_email='allan.clark@gmail.com',
      license='MIT',
      packages=['gitlines'],
      zip_safe=False,
      scripts=['gitlines/stats.py'],
      install_requires=[
          'matplotlib',
      ],
      )
