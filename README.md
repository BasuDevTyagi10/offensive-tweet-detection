# OFFENSIVE TWEET DETECTION WEB-APP
## General Info
**Project Purpose :** work done for miniproject evaluation GEU Semester-4
<!-- ## Table of Contents  
[1. General Info](#generalinfo)  
[2. Technologies](#technologies)  
[3. Setup](#setup)
<a name="generalinfo">
### General Info</a>
<a name="technologies"/>
### Technologies
<a name="setup"/>
### Setup -->

### Project Directory :
<b>&emsp;./model-training-&-testing :</b> contains the dataset csv files, jupyter notebook and pickle files. The jupyter notebook is used for Data Visualization, Data Cleaning and Model Training, Testing & Exporting (for using it in our Web-App)
<br><b>&emsp;./web-app :</b> contains the files for Flask Application (deployed on Heroku server - [link to App](https://offensive-tweet-detector.herokuapp.com)).

## Technologies
The project is created using :
* Python 3.8.8
* Flask 1.1.2
* HTML5 and CSS
* Bootstrap v5.0
* Heroku

## Getting Started
Clone the repo on local machine:
```sh
$ git clone https://github.com/BasuDevTyagi10/offensive-tweet-detection.git
$ cd "offensive-tweet-detection"
```
### Create a virtual environment (for better control (version control) over the project)
It is better to use Anaconda Navigator ([Anaconda Documentation - Installation](https://docs.anaconda.com/anaconda/install/)) for handling such (and further mentioned) tasks of creating virtual environments, installing packages, IDEs, Applications, etc.
<br>
<br>For performing the mentioned operations manually (without Anaconda) :
<br><br>Install ```virtualenv``` module to create isolated virtual environments.
```sh
$ pip install virtualenv
```
To create a Virtual Environment for Python 2.x do the following
```sh
$ virtualenv myenv
```
For a Python 3 virtual environment type –
```sh
$ python3 -m venv myenv
```
To activate the virtual environment -
<br>On Windows, run:
```sh
$ myenv\Scripts\activate.bat
```

### Installing required packages
The following packages will be required to be installed for running the ```4thSemProject.ipynb``` jupyter notebook:
<br>```jupyterlab```, ```pandas-profiling```, ```pandas```, ```matplotlib```, ```unidecode```, ```wordcloud```, ```plotly``` and ```scikit-learn```
<br>And the following for running the Flask web-app in development mode on localhost (Port:5000):
<br>```flask```, ```pandas``` and ```unidecode```
<br><br>Install the above mentioned packages in your virtual environment using Anaconda, and without it by:
<br>_run the below command after you're in your virtual environment_
```sh
(myenv)$ pip install jupyterlab pandas-profiling pandas matplotlib unidecode wordcloud plotly scikit-learn
```

### Run Jupyter Notebook for Data Analysis and to get a Trained Machine Learning Model
Once installed, launch JupyterLab with:
```sh
(myenv)$ cd model-training-&-testing
(myenv)$ jupyter-lab
```
Open the ```4thSemProject.ipynb``` jupyter notebook and Run All the Cells.
<br>The notebook will create 3 files, ```clean_traindata.csv```, ```trained_model.pickle``` and ```vectorizer.pickle```.
<br>Move ```trained_model.pickle``` and ```vectorizer.pickle``` to the ``web-app`` directory.
<br>Windows:
```sh
(myenv)$ move trained_model.pickle ../web-app
(myenv)$ move vectorizer.pickle ../web-app
```

### Run the Flask Web-App to test the Trained Machine Learning Model
Switch to ``web-app`` directory
```sh
(myenv)$ cd ../web-app
```
run the below command:
```sh
(myenv)$ python app.py
```
to run the app in the development mode.
<br>Open [http://localhost:5000](http://localhost:5000) to view it in the browser.

## Authors

-   **Basudev Tyagi** - _Initial work_ - [BasuDevTyagi10](https://github.com/BasuDevTyagi10)
