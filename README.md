1.Open the cmd promt.

2.Change the directory to invite.

3.Create a virtual environment:
	python -m venv venv

4.Activate the virtual environment.

5.Install the following packages to the virtual environment:
	pip install flask,
	pip install flask-SQLalchemy,
	pip install flask-migrate,
	pip install flask-login,
	pip install flask-WTF,
	pip install email-validator,
	pip install python-dotenv.

6.To Intialize database:
	flask db init,
	flask db migrate,
	flask db upgrade.

7.Finally to run the app:
	flask run
