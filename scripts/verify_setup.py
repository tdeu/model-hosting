import requests
import json
import sys
import os
from pathlib import Path
import importlib

def verify_model_files(model_dir):
    """Verify model files locally before deployment"""
    model_dir = Path(model_dir)
    if not model_dir.exists():
        print("❌ Model directory not found!")
        return False
        
    model_json_path = model_dir / 'model.json'
    if not model_json_path.exists():
        print("❌ model.json not found!")
        return False
        
    try:
        with open(model_json_path, 'r') as f:
            model_config = json.load(f)
            print("✅ model.json is valid JSON")
            
        # Verify model structure
        if 'modelTopology' not in model_config:
            print("❌ model.json missing modelTopology!")
            return False
            
        if 'weightsManifest' not in model_config:
            print("❌ model.json missing weightsManifest!")
            return False
    except json.JSONDecodeError:
        print("❌ model.json is not valid JSON!")
        return False
        
    # Check for weights files
    weights_files = list(model_dir.glob('*.bin'))
    if not weights_files:
        print("❌ No weight files found!")
        return False
        
    print(f"✅ Found {len(weights_files)} weight files:")
    for f in weights_files:
        size = f.stat().st_size
        print(f" - {f.name} ({size:,} bytes)")
        
    return True

def verify_deployed_model(base_url):
    """Verify deployed model is accessible"""
    print(f"\nVerifying deployed model at {base_url}")
    
    # Check model.json
    try:
        response = requests.get(f'{base_url}/model/model.json')
        response.raise_for_status()
        model_config = response.json()
        print("✅ model.json accessible and valid")
        
        # Verify weights files
        for manifest in model_config.get('weightsManifest', []):
            for path in manifest.get('paths', []):
                weight_url = f'{base_url}/model/{path}'
                response = requests.head(weight_url)
                response.raise_for_status()
                size = int(response.headers.get('content-length', 0))
                print(f"✅ Weight file {path} accessible ({size:,} bytes)")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing model files: {str(e)}")
        return False
    except json.JSONDecodeError:
        print("❌ model.json is not valid JSON!")
        return False
        
    return True

def check_package(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def verify_setup():
    # Check required packages
    required_packages = ['tensorflow', 'tensorflowjs', 'gdown', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        if not check_package(package):
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall them with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    # Check directories
    model_dir = Path(__file__).parent.parent / 'model'
    if not model_dir.exists():
        print(f"❌ Model directory not found at {model_dir}")
        return False
        
    return True

def verify_model_json(model_dir):
    """Verify model.json is valid and properly formatted"""
    model_json_path = Path(model_dir) / 'model.json'
    
    try:
        with open(model_json_path, 'r') as f:
            model_config = json.load(f)
            
        # Verify required fields
        required_fields = ['format', 'generatedBy', 'convertedBy', 'modelTopology', 'weightsManifest']
        for field in required_fields:
            if field not in model_config:
                print(f"❌ model.json missing required field: {field}")
                return False
                
        # Verify weights manifest
        if not model_config['weightsManifest']:
            print("❌ model.json has empty weightsManifest")
            return False
            
        print("✅ model.json verification passed")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ model.json is not valid JSON: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error verifying model.json: {str(e)}")
        return False

def verify_cors_headers():
    """Verify CORS headers are properly set"""
    url = 'https://tdeu.github.io/model-hosting/model/model.json'
    try:
        response = requests.head(url)
        headers = response.headers
        
        required_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Content-Type': 'application/json'
        }
        
        for header, value in required_headers.items():
            if header not in headers:
                print(f"❌ Missing required header: {header}")
                return False
                
        print("✅ CORS headers verification passed")
        return True
        
    except Exception as e:
        print(f"❌ Error checking CORS headers: {str(e)}")
        return False

def main():
    # Local verification
    print("Verifying local model files...")
    if not verify_model_files('model'):
        print("❌ Local verification failed!")
        return False
        
    # Deployment verification
    base_url = 'https://tdeu.github.io/model-hosting'
    if not verify_deployed_model(base_url):
        print("❌ Deployment verification failed!")
        return False
        
    print("\n✨ All verifications passed successfully!")
    return True

if __name__ == "__main__":
    if verify_setup():
        print("✅ Environment setup verified!")
    else:
        print("\n❌ Please fix the above issues before proceeding")
        sys.exit(1)