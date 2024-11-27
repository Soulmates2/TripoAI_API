import os
import argparse
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

from tripo_api.system import TripoAPI
from tripo_api.utils import tensor_to_pil_base64, pil_to_base64


def get_api_key(env_path='.env', key_name='TRIPO_TOKEN'):
    load_dotenv(dotenv_path=env_path)
    return os.environ[key_name]


def get_balance():
    api_key = get_api_key()
    api = TripoAPI(api_key=api_key, timeout=3000)
    result = api.check_balance()
    if result['status'] == 'success':
        print(f"Remain balance: {result['balance']}")
    else:
        raise RuntimeError(f"Failed to get balance info: {result['message']}")


def generate_mesh(mode, prompt=None, image=None, side=None, refine=False, save_path=None):
    api_key = get_api_key()
    print("apiKey:", api_key)
    api = TripoAPI(api_key=api_key, timeout=3000)
    
    if mode == 'text-to-3d':
        if prompt is None or prompt == "":
            raise RuntimeError("Prompt is required")
        print(f"Request Text-to-3D model with prompt: {prompt}")
        result = api.text_to_3d(prompt)

        if result['status'] == 'success':
            print("Model generated successfully")
        else:
            raise RuntimeError(f"Failed to generate mesh: {result['message']}")

    elif mode == 'image-to-3d':
        if image is None:
            raise RuntimeError("Image is required")
        image_data = pil_to_base64(image)
        print(f"Request Image-to-3D model")
        result = api.image_to_3d(image_data)

        if result['status'] == 'success':
            print("Model generated successfully")
        else:
            raise RuntimeError(f"Failed to generate mesh: {result['message']}")
    
    elif mode == "multiview-to-3d":
        if image is None or len(image) != 3:
            raise RuntimeError("3 Images (front, left/right, back) are required")
        if side is None:
            raise RuntimeError("Side LEFT or RIGHT is required")
        image_data = []
        for img in image:
            image_data.append(pil_to_base64(img))
        
        print(f"Request Multiview-to-3D model")
        result = api.multiview_to_3d(image_data, side=side)
        if result['status'] == 'success':
            print("Model generated successfully")
        else:
            raise RuntimeError(f"Failed to generate mesh: {result['message']}")
    
    else:
        raise RuntimeError("Invalid mode. mode: text-to-3d, image-to-3d, multiview_to_3d")
   
    if save_path is not None:
        print(f"Saving the 3D model to {save_path}")
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        
        with open(save_path, "wb") as f:
            f.write(result['model'])

    if refine:
        print(f"Refine the result model from task_id {result['task_id']}")
        refine_result = api.refine_3d(result['task_id'])
        if refine_result['status'] == 'success':
            print("Model refined successfully")
            
            if save_path is not None:
                refine_save_path = save_path.replace(".glb", "_refine.glb")
                print(f"Saving the refine 3D model to {refine_save_path}")

                with open(refine_save_path, "wb") as f:
                    f.write(refine_result['model'])

            return (result['model'], result['task_id'], refine_result['model'], refine_result['task_id'])
        else:
            raise RuntimeError(f"Failed to refine mesh: {result['message']}")

    return (result['model'], result['task_id'])
    
    
    