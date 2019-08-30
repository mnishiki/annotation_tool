import glob
import os
import yaml
import cv2
import argparse
import json
import shutil 

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', help='読み込むフォルダ名')
parser.add_argument('--output_dir', default='output',help='出力フォルダ名')
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir
annotation_filepath = 'annotation.yml'
config_filepath = 'config.yml'
show_font = cv2.FONT_HERSHEY_SIMPLEX

files = glob.glob(input_dir + '/*.JPG')

with open(config_filepath, "r") as f:
    key_map = yaml.load(f)

anno_dict = {}
if os.path.exists(annotation_filepath):
    with open(annotation_filepath,"rb") as f:
        anno_dict = yaml.load(f)

index = 0 #起動時に表示するファイルのインデックス

while True:
    img_path = files[index]
    org_img = cv2.imread(img_path)
    height, width = org_img.shape[:2]

    if img_path in anno_dict:
        show_img = cv2.putText(org_img, anno_dict[img_path], (width-70,height-20), show_font, 1,(0,0,255),2,cv2.LINE_AA)
    else:
        show_img = org_img.copy()

    cv2.imshow('image', show_img)

    key = cv2.waitKey(0)

    if key == ord('p'):# previous image
        index = index - 1 if index > 0 else index

    if key == ord('b'):# next image
        index = index + 1 if index < len(files) -1 else index

    if chr(key) in key_map:
        anno_code = key_map[chr(key)]
        anno_dict[img_path] = anno_code

    if key == ord('s'): # save
        with open(annotation_filepath, "w") as f:
            f.write(yaml.dump(anno_dict, default_flow_style=False))

    if key == ord('e'): # export
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        
        for img_path, ann_code in anno_dict.items():
            image_basename = os.path.basename(img_path)
            org_name, ext = os.path.splitext(image_basename)
            output_name = org_name + '_' + ann_code + ext
            output_path = os.path.join(output_dir, output_name)
            shutil.copy2(img_path, output_path)

    if key == 27:
        cv2.destroyAllWindows()
        break