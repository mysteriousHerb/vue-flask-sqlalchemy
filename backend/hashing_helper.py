import hashlib
import json
import os
import numpy as np
from holographic import HolographicEncryptionClassBuilder
from typing import Callable, Iterator, Union, Optional, List

def split_and_hash_descriptor(descriptor):
    # convert  np.array to list, otherwise it messes up everything
    descriptor = np.array(descriptor)
    descriptor = descriptor.tolist()
    # replace the splitting with the holographic encoding and decoding
    # server_descriptor = str(descriptor[: len(descriptor) // 2]).encode()
    # user_descriptor = str(descriptor[len(descriptor) // 2:]).encode()

    # splitting with the holographic encoding and decoding
    HolographicEncryptionClass = HolographicEncryptionClassBuilder()
    descriptor =  descriptor
    HolographicEncryptionClass.read_descriptor(descriptor)
    AbsMask_flat, PhMask_flat = HolographicEncryptionClass.find_optimal_encoding(iteration_num=5000, number_of_runs=10)
    
    server_descriptor = str(AbsMask_flat.tolist()).encode()
    user_descriptor = str(PhMask_flat.tolist()).encode()
    
    # Hashing
    descriptor = str(descriptor).encode()
    # DEBUG: there is an issue with lossy recovery of our holography encryption,
    # DEBUG: the hashed results will not match
    # a byte format salt
    salt1 = os.urandom(50)
    descriptor_hash = hashlib.sha512(descriptor + salt1).hexdigest()
    # the salt2 and descriptor_user_hash are all downloaded
    salt2 = os.urandom(50)
    user_descriptor_hash = hashlib.sha512(user_descriptor + salt2).hexdigest()

    return (salt1, descriptor_hash , user_descriptor, salt2, user_descriptor_hash, server_descriptor)


def GenerateUserDescriptorHash(user_descriptor, salt2):
    # user upload the half of descriptor and salt2
    # convert the string back to bytes
    # user_descriptor = eval(user_descriptor)
    # salt2 = eval(salt2)
    generated_user_descriptor_hash = hashlib.sha512(user_descriptor + salt2).hexdigest()
    return generated_user_descriptor_hash

def RecombineDescriptors(user_descriptor, server_descriptor):
    HolographicEncryptionClass = HolographicEncryptionClassBuilder()
    DescriptorRec = HolographicEncryptionClass.decoding(AbsMask_flat=server_descriptor, PhMask_flat=user_descriptor)

    return DescriptorRec


def read_smith_file(file):
    data = json.load(file)
    # convert string back to list and bytes
    # user_descriptor = eval(data['user_descriptor'])
    # salt2 = eval(data['salt2'])
    return (data['user_descriptor'], data['salt2'])


if __name__ == "__main__":
    mock_descriptor = np.random.rand(128)
    # print(mock_descriptor)
    salt1, descriptor_hash , user_descriptor, salt2, user_descriptor_hash, server_descriptor = split_and_hash_descriptor(mock_descriptor)
    # verify
    generated_user_descriptor_hash = GenerateUserDescriptorHash(user_descriptor, salt2)
    print(generated_user_descriptor_hash)
    if generated_user_descriptor_hash == user_descriptor_hash:
        print('yes')
        # convert byte to list
        user_descriptor = eval(user_descriptor.decode())
        server_descriptor = eval(server_descriptor.decode())
        recombined_descriptor = RecombineDescriptors(user_descriptor, server_descriptor)

        print(np.linalg.norm(recombined_descriptor - mock_descriptor))
