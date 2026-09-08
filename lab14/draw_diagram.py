#!/usr/bin/env python3
"""UML Activity Diagram for Lab 14: tour/excursion seat booking."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1100, 1450
BG = (255, 255, 255)
ORANGE = (255, 183, 77)
ORANGE_BORDER = (180, 120, 40)
YELLOW = (255, 235, 59)
YELLOW_BORDER = (180, 160, 20)
GREEN = (56, 142, 60)
RED = (211, 47, 47)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LANE_HEADER_BG = (245, 245, 245)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def text_size(draw, text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def center_text(draw, cx, cy, text, f, fill=BLACK):
    tw, th = text_size(draw, text, f)
    draw.text((cx - tw / 2, cy - th / 2), text, font=f, fill=fill)


def wrapped_center(draw, cx, cy, text, f, max_width, fill=BLACK, line_gap=4):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        tw, _ = text_size(draw, trial, f)
        if tw <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    heights = [text_size(draw, ln, f)[1] for ln in lines]
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = cy - total_h / 2
    for ln, th in zip(lines, heights):
        tw, _ = text_size(draw, ln, f)
        draw.text((cx - tw / 2, y), ln, font=f, fill=fill)
        y += th + line_gap


def rounded_rect(draw, box, fill, outline, radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def activity(draw, cx, cy, w, h, text, f):
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    rounded_rect(draw, box, ORANGE, BLACK, radius=20, width=2)
    wrapped_center(draw, cx, cy, text, f, max_width=w - 24)
    return box


def diamond(draw, cx, cy, size, text, f):
    half = size / 2
    pts = [
        (cx, cy - half),
        (cx + half, cy),
        (cx, cy + half),
        (cx - half, cy),
    ]
    draw.polygon(pts, fill=YELLOW, outline=BLACK)
    # redraw outline thicker
    draw.line(pts + [pts[0]], fill=BLACK, width=2)
    wrapped_center(draw, cx, cy, text, f, max_width=size * 0.85)
    return pts


def arrow(draw, x1, y1, x2, y2, color=BLACK, width=2):
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    # arrow head
    import math

    angle = math.atan2(y2 - y1, x2 - x1)
    ah = 12
    a1 = angle + math.radians(150)
    a2 = angle - math.radians(150)
    p1 = (x2 + ah * math.cos(a1), y2 + ah * math.sin(a1))
    p2 = (x2 + ah * math.cos(a2), y2 + ah * math.sin(a2))
    draw.polygon([(x2, y2), p1, p2], fill=color)


def sync_bar(draw, x1, x2, y, thickness=10):
    draw.rectangle([x1, y - thickness / 2, x2, y + thickness / 2], fill=(240, 240, 240), outline=BLACK, width=2)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title = font(22, bold=True)
    f_lane = font(20, bold=True)
    f_act = font(15)
    f_small = font(14, bold=True)
    f_label = font(13, bold=True)

    # Title
    center_text(draw, W / 2, 28, "Лабораторная работа №14. Диаграмма деятельности", f_title)
    center_text(draw, W / 2, 56, "Бронирование мест на экскурсии и туры", font(16))

    # Swimlanes
    top = 90
    bottom = H - 30
    left = 40
    right = W - 40
    lane_w = (right - left) / 3
    lanes = [
        (left, "Клиент"),
        (left + lane_w, "Система/Админ"),
        (left + 2 * lane_w, "Гид/Туроператор"),
    ]

    # outer frame
    draw.rectangle([left, top, right, bottom], outline=BLACK, width=2)
    # header band
    header_h = 48
    draw.rectangle([left, top, right, top + header_h], fill=LANE_HEADER_BG, outline=BLACK, width=2)
    for i, (x, name) in enumerate(lanes):
        if i > 0:
            draw.line([(x, top), (x, bottom)], fill=BLACK, width=2)
        center_text(draw, x + lane_w / 2, top + header_h / 2, name, f_lane)

    # Column centers
    c1 = left + lane_w / 2
    c2 = left + lane_w + lane_w / 2
    c3 = left + 2 * lane_w + lane_w / 2

    box_w, box_h = 230, 56

    # Y positions — mirror example layout
    y_start = 170
    y_auth = 240
    y_date = 340
    y_route = 440
    y_seats = 540
    y_avail = 540
    y_decision = 660
    y_reg = 790
    y_fork = 870
    y_parallel = 960
    y_join = 1060
    y_confirm = 1180
    y_end = 1300

    # Start node
    r = 16
    draw.ellipse([c1 - r, y_start - r, c1 + r, y_start + r], fill=GREEN, outline=BLACK, width=2)
    arrow(draw, c1, y_start + r, c1, y_auth - box_h / 2)

    # Client activities
    activity(draw, c1, y_auth, box_w, box_h, "Авторизоваться в системе", f_act)
    arrow(draw, c1, y_auth + box_h / 2, c1, y_date - box_h / 2)

    activity(draw, c1, y_date, box_w, box_h, "Выбрать дату экскурсии/тура", f_act)
    arrow(draw, c1, y_date + box_h / 2, c1, y_route - box_h / 2)

    activity(draw, c1, y_route, box_w, box_h, "Выбрать маршрут", f_act)
    arrow(draw, c1, y_route + box_h / 2, c1, y_seats - box_h / 2)

    activity(draw, c1, y_seats, box_w, box_h, "Указать количество мест", f_act)

    # Arrow to system availability check
    arrow(draw, c1 + box_w / 2, y_seats, c2 - box_w / 2, y_avail)
    activity(draw, c2, y_avail, box_w, box_h, "Проверка доступности мест", f_act)
    arrow(draw, c2, y_avail + box_h / 2, c2, y_decision - 55)

    # Decision
    diamond(draw, c2, y_decision, 110, "Свободно?", f_small)

    # Нет — loop back to date selection
    # go left from diamond, up, to date box
    loop_x = c1 - box_w / 2 - 18
    draw.line([(c2 - 55, y_decision), (loop_x, y_decision)], fill=RED, width=2)
    draw.line([(loop_x, y_decision), (loop_x, y_date)], fill=RED, width=2)
    arrow(draw, loop_x, y_date, c1 - box_w / 2, y_date, color=RED)
    center_text(draw, (c2 - 55 + loop_x) / 2, y_decision - 16, "Нет", f_label, RED)

    # Да — down
    arrow(draw, c2, y_decision + 55, c2, y_reg - box_h / 2, color=GREEN)
    center_text(draw, c2 + 28, y_decision + 78, "Да", f_label, GREEN)

    activity(draw, c2, y_reg, box_w + 20, box_h, "Зарегистрировать заявку на бронирование", f_act)
    arrow(draw, c2, y_reg + box_h / 2, c2, y_fork - 8)

    # Fork bar spanning system + guide lanes partly
    fork_left = c2 - 80
    fork_right = c3 + 80
    sync_bar(draw, fork_left, fork_right, y_fork, thickness=12)

    # Parallel: reminder (system) and message (guide)
    arrow(draw, c2, y_fork + 6, c2, y_parallel - box_h / 2)
    activity(draw, c2, y_parallel, box_w, box_h, "Настроить авто напоминание", f_act)

    arrow(draw, c3, y_fork + 6, c3, y_parallel - box_h / 2)
    # horizontal from fork mid to c3 top of fork already covered by bar
    draw.line([(c2, y_fork), (c3, y_fork)], fill=BLACK, width=2)
    activity(draw, c3, y_parallel, box_w, box_h, "Получение сообщения о бронировании", f_act)

    # down to join
    arrow(draw, c2, y_parallel + box_h / 2, c2, y_join - 8)
    arrow(draw, c3, y_parallel + box_h / 2, c3, y_join - 8)
    sync_bar(draw, fork_left, fork_right, y_join, thickness=12)
    draw.line([(c2, y_join), (c3, y_join)], fill=BLACK, width=2)

    # to confirmation in client lane
    mid_y = (y_join + y_confirm) / 2 - 40
    draw.line([(c2, y_join + 6), (c2, mid_y)], fill=BLACK, width=2)
    draw.line([(c2, mid_y), (c1, mid_y)], fill=BLACK, width=2)
    arrow(draw, c1, mid_y, c1, y_confirm - box_h / 2)

    activity(draw, c1, y_confirm, box_w + 10, box_h + 8, "Получение подтверждения в личном кабинете", f_act)
    arrow(draw, c1, y_confirm + box_h / 2 + 4, c1, y_end - 20)

    # End node
    r_out, r_in = 20, 12
    draw.ellipse([c1 - r_out, y_end - r_out, c1 + r_out, y_end + r_out], outline=RED, width=3)
    draw.ellipse([c1 - r_in, y_end - r_in, c1 + r_in, y_end + r_in], fill=RED, outline=RED)

    out = "/workspace/lab14/diagramma_deyatelnosti.png"
    img.save(out, "PNG")
    print("Saved", out)


if __name__ == "__main__":
    main()
