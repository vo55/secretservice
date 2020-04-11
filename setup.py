from setuptools import setup

setup(name='secretservice',
      version='0.1',
      description='Benchmarks how you are handling your AWS Secrets including encrypted parameters, secretsmanager and access keys',
      url='https://github.com/philipbarwi/secretservice',
      author='Philip Barwikowski',
      author_email='philip.barwi@web.de',
      license='MIT',
      packages=['secretservice'],
      setup_requires=[
          'wheel',
      ],
      install_requires=[
          'boto3',
      ],
      scripts=[
          'secrets-cli',
      ],
      zip_safe=True)
