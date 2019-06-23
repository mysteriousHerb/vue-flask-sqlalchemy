import face_recognition
import threading
import os
import pickle
import numpy as np
import json

class FaceReconHelperClassBuilder():
    def __init__(self, json_path='temp/temp.json'):
        self.json_path = json_path
        if not os.path.exists(self.json_path):
            data = {"known_descriptor": [], "unknown_descriptors":[], "match_distances": [], "match_result": False}
            with open(self.json_path, 'w+') as file:
                json.dump(data, file)


    def load_json_file(self):
        with open(self.json_path, 'r') as file:
            self.data = json.load(file)
            # have to convert everything to np.ndarray
            self.data['unknown_descriptors'] = [np.array(a) for a in self.data['unknown_descriptors']]
            self.data['known_descriptor'] = np.array(self.data['known_descriptor'])
            self.data['match_distances'] = np.array(self.data['match_distances'])

    
    def save_json_file(self):
        with open(self.json_path, 'w') as file:
            # convert everything back to list before saving
            self.data['unknown_descriptors'] = [a.tolist() for a in self.data['unknown_descriptors']]
            self.data['known_descriptor'] = self.data['known_descriptor'].tolist()
            self.data['match_distances'] = self.data['match_distances'].tolist()
            json.dump(self.data, file) 



    def GenerateDescriptorThread(self, image_path, unknown):
        # use a thread to do this so we dont block our server?
        thread = threading.Thread(target=self.GenerateDescriptor, args=[image_path])
        thread.start()

    def GenerateDescriptor(self, image_path='image.jpg', unknown=True):
        image = face_recognition.load_image_file(image_path)
        # re-sample the face when calculating encoding. 
        unknown_descriptor = face_recognition.face_encodings(image, num_jitters=5)
        if len(unknown_descriptor) > 0:
            # as the face_encodings is looking for multiple faces, it returns a list
            # convert ndarray to list to save to json file
            if unknown is True:
                self.load_json_file()
                self.data['unknown_descriptors'].append(unknown_descriptor[0])
                self.save_json_file()

        return unknown_descriptor[0]


    def LoadKnownDescriptor(self, known_descriptor):
        if self.ValidateDescriptor(known_descriptor):
            self.load_json_file()
            self.data['known_descriptor'] = known_descriptor
            self.save_json_file()


    def CompareDescriptors(self):
        self.load_json_file()
        if len(self.data['unknown_descriptors']) > 0 and len(self.data['known_descriptor'])>0:
            self.data['match_distances'] = face_recognition.face_distance(self.data['unknown_descriptors'], self.data['known_descriptor'])
            mean_distance = np.mean(self.data['match_distances'])
            # std = np.std(results)
            if mean_distance < 0.5:
                self.data['match_result'] = True
            else:
                self.data['match_result'] = False

            print(self.data['match_distances'])
            self.save_json_file()
            return self.data['match_result']

  
    def ValidateDescriptor(self, known_descriptor):
        example = np.arange(128)
        correct_type = type(example)
        correct_length = len(example)

        if type(known_descriptor) != correct_type:
            return False
        elif len(known_descriptor) != correct_length:
            return False
        else:
            return True



if __name__ == "__main__":
    FaceReconHelper = FaceReconHelperClassBuilder()
    # save new descriptor as unknown_descriptors
    FaceReconHelper.GenerateDescriptor(image_path='saved_files\\tz275.jpg', unknown=True)
    FaceReconHelper.GenerateDescriptor(image_path='saved_files\\tz275.jpg', unknown=True)
    # save new descriptor as known_descriptors
    tianheng_descriptor = FaceReconHelper.GenerateDescriptor(image_path='saved_files\\tz275.jpg', unknown=False)
    FaceReconHelper.LoadKnownDescriptor(tianheng_descriptor)
    # print match result
    print(FaceReconHelper.CompareDescriptors())




