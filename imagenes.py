import fitz
import io, os
from PIL import Image


def extract_image(doc, page):
    ret_names = []
    image_list = page.getImageList()
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page.number}")
    else:
        print("[!] No images found on page", page)
    for image_index, img in enumerate(page.getImageList(), start=1):
        # get the XREF of the image
        xref = img[0]
        smask = img[1] 
        name = img[7].encode('UTF-8')
    # extract the image bytes
        base_image = doc.extractImage(xref)
        img_h = base_image["height"]
        img_w = base_image["width"]
        #remove pictures if aspect ratio > 3
        if not( (img_h//img_w > 3) or (img_w//img_h >3) or (img_h < 200) or (img_w < 200)):
            print ("Name > %s" % name)
            print ("Format > %s" % base_image["cs-name"])
            print ("smask > %i" % base_image["smask"])
            print ("%i height %i width" % (img_h, img_w))
             
            image_ext = base_image["ext"]
            image_bytes = base_image["image"]
            # load it to PIL
            img = Image.open(io.BytesIO(image_bytes))

            # if theres a Mask (transparency?)
            if (smask > 0):
                base_mask = doc.extractImage(smask)
                mask = base_mask["image"]
                #PIL     
                msk = Image.open(io.BytesIO(mask))
                img0 = Image.new("RGBA", img.size)  # prepare result Image
                img0.paste(img, None, msk)  # fill in base image and mask
                img = img0
            # pasted from mupdf example : special case: /ColorSpace definition exists
            # to be sure, we convert these cases to RGB PNG images
            elif "/ColorSpace" in doc.xref_object(xref, compressed=True):
                pix1 = fitz.Pixmap(doc, xref)
                img = fitz.Pixmap(fitz.csRGB, pix1)
                # resize if too big  
                if ((img_w > 450 ) or (img_h > 450)):
                    mode = "RGB"
                    img = Image.frombytes(mode, [img.width, img.height], img.samples)
                    basewidth = 450
                    wpercent = (basewidth/float(img_w))
                    hsize = int((float(img_h)*float(wpercent)))
                    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                
            path = "images"
            image_name = str(name.decode('utf-8'))+ "_" + str(page.number) + "_" + str(img_h) + "_" + str(img_w) + ".png"
            ret_names.append(image_name)
            img.save(os.path.join(path,image_name))        
            
        #    doc.close()
    return ret_names

docu = fitz.open('c.pdf')
doc_pages = docu.page_count
for page in range(0,doc_pages):
    page_to = docu[page]
    name_i = extract_image(docu, page_to)
#print (name_i)
docu.close()
