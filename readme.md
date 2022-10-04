About the script
=================
This script consists of automated test case suite for FedEx homepage Url below:
https://www.fedex.com/en-in/home.html
It is built using Pytest framework. 

Steps to run the script on local machine
==========================================
>> Create a folder in local machine
>> Right click on the folder and do git bash
>> Execute below command
>> git init (to initialize git)
>> git pull https://github.com/ashishakotkar/FedExHomepageTestingPytest.git
>> open pycharm terminal and execute below command to install the dependencies
>> pip install -r requirements.txt
>> Once the dependencies are installed, run the below command to execute the script
>> pytest -s -v -m "functional" testCases/test_rate_transit.py --browser chrome --html=./Reports/report.html --self-contained-html --capture=tee-sys

Running the project using Jenkins
==================================
>> install and login to jenkins
>> Click on new item
>> Click on configure
>> Click on Soource code management and add github url
>> Specify branch to build e.g. "*/master"
>> In build steps, select "Execute windows batch command"
>> add the below commands
cd <project directory>
pytest -s -v -m "functional" testCases/test_rate_transit.py --browser chrome --html=./Reports/reportJenkins.html --self-contained-html --capture=tee-sys