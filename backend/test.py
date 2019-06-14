import pickle
import hashlib
import os

data = [1,2,3,5,7,8]
data_str_byte = str(data).encode()
# eval execute the string as python command
data_recovery = eval(data_str_byte.decode())


salt = os.urandom(50)
hashed_key = hashlib.sha512(salt + data_str_byte)
print(type(hashed_key.hexdigest()))
# print()
# print((hashed_key.digest()))


