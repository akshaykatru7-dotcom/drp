"""Generate fake logos for demo purposes using Pillow."""
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("logos", exist_ok=True)


def make_logo(text, color, bg, filename, size=(200, 200)):
    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40
        )
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=color, font=font)
    img.save(f"logos/{filename}")
    print(f"  OK logos/{filename}")


print("Generating test logos...")
make_logo("PayPal", "#ffffff", "#003087", "official_paypal.png")
make_logo("PayPal", "#ffffff", "#003087", "fake_paypa1_identical.png")
make_logo("PayPal", "#f0f0f0", "#0a2a6a", "fake_paypal_shade.png")
make_logo("PayPal Pro", "#ffffff", "#003087", "fake_paypal_pro.png")
make_logo("PayPal", "#ffe600", "#222222", "fake_paypal_dark.png")
make_logo("Notes", "#ffffff", "#16a34a", "unrelated_notes.png")
print("Done.")
