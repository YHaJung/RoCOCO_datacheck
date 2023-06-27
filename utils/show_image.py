import cv2

import sys, os
root_path = os.getcwd()
sys.path.append(root_path)

from utils.file_processing import load_file

def refine_string(line):
    import re
    line = line.strip(' ').rstrip('\n').rstrip(' \.').lower()
    line = re.sub(r"[,\"'.;?`]", "", line)
    line = line.replace("  ", " ")
    return line

def show_image(origin_line):
    origin_line = refine_string(origin_line)
    img_info_list = load_file('data_check/sub_infos/coco_karpathy_test.json')

    start_idx, end_idx = 0, len(origin_line)
    # start_idx, end_idx = 0, 15
    origin_line_check = origin_line[start_idx:end_idx]
    
    for img_info in img_info_list:
        img_captions = [refine_string(img_cap) for img_cap in img_info['caption']]
        
        img_captions_check = [img_caption[start_idx:end_idx] for img_caption in img_captions]
        if origin_line_check in img_captions_check:
            if start_idx != 0 or end_idx != len(origin_line):
                print([origin_line])
                print(img_captions)
        # if origin_line in img_captions:
            img_path = img_info['image']
            img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
            img = cv2.resize(img, (600, 500)) 
            cv2.namedWindow("window1")   # create a named window
            cv2.imshow("window1", img)            
            cv2.moveWindow("window1", 400, 50)   # Move it to (40, 30)
            cv2.waitKey(0)
            cv2.destroyAllWindows()