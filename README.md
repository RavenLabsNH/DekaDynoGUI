# DekaDynoGUI
Front End Application (HMI) for Deka Dyno

Copyright © 2022 Raven Labs -
Manchester, New Hampshire
www.ravenlabsnh.com

# Getting Started
Building the Dyno front end is relatively easy.

### 1. Install Python 3.9
Using whatever means are appropriate for your platform (MacOS, Linux, or Windows), 
install Python version 3.9 or better/

### 2. Clone the repository
`$ git clone git@github.com:RavenLabsNH/DekaDynoGUI.git`

### 3. Change to the project directory 
`$ cd DekaDynoGUI`

### 4. Create a virtual environment and activate it
You can call the environment anything you want -- by convention I usually call it `env`.
Note that the command to activate the virtual environment differs on Windows.  See https://docs.python.org/3.9/tutorial/venv.html
```
$ python3 -m venv env # creates virtual environment in subdirctory 'env'

$ env/bin/activate # for MacOS/Unix/Linux

> env\Scripts\activate.bat # for Windows
```
### 5. Install requirements
`$ pip3 install -r requirements.txt`

### 6. Launch the application
`$ python3 main.py`
