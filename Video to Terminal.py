from PIL import Image
import os
import time
import cv2

def convertASCII(image, newSize): #convert pil image to ASCII art
    altText = ""
    gscale = "@%#*+=-:. "
    gscale2 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " 

    image = image.convert('L')
    image.thumbnail((newSize, newSize)) #resize image to same resolution as ASCII art

    imageW, imageH = image.size[0], image.size[1]
    px = image.load()

    for y in range(0, imageH): #read each pixel of the resized image and assign ASCII character respectively
        for x in range(0, imageW):
            pixel = px[x, y]
            altText+=gscale2[int((pixel * 69) / 255)] + ' '
        altText+='\n'

    return altText
        
def convertVideo(videoFile, frameRate, newSize): #convert video to ASCII art, return an array of the art in text
    vidcap = cv2.VideoCapture(videoFile)
    sec = 0
    success, image = getFrame(sec, vidcap) #get the first frame
    arrASCII = []

    while success: #get the following frame with framerate gap
        arrASCII.append(convertASCII(image, newSize))
        sec = sec + frameRate
        sec = round(sec, 2)
        success, image = getFrame(sec, vidcap)

    return arrASCII

def getFrame(sec, vidcap): #get the frame of the video at certain time
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames, image = vidcap.read()
    pilImage = ''
    if hasFrames:
        colorConverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert cv2 image to pil image
        pilImage = Image.fromarray(colorConverted)
    return hasFrames, pilImage

def main():
    while True:
        try:
            file = input('Enter the Video File Path: ')
            if file.startswith('\"') and file.endswith('\"'):
                file = file[1:]
                file = file[:-1]
            vidcap = cv2.VideoCapture(file)
            if not vidcap.isOpened():
                raise NameError()
        except (cv2.error, Exception):
            print('The File is Invalid, Please Try Again: ')
        else:
            break
    
    frameRate = 1 / float(input('Enter the FPS of the ASCII Art (larger will take longer): '))

    newSize = int(input('Enter the ASCII Art Size (larger will take longer): '))

    print('Getting the Video Ready, Please Wait')

    text = convertVideo(file, frameRate, newSize)

    os.system('cls' if os.name == 'nt' else 'clear')

    check = input('Video Ready, Please Press Enter')

    for x in text: #print out the ASCII art with delay
        time.sleep(frameRate)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(x)

main()
