from PIL import Image, ImageDraw, ImageFont


def createImage(text):
    a = text
    font = ImageFont.truetype("arial.ttf", 40)
    if len(a) > 100:
        return False
    if len(a) > 30:
        text = "«" + text + "»"
        for i in range(0, len(a), 30):
            text = text[:i] + "\n" + text[i:]

    if len(a) <= 15:
        image = Image.open('files/jak.jpg')
        drawer = ImageDraw.Draw(image)
        drawer.text((335, 300), text, font=font, fill='black', align='center', anchor="ms")
        image.save('jak_memes/last.jpg')
        return True
    image = Image.open('files/jak.jpg')
    drawer = ImageDraw.Draw(image)
    drawer.text((335, 100), text, font=font, fill='black', align='left', anchor="ms")
    image.save('jak_memes/last.jpg')
    # image.show()
    return True
