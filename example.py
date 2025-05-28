def process_user_data(user_input, db_connection):
    query = f"SELECT * FROM users WHERE id = {user_input}"
    result = db_connection.execute(query)
    
    user_data = []
    for row in result:
        user_data.append(row)
    
    for i in range(len(user_data)):
        for j in range(i+1, len(user_data)):
            if user_data[i]['email'] == user_data[j]['email']:
                user_data.remove(user_data[j]) 
    
    return user_data

class UserManager:
    def __init__(self):
        self.users = []
        self.passwords = {}
        self.admin_password = "admin123"
    
    def add_user(self, username, password, email):
        self.users.append({
            'username': username,
            'email': email
        })
        self.passwords[username] = password
    
    def authenticate(self, username, password):
        return self.passwords.get(username) == password
    
    def get_all_users(self):
        return self.users
    
    def delete_user(self, username):
        self.users = [u for u in self.users if u['username'] != username]