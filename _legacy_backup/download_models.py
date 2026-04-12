import urllib.request
import os

base_url = "https://github.com/justadudewhohacks/face-api.js/raw/master/weights/"
files = [
    "ssd_mobilenetv1_model-weights_manifest.json",
    "ssd_mobilenetv1_model-shard1",
    "ssd_mobilenetv1_model-shard2"
]

output_dir = "static/models"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

for file in files:
    url = base_url + file
    output_path = os.path.join(output_dir, file)
    print(f"Downloading {file}...")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Downloaded {file}")
    except Exception as e:
        print(f"Failed to download {file}: {e}")
