@"
import tensorflowjs as tfjs
import tensorflow as tf
import gdown
import os

def convert_h5_to_tfjs():
    try:
        # Download from Google Drive
        file_id = '1foeIsWYYmvr2UAoVyFSRhKPagsAmTLrs'
        output = 'temp_model.h5'
        
        print('Downloading model from Google Drive...')
        gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False)
        
        print('Converting model to TensorFlow.js format...')
        model = tf.keras.models.load_model(output)
        
        # Convert to tfjs format
        output_dir = 'model'
        os.makedirs(output_dir, exist_ok=True)
        tfjs.converters.save_keras_model(model, output_dir)
        
        print('Model converted successfully!')
        os.remove(output)
        
    except Exception as e:
        print(f'Error: {str(e)}')
        raise

if __name__ == '__main__':
    convert_h5_to_tfjs()
"@ | Out-File -FilePath scripts/convert_model.py -Encoding UTF8