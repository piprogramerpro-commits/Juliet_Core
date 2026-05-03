from database import create_user, login_user

def register(username, password):
    return create_user(username, password)

def login(username, password):
    return login_user(username, password)
