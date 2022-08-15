import argparse
import json
import os
import time
import cv2
import numpy as np

# pose connection
pose_pairs = [
    [0, 1], [0, 15], [0, 14],[15, 17],[14, 16],
    [1, 2],[2, 3],[3, 4],
    [1, 5],[5, 6],[6, 7],
    [1, 8],[8, 9], [9, 10],
    [1,11],[11, 12], [12, 13]
]

# all white
pose_colors = [
    (255,255,255),(255,255,255),(255,255,255),(255,255,255),
    (255,255,255),(255,255,255),(255,255,255),(255,255,255),
    (255,255,255),(255,255,255),(255,255,255),(255,255,255),
    (255,255,255),(255,255,255),(255,255,255),(255,255,255),
    (255,255,255)
]


def handle_json(jsonfile):
    print('handling json {}'.format(jsonfile))
    with open(jsonfile, 'r') as f:
        data = json.load(f)

    for f in data['data']:
        frame_index = f.get('frame_index')
        print('frame index is ',f.get('frame_index'))
        middle = ','.join(str(i) for i in f['skeleton'])
        split = eval(middle)
        for count in range(300):
            if frame_index == count:
                #key point and score
                kpt_origin = np.array(split['pose']).reshape((18, 2))
                print(split['pose'])
                #i made a black background here ,so the multiplier here is also 500
                kpt = kpt_origin * 500
                score = np.array(split['score']).reshape((18, 1))
                #load the black background
                img = cv2.imread('black500_500.jpg')
                for p in pose_pairs:
                    pt1 = tuple(list(map(int, kpt[p[0], 0:2])))
                    c1 = score[p[0], 0]
                    pt2 = tuple(list(map(int, kpt[p[1], 0:2])))
                    c2 = score[p[1], 0]
                    #print the link between key points and the scores
                    print('== {}, {}, {}, {} =='.format(pt1, c1, pt2, c2))
                    if c1 == 0.0 or c2 == 0.0:
                        continue
                    color = tuple(list(map(int, pose_colors[p[0]])))
                    img = cv2.line(img, pt1, pt2, color, thickness=4)
                    img = cv2.circle(img, pt1, 4, color, thickness=-1, lineType=8, shift=0)
                    img = cv2.circle(img, pt2, 4, color, thickness=-1, lineType=8, shift=0)
                if not os.path.exists('ske_results'):
                    os.makedirs('ske_results')
                # save the imgs in some different ways
                #cv2.imwrite('ske_results/{}.jpg'.format(jsonfile.split("\\")[-1][0:-5]), img)
                a = time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime())
                f = str(frame_index)
                print("the output is ske_results/frame"+ f +".jpg")
                cv2.imwrite('ske_results/frame'+ f + '.jpg', img)
            count = count + 1
        
if __name__ == '__main__':
    #just point to the json file you need, or using the parser below for the whole dir processing
    handle_json('1.json')

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str,
                        default='.', help='keypoints json directory')
    opt = parser.parse_args()
    '''
    #change json file directory 
    #for jsonfile in os.listdir('jsons'):
        #if jsonfile.endswith('.json'):
            #handle_json(os.path.join('jsons', jsonfile))
