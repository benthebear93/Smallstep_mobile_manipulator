from setuptools import find_packages
from setuptools import setup

package_name = 'ssmm_core'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='benlee',
    maintainer_email='nswve@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'helloworld_publisher = ssmm_core.helloworld_publisher:main',
            'helloworld_subscriber = ssmm_core.helloworld_subscriber:main',
        ],
    },
)
