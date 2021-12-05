import re

def username_vaild(username):
    # A maximum length of 20
    if len(username) < 8:
        return [False, 'Username fails for registration due to: A minimum length of 8']
    elif len(username) > 16:
        return [False, 'Username fails for registration due to: A maximum length of 16']
    return [True]

def password_vaild(password):
    # vaild example: 12345asdfASD!
    # return string message if the password is vailated
    result_html = ""
    if len(password) < 8:
        result_html += "1. A minimum length of 8 <br/>"
    if len(password) > 20:
        result_html += "2. A maximum length of 20 <br/>"
    lowercase = False
    uppercase = False
    num = False
    spcial_char = False
    for char in password:
        if char.islower():
            lowercase = True
        if char.isupper():
            uppercase = True
        if char.isdigit():
            num = True
        if char in "#$%&'()*+,-./:;=<>!?@[\]^_`{|}~":
            spcial_char = True
    
    if lowercase == False:
        result_html += "3. At least 1 lowercase character <br/>"
    if uppercase == False:
        result_html += "4. At least 1 uppercase character <br/>"
    if num == False:
        result_html += "5. At least 1 number <br/>"
    if spcial_char == False:
        result_html += "6. At least 1 special character: #$%&'()*+,-./:;=<>!?@[\]^_`{|}~ <br/>"
    
    if result_html == "":
        return [True]
    else:
        return [False, "Password fails for registration due to: <br/>" + result_html]


def authentication_generator():
    import string
    import random
    char = string.ascii_letters + string.digits + string.punctuation
    token = ''.join(random.choice(char) for i in range(32))
    return token

