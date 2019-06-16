import face_recognition
import threading
import os
import pickle
import numpy as np

def GenerateDescriptorThread(image_path):
    # use a thread to do this so we dont block our server?
    thread = threading.Thread(target=GenerateDescriptor, args=[image_path])
    thread.start()

def GenerateDescriptor(image_path='image.jpg'):
    image = face_recognition.load_image_file(image_path)
    # re-sample the face when calculating encoding. 
    unknown_descriptor = face_recognition.face_encodings(image, num_jitters=5)
    if len(unknown_descriptor) > 0:
        unknown_descriptor = unknown_descriptor[0]
        with open(image_path+'.smith', 'wb') as file:
            pickle.dump(unknown_descriptor, file)
    

def MatchKnownDescriptor(known_descriptor, unknown_descriptors_folder):
    unknown_descriptors = []
    for filename in os.listdir(unknown_descriptors_folder):
        if '.smith' in filename:
            with open(os.path.join(unknown_descriptors_folder, filename),"rb") as file:
                unknown_descriptors.append(pickle.load(file)) 
    
    results = []
    for descriptor in unknown_descriptors:
        # results.append(face_recognition.compare_faces([known_descriptor], descriptor, tolerance=0.6))
        results.append(float(face_recognition.face_distance([known_descriptor], descriptor)))
        mean_distance = np.mean(results)
        # std = np.std(results)
        if mean_distance < 0.5:
            return True
        else:
            return False


if __name__ == "__main__":
    # with open(os.path.join('known_descriptors', 'tianheng.smith'), "rb") as file:
    #     known_descriptor = pickle.load(file)
    
    # unknown_descriptors_folder = 'temp2'
    # match_result = MatchKnownDescriptor(known_descriptor, unknown_descriptors_folder)

    # print(match_result)
    GenerateDescriptor(image_path='known_descriptors\\carlo.jpg')


