# 3D Generation via Tripo API


## Environment setup
```
pip install requirements.txt
```

You should set your personal tokens in the `.env` file like below:
```
TRIPO_TOKEN={your_tripo_api_token}
```

## Text to 3D
```
python text_to_3d.py --text_prompt {$TEXT} --output_path {$OUTPUT_PATH} --refine 0
python text_to_3d.py --text_prompt "A red nike sneaker" --output_path results/text.glb --refine 0
```

## Single Image to 3D (need a front view image)
```
python image_to_3d.py --img_path {$IMAGE_PATH} --output_path {$OUTPUT_PATH} --refine 0
python image_to_3d.py --img_path data/front.jpg --output_path results/front.glb --refine 0
```

## Multi-View Images to 3D (need 3 images)
Front, Left, Back images
```
python multiview_to_3d.py --front_img_path {$FRONT_IMAGE_PATH} --left_img_path {$LEFT_IMAGE_PATH} --back_img_path {$BACK_IMAGE_PATH} --output_path {$OUTPUT_PATH} --refine 0
python multiview_to_3d.py --front_img_path data/front.jpg --left_img_path data/left.jpg --back_img_path data/back.jpg --output_path results/multiview_left.glb --refine 0
```
Front, Right, Back images
```
python multiview_to_3d.py --front_img_path {$FRONT_IMAGE_PATH} --right_img_path {$RIGHT_IMAGE_PATH} --back_img_path {$BACK_IMAGE_PATH} --output_path {$OUTPUT_PATH} --refine 0
python multiview_to_3d.py --front_img_path data/front.jpg --right_img_path data/right.jpg --back_img_path data/back.jpg --output_path results/multiview_right.glb --refine 0
```
