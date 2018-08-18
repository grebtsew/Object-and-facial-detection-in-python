Install python
Install tensorflow

Get modellS:
git clone https://github.com/tensorflow/models.git

Get protoc:
https://github.com/google/protobuf/releases

Set the enviromental variables to almost all folders! I had problems with this.
S�tt alla paths r�tt. I windows skapa milj�variabler, avancerade inst�llningar.
Se till att l�gga till typ alla mappar som verkar saknas!

(in cmd)
Copy  protoc.exe into object_detection.
run: ( i object_detection)
protoc object_detection/protos/*.proto --python_out=.

run: (i object_detection)
python setup.py build
python setup.py install


(not obligatory)
"notebooks" installs:
pip install jupyter
pip install matplotlib
