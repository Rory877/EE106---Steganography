from PIL import Image
import sys
import argparse


# Writes a bit to the LSB of a byte
def setbit(oldbyte, bit):
    if bit == 1:
       if oldbyte % 2 == 0:
            return int(oldbyte + 1)
       else:
            return int(oldbyte)
    elif bit == 0:
        return int(oldbyte & 0b11111110)

#Take a message from the user and convert it to a binary string
def stringToBinary(message):
    string = ""
    for ch in message:
        binary = bin(ord(ch))[2::]
        if len(binary) < 7:
            binary = "0" + binary
        if len(binary) < 8:
            binary = "0" + binary
        string = string + binary
    return string

#Take a binary string and convert it to the original message
def binaryToString(binary):
    message = ""
    binChunks = [binary[8*i:8*(i+1)] for i in range(len(binary)//8)]
    for i in binChunks:
        ch = chr(int(i,2))
        message = message + ch
    print(message)
    

#Main hide function
def store(image, message):    
    im = Image.open(image)
    binary = str(stringToBinary(message))
    
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

#Writes binary sequence to image
    c = 0
    for h in range(im.height):
            for w in range(im.width):
                    (r, g, b, a) = im.getpixel((w, h))
                    nr = setbit(r, binary[c:c+1:])
                    ng = setbit(g, binary[c+1:c+2:])
                    nb = setbit(b, binary[c+2:c+3:])
                    c = c + 3

                    im.putpixel((w, h), (nr, ng, nb))
    newim = im.save(image + '-steg.png', 'PNG')


#Main extract function
def retrieve(image):
    im = Image.open(image)
    binary = []


    for h in range(im.height):
        for w in range(im.width):
            (r, g, b, a) = im.getpixel((w, h))
            binary.append(r & 1)
            binary.append(g & 1)
            binary.append(b & 1)           

    message = binaryToString(binary)
    return message
            

###  MAIN  ###

def main():
    
    parser = argparse.ArgumentParser(description = "Least Significant Bit Steganography")
    parser.add_argument('--store', '-s', dest = 'store', help = 'store a message in a PNG image file')
    parser.add_argument('--retrieve', '-r', dest = 'retrieve', help = 'retrieve a hidden message from a PNG image')
    opt = parser.parse_args()

    if opt.store != None:
        message = input("Enter a message to store: ")
        store(opt.store, message)
    elif opt.retrieve != None:
        retrieve(opt.retrieve)
    else:
        sys.exit()

if __name__ == '__main__':
    main()
