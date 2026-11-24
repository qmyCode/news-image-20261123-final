"""Dev-only: write entry-300.png (needs Pillow; not part of the entry)."""
import os
from PIL import Image
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
im = Image.open(os.path.join(d, "entry.png"))
im.resize((300, 300), Image.LANCZOS).save(os.path.join(d, "entry-300.png"))
