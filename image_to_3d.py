import argparse
from PIL import Image
from api_call import generate_mesh, get_balance


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a single image to a 3D model")
    parser.add_argument("--img_path", default="data/front.jpg", type=str, help="Path to the image file")
    parser.add_argument("--output_path", default="results/front.glb", type=str, help="Path to save the output 3D model")
    parser.add_argument("--refine", default=0, type=int, help="Refine the model (1: True) or not (0: False)")
    args = parser.parse_args()
    
    print("Checking balance")
    get_balance()
    
    img = Image.open(args.img_path)
    response = generate_mesh(mode='image-to-3d', image=img, refine=args.refine, save_path=args.output_path)
    
