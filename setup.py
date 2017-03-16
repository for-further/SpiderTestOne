from distutils.core import setup
import py2exe
wd_path = 'C:\\Python27\\Lib\\site-packages\\selenium\\webdriver'
required_data_files = [('selenium/webdriver/remote', 
                        ['{}\\remote\\getAttribute.js'.format(wd_path), '{}\\remote\\isDisplayed.js'.format(wd_path)]), './phantomjs.exe']

setup(
    console = ['spider.py'],
    data_files = required_data_files,
    options = {
               "py2exe":{
                         "skip_archive": True,
                        }
               }
)