# setup
create a venv
- python -m venv imgrestore
- .\imgrestore\Scripts\Activate.ps1   # activate
- deactivate  # deactivate

### verify venv
- pip -V  # check if indeed using venv

### package installs
- python -m pip install -r requirments.txt

# application 
- api dir: backend/ flask api handlers
- build dir: frontend/ UI layer
- tests dir: contain all of the tests
- db.py: methods that interact with the database
- factory: run instance of the application
