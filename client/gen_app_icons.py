"""
@ai-generated true 2026-06-18
临时脚本: 生成 APP 应用图标全套
覆盖 Android 4 个尺寸 + iOS 全套
"""
import os
from PIL import Image, ImageDraw, ImageFont

GOLD = (212, 168, 83, 255)
BG_TOP = (12, 12, 26, 255)
BG_BOT = (32, 26, 56, 255)


def make_gradient(size: int) -> Image.Image:
    """生成竖向渐变背景"""
    img = Image.new("RGBA", (size, size), BG_TOP)
    pixels = img.load()
    for y in range(size):
        ratio = y / size
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOT[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOT[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOT[2] * ratio)
        for x in range(size):
            pixels[x, y] = (r, g, b, 255)
    return img


def round_corner(img: Image.Image, radius_ratio: float = 0.22) -> Image.Image:
    """给图标加圆角"""
    size = img.size[0]
    radius = int(size * radius_ratio)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size, size), radius=radius, fill=255)
    img.putalpha(mask)
    return img


def draw_icon(size: int) -> Image.Image:
    """生成 size×size 的应用图标"""
    img = make_gradient(size)
    d = ImageDraw.Draw(img)

    # 字体优先 Georgia（macOS/Windows 都有），否则降级
    font = None
    candidates = [
        "C:/Windows/Fonts/georgiai.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/timesi.ttf",
        "/System/Library/Fonts/Georgia.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            font = ImageFont.truetype(path, int(size * 0.7))
            break
    if font is None:
        font = ImageFont.load_default()

    # 居中绘制 ℞
    text = "\u211E"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - int(size * 0.04)
    d.text((x, y), text, fill=GOLD, font=font)

    # 圆角
    return round_corner(img, 0.22)


# 各端尺寸需求
SIZES = {
    "icon-20.png": 20,
    "icon-29.png": 29,
    "icon-40.png": 40,
    "icon-58.png": 58,
    "icon-60.png": 60,
    "icon-72.png": 72,
    "icon-76.png": 76,
    "icon-80.png": 80,
    "icon-87.png": 87,
    "icon-96.png": 96,
    "icon-120.png": 120,
    "icon-144.png": 144,
    "icon-152.png": 152,
    "icon-167.png": 167,
    "icon-180.png": 180,
    "icon-192.png": 192,
    "icon-1024.png": 1024,
}


if __name__ == "__main__":
    out_dir = os.path.join(
        os.path.dirname(__file__), "src", "static", "app-icon"
    )
    os.makedirs(out_dir, exist_ok=True)
    for name, size in SIZES.items():
        img = draw_icon(size)
        path = os.path.join(out_dir, name)
        img.save(path, "PNG")
        print(f"[ok] {name} ({size}x{size})")
    print(f"done: {len(SIZES)} icons")
