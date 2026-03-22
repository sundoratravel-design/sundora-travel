import re

with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace base64 img with file reference
html = re.sub(
    r'<div class="intro-card" style="padding:0;overflow:hidden;border-radius:12px;">\s*<img src="data:image/jpeg;base64,[^"]*"',
    '<div class="intro-card" style="padding:0;overflow:hidden;border-radius:12px;"><img src="/intro-photo.jpg"',
    html
)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("done")
