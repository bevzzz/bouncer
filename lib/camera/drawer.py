import cv2
import cv2 as cv
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import numpy as np

img_path = "/home/dmytro/pycharm/bouncer/resources/images/bevzzz/bevzzz_20210405131408.jpeg"
# img = cv.imread(img_path)


im = open(img_path, 'rb')

# here's how you convert bytes into cv image
# im.read() produces byte array
img = cv.imdecode(
    np.frombuffer(im.read(), np.uint8), 1
)


height = img.shape[0]
width = img.shape[1]

# draw lines --> (0,0) is the upper-left corner
cv.line(
    img=img,
    pt1=(20, 40),
    pt2=(20, 280),
    color=(0, 0, 255),
    thickness=2
)
cv.line(
    img=img,
    pt1=(220, 40),
    pt2=(220, 280),
    color=(0, 0, 255),
    thickness=2
)
cv.line(
    img=img,
    pt1=(20, 40),
    pt2=(220, 40),
    color=(0, 0, 255),
    thickness=2
)
cv.line(
    img=img,
    pt1=(20, 280),
    pt2=(220, 280),
    color=(0, 0, 255),
    thickness=2
)


pil_image = Image.fromarray(img)

# draw transforms ORIGINAL object - pil_image
draw = ImageDraw.Draw(pil_image)
draw.text(
    xy=(20, 280+5),
    text="bevzzz",
    fill=(0, 0, 255),
    font=ImageFont.load_default()

)

# convert back to that
img = np.asarray(pil_image)


def add_stuff(img, name):

    height = img.shape[0]
    width = img.shape[1]

    # draw lines --> (0,0) is the upper-left corner
    cv.line(
        img=img,
        pt1=(20, 40),
        pt2=(20, height-40),
        color=(0, 0, 255),
        thickness=2
    )
    cv.line(
        img=img,
        pt1=(width-20, 40),
        pt2=(width-20, height-40),
        color=(0, 0, 255),
        thickness=2
    )
    cv.line(
        img=img,
        pt1=(20, 40),
        pt2=(width-20, 40),
        color=(0, 0, 255),
        thickness=2
    )
    cv.line(
        img=img,
        pt1=(20, height-40),
        pt2=(width-20, height-40),
        color=(0, 0, 255),
        thickness=2
    )

    pil_image = Image.fromarray(img)

    # draw transforms ORIGINAL object - pil_image
    draw = ImageDraw.Draw(pil_image)
    draw.text(
        xy=(20, 280 + 5),
        text=name,
        fill=(0, 0, 255),
        font=ImageFont.load_default()

    )

    # convert back to that
    return np.asarray(pil_image)
