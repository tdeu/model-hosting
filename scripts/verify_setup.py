import requests
import json
import sys

def verify_setup():
    base_url = 'https://tdeu.github.io/model-hosting'
    
    # Check index.html
    print("Checking index.html...")
    try:
        response = requests.get(f'{base_url}/index.html')
        response.raise_for_status()
        print("✅ index.html accessible")
    except Exception as e:
        print(f"❌ Error accessing index.html: {str(e)}")
        return False

    # Check model.json
    print("\nChecking model.json...")
    try:
        response = requests.get(f'{base_url}/model/model.json')
        response.raise_for_status()
        model_config = response.json()
        print("✅ model.json accessible and valid JSON")
        
        # Check model format
        if 'format' in model_config and model_config['format'] == 'layers-model':
            print("✅ Valid TensorFlow.js model format")
        else:
            print("❌ Invalid model format")
            return False
    except Exception as e:
        print(f"❌ Error accessing model.json: {str(e)}")
        return False

    print("\n✨ Setup verified successfully!")
    return True

if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)