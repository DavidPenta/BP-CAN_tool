# CAN tool

## Installation manual

1.	Download files from this repository.
2.	Add the required fields to the .env file. This includes the Django SECRET_KEY, credentials for two administrative accounts, and the password for the database.
3.	Open the terminal and navigate to the directory where the docker-compose.yml file is located.
4.	Run the command docker-compose up.
5.	The web application is now accessible at the following URL: http://localhost:8001.
6.	To run the web application on a different URL, add the URL to the CSRF_TRUSTED_ORIGINS list in the settings.py file. The settings.py file can be found in the CAN_tool_project folder within the django_project folder.
