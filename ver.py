from tkinter import *
import fitz
import io
from PIL import Image, ImageTk

canvas = Canvas(Tk(),width=750,height=750)
canvas.pack()

doc = fitz.open('c.pdf')
page = doc[3]

#image = Image.open(pix)
image_list = page.getImageList()
# printing number of images found in this page
if image_list:
    print(f"[+] Found a total of {len(image_list)} images in page {page}")
else:
    print("[!] No images found on page", page)
for image_index, img in enumerate(page.getImageList(), start=1):
    # get the XREF of the image
    xref = img[0]
    smask = img[1] 
    name = img[7]
# extract the image bytes
    base_image = doc.extractImage(xref)
    print ("Name > %s" % name)
    print ("Format > %s" % base_image["cs-name"])
    print ("smask > %i" % base_image["smask"])
    print ("%i height %i width" % (base_image["height"], base_image["width"]))
    image_bytes = base_image["image"]
    # load it to PIL
    img = Image.open(io.BytesIO(image_bytes))
    #Mask (transparency?)
    if (smask > 0):
        base_mask = doc.extractImage(smask)
        mask = base_mask["image"]
        #PIL     
        msk = Image.open(io.BytesIO(mask))
        img0 = Image.new("RGBA", img.size)  # prepare result Image
        img0.paste(img, None, msk)  # fill in base image and mask
        img = img0
    
    # get the image extension 
    image_ext = base_image["ext"]
   
    #pix = fitz.Pixmap(doc, xref)
    #mode = "RGBA" if pix.alpha else "RGB"
    #img = Image.frombytes(mode, image_bytes)
    if ((base_image["width"] > 450 ) or (base_image["height"] > 450)):
        basewidth = 450
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    tkimg = ImageTk.PhotoImage(img)
    canvas.create_image(450,450,image=tkimg)
    input("next")



doc.close()
