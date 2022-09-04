from PIL import Image

def inpImage(arr):
    Image.fromarray(arr).convert("RGB").save("backup.png")