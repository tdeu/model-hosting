import numpy as np
import os
import pathlib

def ensure_model_directory():
    """Ensure the model directory exists"""
    model_dir = pathlib.Path(__file__).parent.parent / 'model'
    model_dir.mkdir(exist_ok=True)
    return model_dir

def generate_test_weights():
    """Generate dummy weights for testing the model"""
    try:
        # Get model directory
        model_dir = ensure_model_directory()
        weights_path = model_dir / 'weights.bin'

        # Generate random weights with specific seeds for reproducibility
        np.random.seed(42)
        
        # Conv2D weights
        conv_kernel = np.random.randn(3, 3, 3, 32).astype(np.float32)
        conv_bias = np.random.randn(32).astype(np.float32)
        
        # Dense layer weights
        dense_kernel = np.random.randn(100352, 4).astype(np.float32)
        dense_bias = np.random.randn(4).astype(np.float32)
        
        # Write to binary file
        with open(weights_path, 'wb') as f:
            f.write(conv_kernel.tobytes())
            f.write(conv_bias.tobytes())
            f.write(dense_kernel.tobytes())
            f.write(dense_bias.tobytes())
            
        print(f"✅ Generated test weights successfully at {weights_path}")
        print(f"File size: {weights_path.stat().st_size:,} bytes")
        
        # Verify the file exists and has content
        if weights_path.exists() and weights_path.stat().st_size > 0:
            return True
        else:
            print("❌ Weight file creation failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error generating weights: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = generate_test_weights()
        if not success:
            print("❌ Failed to generate weights!")
            exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        exit(1) 