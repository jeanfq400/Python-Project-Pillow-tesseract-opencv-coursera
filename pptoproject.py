#The assignment grading is very simple, if you create something that looks like the
#two sample outputs (searching for "Chris" in the small images and "Mark" in the large
#images) you get full points! If you fail to handle the case where some pages have the
#text but no faces (with the Mark search) you can still pass the assignment, but I know
#you can do better!

import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!
img = {}
n_lst = []


def doc_unzip(z_name):

    zpfile = zipfile.ZipFile(z_name)
    for ch in zpfile.infolist():
        img[ch.filename] = [Image.open(zpfile.open(ch.filename))]
        n_lst.append(ch.filename)

if __name__ == '__main__':
    doc_unzip('readonly/images.zip')


    for name in n_lst:
        image = img[name][0]

        img[name].append(pytesseract.image_to_string(image).replace('-\n',''))


        if 'Mark' in img[name][1]:
            print('Results found in file', name)

            try:
                faces = (face_cascade.detectMultiScale(np.array(image),1.35,4)).tolist()

                img[name].append(faces)

                faces_in_each = []

                for x,y,w,h in img[name][2]:
                    faces_in_each.append(image.crop((x,y,x+w,y+w)))


                contact_sheet = Image.new(image.mode, (550, 110*int(np.ceil(len(faces_in_each)/5))))

                x = 0
                y = 0

                for face in faces_in_each:
                    face.thumbnail((110,110))
                    contact_sheet.paste(face, (x,y))

                    if x+110 == contact_sheet.width:
                        x=0
                        y=y+110
                    else:
                        x=x+110

                display(contact_sheet)
            except:
                print('But there were no faces in that file!')
