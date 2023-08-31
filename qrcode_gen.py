import time
from io import BytesIO
import segno
from segno import helpers
from PIL import Image
from urllib.request import urlopen


t1 = time.perf_counter()
qrcode = segno.make_qr("Welcome", error="H")
print(qrcode.designator)
t = time.perf_counter() - t1
print(type(qrcode))
print(f"{t:0.2f}s")

# Save the image to a file
qrcode.save(
    "examples/welcome.png",
    scale=10,
    dark="#0000ffcc",
    data_dark="steelblue",
    timing_dark="yellow",
)
print(type(qrcode.png_data_uri()))

t1 = time.perf_counter()
qrcode = helpers.make_wifi(ssid="MyWifi", password="1234567890", security="WPA")
print(qrcode.designator)

qrcode.save("examples/wifi-access.png", scale=10)
t = time.perf_counter() - t1
print(f"{t:0.2f}s")


qrcode = helpers.make_mecard(
    name="Shittu Olumide", email="me@example.com", phone="+123456789"
)
qrcode.designator
"3-L"
# Some params accept multiple values, like email, phone, url
qrcode = helpers.make_mecard(
    name="Shittu Olumide",
    email=("me@example.com", "email@example.com"),
    url=["http://www.example.com", "https://example.come/~olu"],
)
qrcode.save("examples/mycontact.png", scale=5)

t1 = time.perf_counter()
qrcode = segno.make("Yellow Submarine", error="h")
img = qrcode.to_pil(
    scale=4, dark="darkred", data_dark="darkorange", data_light="yellow"
)
print(time.perf_counter() - t1)
print(type(img))
img.save("./examples/yellow-submarine.png")


out = BytesIO()
# Nothing special here, let Segno generate the QR code and save it as PNG in a buffer
segno.make("Blackbird singing in the dead of night", error="h").save(
    out, scale=10, kind="png"
)
out.seek(0)  # Important to let Pillow load the PNG

img = Image.open(out)
img = img.convert("RGB")  # Ensure colors for the output
img_width, img_height = img.size

logo_max_size = img_height // 3  # May use a fixed value as well
logo_img = Image.open("./blackbird.jpg")  # The logo
# Resize the logo to logo_max_size
logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

# Calculate the center of the QR code
box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
img.paste(logo_img, box)
img.save("qrcode_with_logo.png")


############################################


qrcode = segno.make("Ringo Starr", error="h")
url = "https://media.giphy.com/media/HNo1tVKdFaoco/giphy.gif"
bg_file = urlopen(url)
qrcode.to_artistic(background=bg_file, target="ringo.gif", scale=10)
