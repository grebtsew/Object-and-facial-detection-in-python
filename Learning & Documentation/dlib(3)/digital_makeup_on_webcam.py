from PIL import Image, ImageDraw
import face_recognition
import cv2

#image = face_recognition.load_image_file("biden.jpg")


# Load the jpg file into a numpy array
video_capture = cv2.VideoCapture(0)

# Find all facial features in all the faces in the image
#face_landmarks_list = face_recognition.face_landmarks(image)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()


    face_landmarks_list = face_recognition.face_landmarks(frame)


    for face_landmarks in face_landmarks_list:
        #pil_image = Image.fromarray(frame)
       # d = ImageDraw.Draw(pil_image, 'RGBA')


    # Make the eyebrows into a nightmare
      #  cv2.polylines(frame,face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
      #  cv2.polylines(frame,face_landmarks['right_eyebrow'],true, (68, 54, 39))

        cv2.line(frame, face_landmarks['left_eyebrow'][0], face_landmarks['left_eyebrow'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['right_eyebrow'][0], face_landmarks['right_eyebrow'][4],(68, 54, 39), 5)

    # Gloss the lips
        #d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
        #d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))

        cv2.line(frame, face_landmarks['top_lip'][0], face_landmarks['top_lip'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['bottom_lip'][0], face_landmarks['bottom_lip'][4],(68, 54, 39), 5)


    # Sparkle the eyes
        #d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        #d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    # Apply some eyeliner
        cv2.line(frame, face_landmarks['left_eye'][0], face_landmarks['left_eye'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['right_eye'][0], face_landmarks['right_eye'][4],(68, 54, 39), 5)



    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
