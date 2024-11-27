import argparse
from PIL import Image
from api_call import generate_mesh, get_balance


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert multi-view images to a 3D model")
    parser.add_argument("--front_img_path", default="data/front.jpg", type=str, help="Path to the image file")
    parser.add_argument("--left_img_path", default=None, type=str, help="Path to the image file")
    parser.add_argument("--right_img_path", default=None, type=str, help="Path to the image file")
    parser.add_argument("--back_img_path", default="data/back.jpg", type=str, help="Path to the image file")
    parser.add_argument("--output_path", default="results/multiview_left.glb", type=str, help="Path to save the output 3D model")
    parser.add_argument("--refine", default=0, type=int, help="Refine the model (1: True) or not (0: False)")
    args = parser.parse_args()
    
    print("Checking balance")
    get_balance()
    
    if args.left_img_path is not None:
        img_front = Image.open(args.front_img_path)
        img_side = Image.open(args.left_img_path)
        img_back = Image.open(args.back_img_path)
        imgs = [img_front, img_side, img_back]
        response = generate_mesh(mode='multiview-to-3d', image=imgs, side="LEFT", refine=args.refine, save_path=args.output_path)
    
    if args.right_img_path is not None:
        img_front = Image.open(args.front_img_path)
        img_side = Image.open(args.right_img_path)
        img_back = Image.open(args.back_img_path)
        imgs = [img_front, img_side, img_back]
        response = generate_mesh(mode='multiview-to-3d', image=imgs, side="RIGHT", refine=args.refine, save_path=args.output_path)
    