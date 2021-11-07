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

# loop through image set writing pngs
try:
    for i, imageref in enumerate(all_images_set):
        xref = imageref[0]
        smask = imageref[1]
        if smask > 0:
            pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
            mask = fitz.Pixmap(doc.extract_image(smask)["image"])
            if pix0.width == mask.width and pix0.height == mask.height:
                pix = fitz.Pixmap(pix0, mask)
                pix.save(savedir + "output_%s.png" % i)
                print("writing image " + str(i) + "/" + str(len(all_images_set)))
            else:
                print("writing image " + str(i) + "/" + str(len(all_images_set)) + " fucked up, skipping")
        else:
            pix = fitz.Pixmap(doc, xref)
            pix.save(savedir + "output_%s.png" % i)
            print("writing image " + str(i) + "/" + str(len(all_images_set)))
except Exception as pidor:
    with open('error.txt', 'w') as f:
        f.write(str(pidor))
