import re

with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('src="/intro-photo.jpg"', 'src="/intro-photo2.jpg"')

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("done")
