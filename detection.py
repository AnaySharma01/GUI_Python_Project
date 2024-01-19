#imports packages
import time
import cv2
import numpy as np

#Masking
def mask_img(img):  # H  S  V
    lower_thr = np.array([0, 0, 0])
    upper_thr = np.array([179, 255, 87])
    img_masked = cv2.inRange(img, lower_thr, upper_thr)
    return img_masked

#Canny Edge Detection
def detect_edges(img):
  img_gre = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(img_gre, (5, 5), 0)
  img_canny = cv2.Canny(blur, 200, 400)
  return img_canny

#Cropping, Region of Interest
def crop_roi(img):
    height = img.shape[0]
    width = img.shape[1]
    # print(height, width)
    mask = np.zeros_like(img)
    cv2.rectangle(mask, (0, height // 2), (width, height), 255, -1)  # -1 -> fill
    roi = cv2.bitwise_and(img, mask)
    return roi

#Hough Transform
def detect_lines(img):
    # function that we use is HoughLinesP
    rho = 1
    theta = np.pi / 180
    min_threshold = 10
    min_line_length = 20
    max_line_gap = 4
    lines = cv2.HoughLinesP(img, rho, theta, min_threshold, np.array([]), min_line_length, max_line_gap)
    return lines
  
# Groups positive slope and negative slope lines, which will define left and right lane markings
def group_lines(img, lines):
    height = img.shape[0]
    width = img.shape[1]
    lane_lines = []
    # No lines found
    if lines is None:
        return lane_lines
    left_lane = []
    right_lane = []
    boundary = 1 / 3
    left_lane_area_width = width * (1 - boundary)
    right_lane_area_width = width * boundary
    for line in lines:
        for x1, y1, x2, y2 in line:
            # skip vertical lines as they have infinite slope
            if x1 == x2:
                continue
            coff = np.polyfit((x1, x2), (y1, y2), 1)
            slope = coff[0]
            intercept = coff[1]
            # positive slope -> right lane marking  \
            #                                       \
            #                                        \
            #                                         \
            if slope > 0:
                # search area check
                if x1 > right_lane_area_width and x2 > right_lane_area_width:
                    right_lane.append((slope, intercept))
            # negative slope -> left lane marking  /
            #                                    /
            #                                   /
            #                                  /
            else:
                if x1 < left_lane_area_width and x2 < left_lane_area_width:
                    left_lane.append((slope, intercept))

    # averaging all the lines in each group to get a single line out of them
    left_avg = np.average(left_lane, axis=0)
    right_avg = np.average(right_lane, axis=0)

    # if got left lane, convert to point form from intercept form
    if len(left_lane) > 0:
        lane_lines.append(line_to_point(img, left_avg))
    if len(right_lane) > 0:
        lane_lines.append((line_to_point(img, right_avg)))
    return lane_lines

# Create points from the lane lines with slop and intercept
def line_to_point(img, line):
    slop = line[0]
    intercept = line[1]
    height = img.shape[0]
    width = img.shape[1]
    y1 = int(height / 2)  # middle
    x1 = int((y1 - intercept) / slop)
    if x1 < 0:
        x1 = 0
    if x1 > width:
        x1 = width
    y2 = int(height)  # bottom
    x2 = int((y2 - intercept) / slop)
    if x2 < 0:
        x2 = 0
    if x2 > width:
        x2 = width
    return [[x1, y1, x2, y2]]
