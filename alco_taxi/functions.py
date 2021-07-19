#Function to get user_name when we log in
def get_user_name(user):
    user_name = str(user)[6:]
    end = int(user_name.find("'"))
    return user_name[:end]


#Function to marge dictionaries with products
def MergDictionary(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

