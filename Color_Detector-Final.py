import cv2
#import numpy as np
import pandas as pd
from gooey import Gooey, GooeyParser

@Gooey(program_name="AML-1214 Color Detector",
       terminal_font_size=10,
       terminal_font_color='red',
       clear_before_run=True,
       program_description='Python TERM Project',
       default_size=(700, 500),
       menu=[{'name': 'Group Member', 'items': [{
           'type': 'AboutDialog',
           'menuTitle': 'Tusker',
           'name': 'AML-1214 Color Detector',
           'description': 'AML-1214 Color Detector - TERM Project',
           'developer': '\nLouie Lachica\nAileen Dino\nVibhav Sahni\nSri Aravind Devavarapu'
       }]
       }])
def parse_args():
    parser = GooeyParser(description="Detect Color on the Selected Image File")
    parser.add_argument('Image_Path', widget="FileChooser")

    return parser.parse_args()
args = parse_args()
img_path=(args.Image_Path)
print(f'Processing Image.....{img_path}\n\nPress ESC to close the Image Window')

# Opening the image file from file chooser
img = cv2.imread(img_path)

# Global Variable for click,  R.G.B values and x,y posistion
clicked = False
r = g = b = xpos = ypos = 0

# Reading color.csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# this function will get x,y coordinates of mouse cursor when double clicked.
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', draw_function)

while (1):

    cv2.imshow("image", img)
    if (clicked):

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()



























