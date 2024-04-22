from openbabel import openbabel
from pymongo import MongoClient
from datetime import datetime
import uuid

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['molecules']
collection = db['cif_files']

def  cif_to_sdf_and_upload(cif_file, sdf_file):
    mol = openbabel.OBMol()
    conv = openbabel.OBConversion()
    conv.SetInFormat("cif")
    conv.ReadFile(mol, sdf_file)
    conv.SetOutFormat("sdf")
    conv.WriteFile(mol, cif_file)
    cif_data = conv.WriteString(mol)
    with open(cif_file, 'w') as f:
        f.write(cif_data) 
    
    file_uuid = str(uuid.uuid4())
    current_time = datetime.now()
    file_document = {
        'uuid' : file_uuid,
        'cif_name' : cif_file,
        'datetime' : current_time,
        'data' : cif_data
    }
    collection.insert_one(file_document)
    return file_uuid

sdf_file = "sdf_sample.sdf"
cif_file = "cif_sample.cif"
file_uuid = cif_to_sdf_and_upload(sdf_file, cif_file)
print("CIF file uploaded with UUID:", file_uuid)
