import face_recognition
import os
import numpy as np
import copy
import cv2

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.

# Load a sample picture and learn how to recognize it.
root_folder_name = r"D:\Dropbox\SMITH\\"
known_faces_folder = root_folder_name + 'known_faces/'
unknown_faces_folder = root_folder_name + 'unknown_faces/'
database_folder = root_folder_name + 'database/'
encodings_folder = root_folder_name + 'encodings/'

def generate_encoding(filename):
    image = face_recognition.load_image_file(known_faces_folder + filename)
    # Given an image, return the 128-dimension face encoding for each face in the image.
    face_encoding = face_recognition.face_encodings(image)[0]
    return face_encoding

def convert_encoding_to_csv(face_encoding, filename='encoding.csv'):
    #  convert the face_encoding to 16 bit scale
    #  as the value ranges from -0.5 to 0.5, conver to  0 to 1
    face_encoding_output = face_encoding + 0.5
    # wrap around as a matrix
    face_encoding_output = face_encoding_output.reshape([8,16])
    
    with open(encodings_folder+filename, 'w+') as encoding_csv:
        for i in face_encoding_output:
            for j in i:
                encoding_csv.write('{},'.format(j))
            encoding_csv.write('\n')
    

    return(face_encoding_output)

def convert_encoding_to_image(face_encoding, filename='encoding.png'):
    #  convert the face_encoding to 16 bit scale
    #  as the value ranges from -0.5 to 0.5, conver to  0 to 1
    face_encoding_output = face_encoding + 0.5
    #  convert to 16 bit
    face_encoding_output *= 2**16
    face_encoding_output = face_encoding_output.astype(np.uint16)
    # wrap around as a matrix
    face_encoding_output = face_encoding_output.reshape([8,16])
    
    # cv2.imshow("Overlay image", face_encoding_output)
    cv2.imwrite(encodings_folder+filename, face_encoding_output)
    # cv2.waitKey(0)

    # print(face_encoding_output)
    return(face_encoding_output)


def convert_image_to_encoding(face_encoding_output):
    #  convert the 16 bit back to -0.5 to 0.5 scale - the format the NN can use
    face_encoding_output = face_encoding_output.astype(float)
    face_encoding_input = face_encoding_output / 2**16
    face_encoding_input -= 0.5
    face_encoding_input = face_encoding_input.flatten()
    # print(face_encoding_input)
    return(face_encoding_input)

def convert_csv_to_encoding(filename ='encoding.csv'):
    with open(encodings_folder+filename, 'r') as encoding_csv:
    #  convert the 16 bit back to -0.5 to 0.5 scale - the format the NN can use
        face_encoding_input = encoding_csv.read().replace('\n',',').split(',')[:-1]
        face_encoding_input = [float(i) for i in face_encoding_input]
        face_encoding_input = np.asarray(face_encoding_input)

        face_encoding_input -= 0.5
        face_encoding_input = face_encoding_input.flatten()
        # print(face_encoding_input)
        return(face_encoding_input)


if __name__ == "__main__":
    face_encoding = generate_encoding('Tianheng.jpg')
    face_encoding_output = convert_encoding_to_image(face_encoding, 'Tianheng_encoding.png')
    face_encoding_output = convert_encoding_to_csv(face_encoding, 'Tianheng_encoding.csv')

    face_encoding_output = cv2.imread(encodings_folder+'Tianheng_encoding.png', -1)
    face_encoding_input = convert_image_to_encoding(face_encoding_output)
    face_encoding_input = convert_csv_to_encoding('Tianheng_encoding_hologram.csv')

   
