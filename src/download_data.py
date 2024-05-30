from urllib.request import urlretrieve
import zipfile


SAMPLE_URL = "https://drive.usercontent.google.com/download?id=140PpLsdnVOQVIp5ia9jT_yvqtcWtF8Gj&export=download&confirm=t&uuid=483b1776-4e25-4976-9837-b498c823754a"
urlretrieve(SAMPLE_URL, "orthophotos.zip")

with zipfile.ZipFile("orthophotos.zip", 'r') as zip_ref:
    zip_ref.extractall("../data")

