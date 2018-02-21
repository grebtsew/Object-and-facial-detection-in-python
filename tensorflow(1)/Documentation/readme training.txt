 ----------- SKAPA BILDER ----------- Swedish commentary

bilder med tillhörande xml filer

ändra xml_to_script:
def main():
    for directory in ['train','test']:
        image_path = os.path.join(os.getcwd(), 'images/{}'.format(directory))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv('data/{}_labels.csv'.format(directory), index=None)
        print('Successfully converted xml to csv.')



kör:
xml_to_script.py # skapar filer i data-mappen

Ska se ut såhär:
Object-Detection
-data/
--test_labels.csv
--train_labels.csv
-images/
--test/ # 10 % av bilderna i träning
---testingimages.jpg
--train/
---testingimages.jpg
--...yourimages.jpg
-training
-xml_to_csv.py
-...

  --------  SKAPA RECORDS   ------------

Ändra generate_tfrecord:
def class_text_to_int(row_label):
    if row_label == 'macncheese':
        return 1
    else:
        None

Now we can run the generate_tfrecord.py script. 
We will run it twice, once for the train TFRecord and once for the test TFRecord.

python generate_tfrecord.py --csv_input=data/train_labels.csv --output_path=data/train.record

python generate_tfrecord.py --csv_input=data/test_labels.csv --output_path=data/test.record

Now, in your data directory, you should have train.record and test.record.

----------------- LADDA NER MODELL --------------

https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/

ändra config filen:

Currently, it is set to 24 in my configuration file. 
Other models may have different batch sizes. 
If you get a memory error, you can try to decrease the batch 
size to get the model to fit in your VRAM. Finally, 
you also need to change the checkpoint name/path, 
num_classes to 1, num_examples to 12, and label_map_path: 
"training/object-detect.pbtxt"


--------- SKAPA object-detection.pdtxt --------------

inuti training mappen

item {
  id: 1
  name: 'macncheese'
}


------------ STARTA träning -----------------

python train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/ssd_mobilenet_v1_pets.config


-------------- STARTA TENSORBOARD --------------

tensorboard --logdir=training

127.0.0.1:6006


------------ TESTNING ------------
Byt ut mot de nya mallarna vi skapat

