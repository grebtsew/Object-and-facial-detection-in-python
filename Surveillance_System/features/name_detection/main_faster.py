import face_recognition
import cv2
import file_handler
import threading
import time

print("Start program")

print("Make sure data folder exist")
file_handler.secure_data_files() # Make sure Data folders exist

print("Find images and names")
all_image_paths, known_face_names = file_handler.get_images_paths_and_names()

known_face_encodings = []
print("Load all images for recognition")
for path in all_image_paths:
    print("Currently at ", path)
    image = cv2.imread(path)
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)

print("Capture Camera")
video_capture = cv2.VideoCapture(0)

print("Start Stream")
while True:

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        else:
        # unknown person
            # Create name
            name = file_handler.get_available_name()
            print("got name ", name)

            # Save image
            path, image = file_handler.save_image(name, frame)
            file_handler.save_face(name,frame[top:bottom, left:right]) # save cropped image
            print("Saved image", path)

            # Update face_recognition list
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)
            print("updated encoding")
            # Do memory expand check
            file_handler.check_program_size()



        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


        file_handler.save_time_data(name)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
