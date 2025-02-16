import tensorflowjs as tfjs
import tensorflow as tf
import gdown
import os
import shutil
import pathlib

def ensure_directories():
    """Ensure all required directories exist"""
    temp_dir = pathlib.Path('temp_model_dir')
    output_dir = pathlib.Path('../model')
    
    temp_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    return temp_dir, output_dir

def convert_h5_to_tfjs():
    try:
        # Setup directories
        temp_dir, output_dir = ensure_directories()
        
        # Download your model from Google Drive
        file_id = '1XrWEZJWOluRv2nMUiGmifiLnvzKkfUY9'  # Updated to your model's file ID
        output = temp_dir / 'model.h5'
        
        print('Downloading model from Google Drive...')
        gdown.download(f'https://drive.google.com/uc?id={file_id}', str(output), quiet=False)
        
        if not output.exists():
            raise Exception("Failed to download model file")
            
        print('Loading Keras model...')
        model = tf.keras.models.load_model(str(output))
        
        print('Model architecture:')
        model.summary()
        
        # Convert to tfjs format
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir()
        
        print('\nConverting model to TensorFlow.js format...')
        tfjs.converters.save_keras_model(model, str(output_dir))
        
        # Verify the conversion
        if (output_dir / 'model.json').exists() and \
           any(f.endswith('.bin') for f in output_dir.iterdir()):
            print('✅ Model converted successfully!')
            print(f'Files in {output_dir}:')
            for f in output_dir.iterdir():
                print(f' - {f.name} ({f.stat().st_size:,} bytes)')
        else:
            print('❌ Conversion may have failed - check the output files')
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f'❌ Error: {str(e)}')
        raise

if __name__ == '__main__':
    convert_h5_to_tfjs()