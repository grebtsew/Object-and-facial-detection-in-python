import xml.etree.cElementTree as ET

class detected_object:
    def __init__(self):
        self.positions = [0,0,0,0]
        self.name = ""
        self.pose = "Unspecified"
        self.truncated = 0
        self.difficult = 0


#Create file for tensorflow learning

def create_training_xml(folder,
                        filename,
                        path,
                        database,
                        width,
                        height,
                        depth,
                        segmented,
                        detected_objects_array,
                        result_folder):
 
 #folder = "" str path to image file folder
 #filename = "" srt image filename
 #path = "" str image full path
 #database = "" database "unknown"
 #width = "" image width
 #height = "" image height
 #depth = "" 
 #segmented = ""

 #detected_object_array = [] array of detected object struct ( contains all detected objects)   
 #name = "" object tag name
 #pose = "" 
 #truncated = "" 
 #difficult = "" 
 #xmin = ""  #ymin = "" #xmax = "" #ymax = "" box positions 
 #result_folder = "" Creates result xml i following folder with same name as image

 xml_annotation = ET.Element('annotation')

 ET.SubElement(xml_annotation, "folder").text = folder
 ET.SubElement(xml_annotation, "filename").text = filename
 ET.SubElement(xml_annotation, "path").text = path
 xml_source = ET.SubElement(xml_annotation, "source")
 ET.SubElement(xml_source, "database").text = database
 xml_size = ET.SubElement(xml_annotation, "size")
 ET.SubElement(xml_size, "width").text = width
 ET.SubElement(xml_size, "height").text = height
 ET.SubElement(xml_size, "depth").text = depth
 ET.SubElement(xml_annotation, "segmented").text = segmented

 for obj in object_array:
     xml_object = ET.SubElement(xml_annotation, "object")
     ET.SubElement(xml_object, "name").text = name
     ET.SubElement(xml_object, "pose").text = pose
     ET.SubElement(xml_object, "truncated").text = truncated
     ET.SubElement(xml_object, "difficult").text = difficult
     xml_bndbox = ET.SubElement(xml_object, "bndbox")
     ET.SubElement(xml_bndbox, "xmin").text = xmin
     ET.SubElement(xml_bndbox, "ymin").text = ymin
     ET.SubElement(xml_bndbox, "xmax").text = xmax
     ET.SubElement(xml_bndbox, "ymax").text = ymax
     
 file = ET.ElementTree(xml_annotation)
 file.write(str.join(result_dir,filename,".xml"))

 return
