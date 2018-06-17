from setuptools import setup, find_packages
setup(
    name="HelloWorld",
    version="0.1",
    packages=find_packages(),
    scripts=['woeusb.py', 'woeusbgui.py', 'utils.py', 'workaround.py', 'list_devices.py'],
)
