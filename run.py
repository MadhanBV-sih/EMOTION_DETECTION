import os
import warnings
import logging

# Suppress Warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=UserWarning, module='fer')
logging.getLogger('werkzeug').setLevel(logging.ERROR)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Emotion Analyzer...")
    print("Go to http://0.0.0.0:8080 (or your Pi's IP address)")
    app.run(host='0.0.0.0', debug=True, port=8080, use_reloader=False)
