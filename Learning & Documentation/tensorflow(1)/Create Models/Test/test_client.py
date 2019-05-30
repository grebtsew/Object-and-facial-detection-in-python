import logging
import numpy as np

#
# Test server and model
# If you send correct data with this code to server
# You will see what the server returns
# A great tool to test model varaibles and parameters if downloaded.
#

from predict_client.prod_client import ProdClient

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# In each file/module, do this to get the module name in the logs
logger = logging.getLogger(__name__)

# Make sure you have a model running on localhost:9000
host = '192.168.0.1:9000'
model_name = 'test'
model_version = 1

#img = np.zeros((1, 640, 480,3), dtype = np.int8)

req_data = [{'in_tensor_name': 'X', 'in_tensor_dtype': 'DT_FLOAT', 'data': 5},
{'in_tensor_name': 'Y', 'in_tensor_dtype': 'DT_FLOAT', 'data': 2}]

client = ProdClient(host, model_name, model_version)

prediction = client.predict(req_data, request_timeout=10)

print(prediction)
