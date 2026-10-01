from PIL import Image, ImageDraw

# Create a simple portrait image (neutral face)
img = Image.new("RGB", (400, 450), color="#2A1A3E")
draw = ImageDraw.Draw(img)

# Face oval
draw.ellipse([100, 100, 300, 350], fill="#E6C2A0", outline="#4A2A00", width=3)
# Eyes
draw.ellipse([150, 180, 175, 200], fill="#3E2723")
draw.ellipse([225, 180, 250, 200], fill="#3E2723")
# Mouth / smile
draw.arc([175, 250, 225, 290], start=0, end=180, fill="#C62828", width=3)
# Hair
draw.ellipse([90, 80, 310, 150], fill="#1A1A1A")

img.save("test_portrait.png")
print("Saved test_portrait.png")
