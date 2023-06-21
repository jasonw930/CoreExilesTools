import data.player as player_data

def login():
    (username, password) = player_data.account_credentials()
    player_data.login(username, password)

def load_client():
    player_data.load_client()
