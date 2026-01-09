# make_cta_gif.py
# Generates a looping "Like / Share / Subscribe" animation GIF using Pillow only.

from PIL import Image, ImageDraw, ImageFont
import math
import os

# -------------------------
# Config
# -------------------------
W, H = 800, 450
BG = (18, 18, 18)          # background
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (24, 119, 242)
GRAY = (33, 33, 33)

FPS = 20
DURATION_SEC = 3.0
N_FRAMES = int(FPS * DURATION_SEC)

# Try to load a bold TTF font, fallback to default
def get_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "DejaVuSans-Bold.ttf",
        "arialbd.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except:
                pass
    return ImageFont.load_default()

# -------------------------
# Easing helpers
# -------------------------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out_cubic(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3

def ease_in_out_sine(t):
    t = clamp(t)
    return 0.5 * (1 - math.cos(math.pi * t))

def ease_out_back(t, s=1.70158):
    t = clamp(t)
    return 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2

def triangle(t):
    # 0->1->0 over t in [0,1]
    t = clamp(t)
    return 1 - abs(2 * t - 1)

# -------------------------
# Drawing helpers
# -------------------------
def draw_centered_text(draw, xy, text, font, fill):
    w, h = draw.textlength(text, font=font), font.size
    x, y = xy
    draw.text((x - w / 2, y - h / 2), text, font=font, fill=fill)

