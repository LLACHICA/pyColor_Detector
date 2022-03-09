import cv2
import pandas as pd
from gooey import Gooey, GooeyParser

# Setup Gooey as a Front-End interface for the Color-Detection Apps
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
# Using GooeyParser to parse the path of the Image File selected by the user
def parse_args():
    parser = GooeyParser(description="Detect Color on the Selected Image File")
    parser.add_argument('Image_Path', widget="FileChooser")
    return parser.parse_args()

args = parse_args()
img_path=(args.Image_Path)
print(f'Processing Image.....{img_path}\n\nPress ESC to close the Image Window')

# Opening the image file from file chooser
img = cv2.imread(img_path)

# Setting Global Variable for click,  R.G.B values and x,y posistion
clicked = False
r = g = b = xpos = ypos = 0

# Open color.csv file and setting column names using pandas
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# Function to get the matching color and calculate the distance from all color
def get_ColorN(R, G, B):
    min = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d <= min):
            min = d
            cname = csv.loc[i, "color_name"]
    return cname


# Function to get the rgb values of the pixel when we double clicked and the (x,y) coordinates of the mouse position
def Func_Draw(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        print(f'Clicked R.G.B values {img[y, x]}')
        b = int(b)
        g = int(g)
        r = int(r)
# Open the image in  the new window
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# cv2 capture mouse click event
cv2.setMouseCallback('image', Func_Draw)

while True:

    cv2.imshow("image", img)
    if (clicked):

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_ColorN(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()



























