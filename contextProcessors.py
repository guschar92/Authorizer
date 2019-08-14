"""
contextProcessors.py
----------------------

"""

#encoding=utf-8
from models import app, func,db

@app.template_filter('decryptor')
def decryptor(encrypted):
    """
    *Decrypt encrypted passwords*

    :param encrypted: ecrypted password
    :return: decrypted password
    """
    return bytearray.fromhex(db.session.query(func.decrypt_aes(encrypted)).first()[0].replace('\\x','')).decode()


@app.template_filter('none')
def none(value):
    """
    *Return None if value is ''*

    :param value:
    :return: value or ''
    """
    return value if value != None else ''

