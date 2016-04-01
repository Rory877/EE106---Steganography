from PIL import Image
import sys
import argparse


#Writes a bit to the LSB of a byte
def setbit(oldbyte, bit):
    if bit == 1:
        if oldbyte % 2 == 0:
            return int(oldbyte + 1)
        else:
            return int(oldbyte)
    elif bit == 0:
        return int(oldbyte & 0b11111110)
    else:
        print("Error - invalid bit")
        sys.exit()

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

    while(len(binary)%3):
        binary += '0'

    binlength = len(binary)
    c = 0

#Writes binary sequence to image
    for h in range(im.height):
            for w in range(im.width):
                    (r, g, b, a) = im.getpixel((w, h))
                    if c < len(binary):
                        r = setbit(r, int(binary[c]))
                        g = setbit(g, int(binary[c + 1]))
                        b = setbit(b, int(binary[c + 2]))
                        c = c + 3

                    im.putpixel((w, h), (r, g, b, a))
    newim = im.save('steg.png', 'PNG')
    print(binlength)


#Main retrieve function
def retrieve(image, binlength):
    im = Image.open(image)
    binary = ''
    c = 0

    for h in range(im.height):
        for w in range(im.width):
            (r, g, b, a) = im.getpixel((w, h))
            if c < int(binlength):
                binary += str(r & 1)
                binary += str(g & 1)
                binary += str(b & 1)
                c = c + 3           

    message = binaryToString(binary)
    return message
            

###  MAIN  ###

def main():
    
    parser = argparse.ArgumentParser(description = "Least Significant Bit Steganography")
    parser.add_argument('-s', '--store', metavar = '<image file>', dest = 'store', help = 'store a message in a PNG image file')
    parser.add_argument('-r', '--retrieve', metavar = '<image file>', dest = 'retrieve', help = 'retrieve a hidden message from a PNG image')
    args = parser.parse_args()

    if args.store:
        message = input("Enter a message to store: ")
        store(args.store, message)
    elif args.retrieve:
        binlength = input("How long is the binary sequence?: ")
        retrieve(args.retrieve, binlength)
    else:
        sys.exit()

if __name__ == '__main__':
    main()
