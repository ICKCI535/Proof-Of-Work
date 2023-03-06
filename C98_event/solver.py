import cv2 as cv
import numpy as np
import os

#need to work: distance from top_left of first number to last number, 91x2

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def process_image(number, captcha_img_gray, template, threshold):
    number = str(number)
    result = cv.matchTemplate(captcha_img_gray, template, cv.TM_CCOEFF_NORMED)
    # get the best match posiion (val = whitest point)
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    locations = sorted(locations)

    number_matched_dict[number] = []
    object_width = template.shape[1]
    object_height = template.shape[0]
    #
    for loc in locations:
        if loc[1] not in range(30,50):
            continue
        confidence = result[loc[1]][loc[0]]
        loc = list(loc)
        loc.append(confidence)
        loc = tuple(loc)
        break_code = False
        for item in number_matched_dict.values(): # not adding duplicates
            for loc1 in item:
                if loc == loc1:
                    break_code = True
                    break
        if break_code == True:
            continue
        rect = [int(loc[0]), int(loc[1]), object_width, object_height]
        rects = {}
        rects["rect"] = rect
        rects["confidence"] = confidence
        matches.append(rects)
        number_matched_dict[number].append(loc)
        # execute
    return

def draw_image(rectangle, confidence):
    global captcha_img
    line_color = (0, 255, 0)
    line_type = cv.LINE_4
    # 
    x, y, w, h = rectangle
    center_x = x + int(w/2)
    center_y = y + int(h/2)
    top_left = (x, y)
    bottom_right = (x + w, y + h)
    # Draw the box
    cv.putText(img=captcha_img, text=str(confidence)[0:4], org=(x, y-5), fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.5, color=(0,0,255), thickness=1)
    cv.rectangle(captcha_img, top_left, bottom_right, color=line_color,lineType=line_type, thickness=2)

def sort_number(number_matched_dict, template):
    final_number = ["x", "x", "x", "x"]
    position_dict = {0: {'loc': (), 'confidence': 0}, 1: {'loc': (), 'confidence': 0}, 2: {'loc': (), 'confidence': 0}, 3: {'loc': (), 'confidence': 0}}
    for key in number_matched_dict: # key
        for loc in number_matched_dict[key]:  # loc = (125, 39, 0.5451897382736206)
            number_index = get_number_index(loc[0])
            if number_index == -1:
                continue
            if loc[2] > position_dict[number_index]['confidence']:
                position_dict[number_index]['loc'] = (loc[0], loc[1], template.shape[1], template.shape[0])
                position_dict[number_index]['confidence'] = loc[2]
                final_number[number_index] = key

    final_number = ''.join(final_number)
    return {'final_number': final_number, 'position_dict': position_dict}

def get_number_index(x):
    if x >= 45 and x <= 65:
        return 0
    elif x >= 75 and x <= 95:
        return 1
    elif x >= 110 and x <= 130:
        return 2
    elif x >= 145 and x <= 165:
        return 3
    else:
        return -1

def binarize_image(im_gray):
    (thresh, im_bw) = cv.threshold(im_gray, 85, 255, cv.THRESH_BINARY)
    im_bw = cv.threshold(im_gray, thresh, 255, cv.THRESH_BINARY)[1]
    return im_bw

def solve(file_name, thresh_hold=0.77):
    global captcha_img
    global matches
    global number_matched_dict

    matches = []
    number_matched_dict = {}

    for i in range(0, 10):
        template = cv.imread(f"captcha_number/{i}.png", cv.IMREAD_GRAYSCALE)
        captcha_img = cv.imread(f"captcha/{file_name}.png", cv.IMREAD_UNCHANGED)
        captcha_img_gray = cv.imread(f"captcha/{file_name}.png", cv.IMREAD_GRAYSCALE)
        process_image(i, captcha_img_gray, template, thresh_hold)
    
    result = sort_number(number_matched_dict, template)
    return result

def main(file_name):
    result = solve(file_name=file_name, thresh_hold=0.4)
    final_number = result['final_number']
    for item in result['position_dict'].values():
        if not item['loc']:
            continue
    return final_number

# if __name__ == "__main__":
#     for i in range(17,10001):
#         print(i)
#         result = solve(file_name=i, thresh_hold=0.47)
#         final_number = result['final_number']
#         for item in result['position_dict'].values():
#             if not item['loc']:
#                 continue
#             draw_image(item['loc'], item['confidence'])
#         print(number_matched_dict)
#         print(final_number)
#         cv.imshow('Matches', captcha_img)
#         cv.waitKey(0)

# main("nauc.omxog62.683.8.38@gmail.com")