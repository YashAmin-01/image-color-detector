# Import required libraries
import cv2
import pandas as pd

# Reading the image using opencv
img = cv2.imread("image.jpg")
img = cv2.resize(img, (960,540))

# creating global variables
clicked = False
r = g = b = xpos = ypos = 0

# Reading colors file with csv info
index=["color","color_name","hex","R","G","B"]
colors = pd.read_csv('colors.csv', names=index, header=None)

# function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(colors)):
        d = abs(R- int(colors.loc[i,"R"])) + abs(G- int(colors.loc[i,"G"]))+ abs(B- int(colors.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = colors.loc[i,"color_name"]
    return cname

# function to get x,y coordinates on click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('color_detector')
cv2.setMouseCallback('color_detector',draw_function)

while(True):

    cv2.imshow("color_detector",img)
    if (clicked): 
        cv2.rectangle(img,(20,20), (600,60), (b,g,r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
