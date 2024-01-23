import string
import random 
import os
import uuid
import secrets

from datetime import datetime

def genrate_password(digits=8):
    """
    This function will genrate unique password with given digits

    Bydefault will generate 8 digits password
    """
    chs = string.ascii_letters + string.digits + '@_$.'
    password_ = ''
    for d in range(0, digits):
        password_ +=  chs[random.randint(0, len(chs) - 1)]
    return password_

def genrate_otp(digits=6):
    """
    This function will genrate otp for 6/4 digits by default.
    """
    if digits == 6:
        otp_ = random.randint(111111, 999999)
    elif digits == 4:
        otp_ = random.randint(1111, 9999)
    
    return otp_

def custom_filename(instance, filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f'{timestamp}_{unique_id}_{instance.FILENAME_WORD}.{extension}'
    return os.path.join(instance.DIR_NAME, new_filename)

def genrate_always_unique_id(word):
    """
    This function will return always unique id with one specific word
    Example : {20_char_string}_word
    """
    length = 20
    unique_id = secrets.token_hex(length // 2)
    return unique_id + '_' + word
