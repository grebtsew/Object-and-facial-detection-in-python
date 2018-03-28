
def load_model(path):
    global pnet
    global rnet
    global onet
    pnet, rnet, onet = detect_and_align.create_mtcnn(sess, None)
        
    model_exp = os.path.expanduser(path)
    if (os.path.isfile(model_exp)):
      #  print('Model filename: %s' % model_exp)
        with gfile.FastGFile(model_exp, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
            
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")            
    




# Object_detection
# @ returns True if detections successful
# @ returns False if no face found
#
# This function uses Tensorflow to make a face detection.
# Then transform the result to OpenCV 
#
def object_detection():
    #print("Detection")
    global face_box
    global frame
    global face_found
    global pnet
    global rnet
    global onet
    global show_id
    global show_bb
    global show_landmarks
    
    # Do detection
    face_patches, padded_bounding_boxes, landmarks = detect_and_align.align_image(frame, pnet, rnet, onet)

    # if found faces
    if len(face_patches) > 0:
        face_patches = np.stack(face_patches)
        feed_dict = {images_placeholder: face_patches, phase_train_placeholder: False}
       
        embs = sess.run(embeddings, feed_dict=feed_dict)

        print('Matches in frame:')
        for i in range(len(embs)):
            bb = padded_bounding_boxes[i]
            
            if show_bb:
                cv2.rectangle(frame, (bb[0], bb[1]), (bb[2], bb[3]), (255, 0, 0), 2)

            if show_landmarks:
                for j in range(5):
                    size = 1
                    top_left = (int(landmarks[i, j]) - size, int(landmarks[i, j + 5]) - size)
                    bottom_right = (int(landmarks[i, j]) + size, int(landmarks[i, j + 5]) + size)
                    cv2.rectangle(frame, top_left, bottom_right, (255, 0, 255), 2)
        
        # Convert box to OpenCV
        face_box = convert_tensorflow_box_to_openCV_box(padded_bounding_boxes[0])
    
        # if running custom tracker this is needed
        update_custom_tracker()

    
        face_found = True
        return True
        

    else:
        # No face
        face_found = False
        return False
