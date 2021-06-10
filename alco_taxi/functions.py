#Function to get user_name when we log in
def get_user_name(user):
    user_name = str(user)[6:]
    end = int(user_name.find("'"))
    return user_name[:end]