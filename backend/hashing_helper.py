import hashlib
import json
import os
import numpy as np

def split_and_hash_descriptor(descriptor):
    # convert  np.array to list, otherwise it messes up everything
    descriptor = np.array(descriptor)
    descriptor = descriptor.tolist()
    server_descriptor = str(descriptor[: len(descriptor) // 2]).encode()
    user_descriptor = str(descriptor[len(descriptor) // 2:]).encode()
    descriptor = str(descriptor).encode()
    # DEBUG: there is an issue with lossy recovery of our holography encryption,
    # DEBUG: the hashed results will not match
    # a byte format salt
    salt1 = os.urandom(50)
    descriptor_hash = hashlib.sha512(descriptor + salt1).hexdigest()
    # the salt2 and descriptor_user_hash are all downloaded
    salt2 = os.urandom(50)
    user_descriptor_hash = hashlib.sha512(user_descriptor + salt2).hexdigest()

    return (salt1, descriptor_hash , user_descriptor, salt2, user_descriptor_hash, server_descriptor )


def generate_user_descriptor_hash(user_descriptor, salt2):
    # user upload the half of descriptor and salt2
    # convert the string back to bytes
    # user_descriptor = eval(user_descriptor)
    # salt2 = eval(salt2)
    generated_user_descriptor_hash = hashlib.sha512(user_descriptor + salt2).hexdigest()
    return generated_user_descriptor_hash


def read_smith_file_old(filepath):
    with open(filepath) as file:
        user_descriptor, salt2 = pickle.load(file)
        return (user_descriptor, salt2)


def read_smith_file(file):
    data = json.load(file)
    # convert string back to list and bytes
    user_descriptor = eval(data['user_descriptor'])
    salt2 = eval(data['salt2'])
    return (user_descriptor, salt2)