def rounded_rect(draw, bbox, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def make_layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def paste_with_alpha(base, layer, alpha=1.0):
    if alpha >= 1.0:
        base.alpha_composite(layer)
    else:
        # Reduce layer alpha globally
        l = layer.copy()
        a = l.split()[-1].point(lambda p: int(p * alpha))
        l.putalpha(a)
        base.alpha_composite(l)

# -------------------------
# Icons
# -------------------------
def draw_bell_icon(size, color=WHITE, angle_deg=0):
    # Simple bell: dome + body + clapper
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Dome
    d.pieslice([s*0.15, s*0.05, s*0.85, s*0.75], start=200, end=-20, fill=color)
    # Body
    d.rectangle([s*0.25, s*0.38, s*0.75, s*0.78], fill=color)
    # Clapper
    d.ellipse([s*0.45, s*0.75, s*0.55, s*0.88], fill=color)
    if angle_deg != 0:
        img = img.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    return img

def draw_share_icon(size, color=WHITE, angle_deg=0):
    # Three dots connected by two lines
    s = size
    pad = int(s * 0.15)
    points = [
        (pad, s // 2),
        (s // 2, pad),
        (s - pad, s // 2),
    ]
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Lines
    d.line([points[0], points[1]], fill=color, width=max(2, s // 20))
    d.line([points[1], points[2]], fill=color, width=max(2, s // 20))
    # Dots
    r = max(3, s // 10)
    for (x, y) in points:
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    if angle_deg != 0:
        img = img.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    return img

def draw_like_icon(size, color=WHITE):
    # Simple "thumb" silhouette using rectangles and a rounded tip
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Palm
    d.rectangle([s*0.30, s*0.35, s*0.80, s*0.85], fill=color)
    # Thumb
    d.rectangle([s*0.20, s*0.40, s*0.35, s*0.60], fill=color)
    # Rounded tip
    d.ellipse([s*0.70, s*0.25, s*0.95, s*0.55], fill=color)
    return img

# -------------------------
# Elements
# -------------------------
def draw_subscribe(layer, cx, cy, scale=1.0, bell_angle=0, click_ripple=0.0):
    d = ImageDraw.Draw(layer)
    btn_w, btn_h = int(260 * scale), int(64 * scale)
    rect = [cx - btn_w // 2, cy - btn_h // 2, cx + btn_w // 2, cy + btn_h // 2]
    rounded_rect(d, rect, radius=int(16 * scale), fill=RED)
    # Text
    font = get_font(int(28 * scale))
    draw_centered_text(d, (cx - btn_w * 0.1, cy), "SUBSCRIBE", font, WHITE)
    # Bell
    bell_size = int(32 * scale)
    bell = draw_bell_icon(bell_size, WHITE, angle_deg=bell_angle)
    bx = int(cx + btn_w * 0.35 - bell.width // 2)
    by = int(cy - bell.height // 2)
    layer.alpha_composite(bell, dest=(bx, by))
    # Click ripple (white ring expanding)
    if click_ripple > 0:
        r = int(20 * scale * (1 + 1.5 * click_ripple))
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(ring)
        alpha = int(180 * (1 - click_ripple))
        for w in range(3):
            dr.ellipse([cx - r - w, cy - r - w, cx + r + w, cy + r + w], outline=(255, 255, 255, alpha), width=2)
        layer.alpha_composite(ring)

def draw_like(layer, cx, cy, t_bounce=1.0):
    # Bounce effect is applied via y-offset before calling this
    icon_size = 56
    icon = draw_like_icon(icon_size, WHITE)
    layer.alpha_composite(icon, dest=(int(cx - icon.width // 2), int(cy - icon.height // 2)))
    # Label
    d = ImageDraw.Draw(layer)
    font = get_font(18)
    draw_centered_text(d, (cx, cy + 45), "LIKE", font, WHITE)

def draw_share(layer, cx, cy, angle_deg=0):
    icon_size = 56
    icon = draw_share_icon(icon_size, WHITE, angle_deg=angle_deg)
    layer.alpha_composite(icon, dest=(int(cx - icon.width // 2), int(cy - icon.height // 2)))
    # Label
    d = ImageDraw.Draw(layer)
    font = get_font(18)
    draw_centered_text(d, (cx, cy + 45), "SHARE", font, WHITE)
def draw_glow(layer, centers, color=(255, 255, 255), intensity=1.0):
    # Simple soft glow by drawing multiple translucent circles
    for (cx, cy) in centers:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dg = ImageDraw.Draw(glow)
        max_r = 110
        steps = 6
        for i in range(steps):
            t = i / (steps - 1)
            r = int(lerp(30, max_r, t))
            a = int(lerp(120, 0, t) * intensity)
            dg.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(color[0], color[1], color[2], a))
        layer.alpha_composite(glow)
# -------------------------
# Timeline
# -------------------------
# Targets
SUB_POS = (W // 2, H // 2 - 40)
LIKE_POS = (W // 2 - 170, H // 2 + 80)
SHARE_POS = (W // 2 + 170, H // 2 + 80)

frames = []

for f in range(N_FRAMES):
    t = f / (N_FRAMES - 1)  # 0..1
    img = Image.new("RGBA", (W, H), BG + (255,))
    # Global fade (starts around 45/60 to 60/60)
    fade_t = clamp((f - int(0.75 * N_FRAMES)) / (0.25 * N_FRAMES))
    global_alpha = 1.0 - ease_in_out_sine(fade_t)

    # Layers
    layer_sub = make_layer()
    layer_like = make_layer()
    layer_share = make_layer()
    layer_glow = make_layer()

    # --- Subscribe slide-in (0.0s -> 0.5s)
    sub_slide_t = clamp(f / (0.5 * FPS))
    sub_x = lerp(-300, SUB_POS[0], ease_out_cubic(sub_slide_t))
    sub_y = SUB_POS[1]
    # Pulse + bell spin on "click" (~0.5s -> 0.75s)
    pulse = 0.0
    bell_angle = 0.0
    click_ripple = 0.0
    if 0.5 * FPS <= f < 0.75 * FPS:
        local = (f - 0.5 * FPS) / (0.25 * FPS)  # 0..1
        pulse = 1 + 0.15 * triangle(local)
        bell_angle = 360 * local
        click_ripple = local
    else:
        pulse = 1.0

    draw_subscribe(layer_sub, int(sub_x), sub_y, scale=pulse, bell_angle=bell_angle, click_ripple=click_ripple)

    
    # --- Like bounce-in (1.0s -> 1.5s)
    like_in_t = clamp((f - 1.0 * FPS) / (0.5 * FPS))
    like_y = LIKE_POS[1] + int((1 - ease_out_back(like_in_t)) * 90)
    draw_like(layer_like, LIKE_POS[0], like_y, t_bounce=like_in_t)

    # --- Share fly-in + spin (1.5s -> 2.0s)
    share_in_t = clamp((f - 1.5 * FPS) / (0.5 * FPS))
    share_x = int(lerp(W + 300, SHARE_POS[0], ease_out_cubic(share_in_t)))
    share_angle = 360 * share_in_t
    draw_share(layer_share, share_x, SHARE_POS[1], angle_deg=share_angle)

    # --- Glow burst (2.0s -> 2.5s)
    if 2.0 * FPS <= f < 2.5 * FPS:
        glow_t = (f - 2.0 * FPS) / (0.5 * FPS)
        draw_glow(layer_glow, [SUB_POS, LIKE_POS, SHARE_POS], color=WHITE, intensity=1 - glow_t)

    # Composite with global fade
    paste_with_alpha(img, layer_sub, global_alpha)
    paste_with_alpha(img, layer_like, global_alpha)
    paste_with_alpha(img, layer_share, global_alpha)
    paste_with_alpha(img, layer_glow, global_alpha)

    frames.append(img.convert("P", palette=Image.ADAPTIVE, dither=Image.NONE))
# Save GIF
out_path = "cta_like_share_subscribe.gif"
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    disposal=2,
    optimize=False,
)

print(f"Saved {out_path} ({N_FRAMES} frames at {FPS} fps).")
