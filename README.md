# NinerChat

## Installation Instructions
`python3 -m venv env`\
`source env/bin/activate`\
`pip install -r requirements.txt`

## Running Flask App

Linux/MacOs:

`source env/bin/activate`\
`bash start.sh`\
`deactivate`

Windows:

`env\Scripts\activate`\
`start.bat`\
`deactivate`

## API
[See API folder](/application/api/README.md)

## Admin Account
There is a default admin account with elevated previledges:

    email: ninerchat@uncc.edu 
    password: admin

## Special URLs
### Clearing Database
    localhost:5000/clear
The NinerChat web server will clear the database and create an admin account

### Users list

    localhost:5000/users
Display a list of all users

### Room list
    localhost:5000/room/
Display a list of all rooms