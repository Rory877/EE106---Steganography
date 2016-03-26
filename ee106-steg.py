from PIL import Image
import sys


#Take a message from the user and convert it to a binary string
def stringToBinary(message):
    string=""
    for ch in message:
        binary= bin(ord(ch))[2::]
        if len(binary)<7:
            binary="0"+binary
        if len(binary)<8:
            binary="0"+binary
        string=string+binary
    return string

#Take a binary string and convert it to the original message
def binaryToString(binary):
    message=""
    binChunks = [binary[8*i:8*(i+1)] for i in range(len(binary)//8)]
    for i in binChunks:
        ch=chr(int(i,2))
        message=message+ch
    print(message)
    

#Main hide function
def hide(image, message):    
    im = Image.open(image)
    binary = stringToBinary(message)
    
#Check the message will fit
    imsize = im.height * im.width * 3
    msize = len(message) * 8
    if imsize < msize:
        print("Error - message is too large")
        sys.exit()

#Check for correct format
    if im.mode == 'RGBA' or 'RGB':
        im = im.convert("RGBA")
    else:
        print("Error - image is not in the correct format")
        sys.exit()

    for h in range(im.height):
            for w in range(im.width):
                    (r, g, b, a) = im.getpixel((w, h))
                    newpix = im.putpixel((w, h), (r + b0, g + b1, b + b2))
                    newim = im.save('steg.png', 'PNG')
                    #Where b0, b1, b2 are the sequence of bits to be written


def extract(image):
    im = Image.open(image)

    for h in range(im.height):
        for w in range(im.width):
            (r, g, b, a) = im.getpixel((w, h))
            print([int(bin(r))[2::] & 1, int(bin(g))[2::] & 1, int(bin(b))[2::] & 1)

            

###  MAIN  ###

if __name__ == "__main__":
