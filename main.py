import os
import sys
import fitz

# get file name from dropped .pdf
fname = sys.argv[1]
doc = fitz.open(fname)

# make subfolder based on input file name
fname_stripped = fname[:-4]
if not os.path.exists(fname_stripped):
    os.mkdir(fname_stripped)
savedir = fname_stripped + "\\"

# list to throw all the image references in
all_images = []

# fill the above list regardless of dupes
for i in range(len(doc)):
    pagelist = doc.getPageImageList(i)
    all_images.extend(pagelist)

# create image set, killin dupes
all_images_set = set(all_images)

# loop thru images set saving em
try:
    for i, item in enumerate(all_images_set): # xref [0] smask [1]
        info = []

        # apply smask if necessary
        if item[1] > 0:
            pixmap = fitz.Pixmap(doc.extract_image(item[0])["image"])
            mask = fitz.Pixmap(doc.extract_image(item[1])["image"])
            # check if smask of proper size
            if mask.width == pixmap.width and mask.height == pixmap.height:
                pixmap = fitz.Pixmap(pixmap, mask)
                info.append("has alpha")
            else:
                info.append("size mismatch -> writing as opaque")

        # make pixmap w/o smask
        else:
            pixmap = fitz.Pixmap(doc, item[0])

        # convert to srgb if necessary
        if hasattr(pixmap.colorspace, 'name') and pixmap.colorspace.name not in (fitz.csGRAY.name, fitz.csRGB.name):
            pixmap = fitz.Pixmap(fitz.csRGB, pixmap)
            info.append("converted to RGB")

        # write png
        pixmap.save(savedir + "output_%s.png" % i)
        print("writing image " + str(i) + "/" + str(len(all_images_set)), end=' ')
        print(*info, sep=", ")

except Exception as pidor:
    with open('error.txt', 'w') as f:
        f.write(str(pidor))
