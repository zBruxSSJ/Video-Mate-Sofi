"""Escena 4 - Condición 1 (~25 s)
h(2) = 1/(2-2) = 1/0 -> No existe. Marca roja X animada.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np

DURATION = 25.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_04_condicion1.mp4")

fig, ax = su.make_figure()

badge = Circle((2.0, 7.9), 0.01, facecolor=su.TURQUOISE, edgecolor="none", zorder=7)
ax.add_patch(badge)
badge_num = ax.text(2.0, 7.9, "1", ha="center", va="center", fontsize=20,
                     color=su.BG_TOP, fontfamily=su.TITLE_FONT, fontweight="bold",
                     alpha=0, zorder=8)
header = ax.text(2.55, 7.9, "Condición 1:  h(a) existe", ha="left", va="center",
                  **su.title_kwargs(size=26), alpha=0, zorder=8)

sub = ax.text(8, 7.2, "Evaluamos en a = 2", ha="center", va="center",
              fontsize=18, color=su.TEXT_MUTED, fontfamily=su.BODY_FONT, alpha=0, zorder=8)

step1 = ax.text(8, 5.85, r"$h(2) = \dfrac{1}{2-2}$", ha="center", va="center",
                 fontsize=30, color=su.TEXT_LIGHT, alpha=0, zorder=8)
step2 = ax.text(8, 4.35, r"$h(2) = \dfrac{1}{0}$", ha="center", va="center",
                 fontsize=30, color=su.TEXT_LIGHT, alpha=0, zorder=8)
step3 = ax.text(8, 3.05, "No existe", ha="center", va="center",
                 fontsize=32, color=su.RED, fontfamily=su.TITLE_FONT,
                 fontweight="bold", alpha=0, zorder=8)

cross = ax.text(8, 1.85, "✗", ha="center", va="center", fontsize=10,
                 color=su.RED, fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=9)

caption_card = su.rounded_card(ax, 8, 0.78, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.2, zorder=4)
caption = ax.text(8, 0.78, "Falla la condición 1 — h(2) no está definida",
                   ha="center", va="center", fontsize=17.5, color=su.TEXT_LIGHT,
                   fontfamily=su.BODY_FONT, alpha=0, zorder=7)
CAP_W, CAP_H = 8.6, 0.9


def update(frame):
    t = su.frame_time(frame)

    eb = su.eased(t, 0.2, 0.5)
    badge.set_radius(max(0.001, 0.4 * eb))
    badge_num.set_alpha(eb)
    header.set_alpha(su.eased(t, 0.45, 0.6))

    sub.set_alpha(su.eased(t, 1.2, 0.6))

    step1.set_alpha(su.eased(t, 2.0, 0.7))
    step2.set_alpha(su.eased(t, 3.3, 0.7))

    e3 = su.eased(t, 4.6, 0.7)
    step3.set_alpha(e3)
    step3.set_position((8, 3.05 - 0.1 * (1 - e3)))

    ec = su.eased(t, 5.8, 0.55)
    cross.set_fontsize(10 + 70 * ec)
    cross.set_alpha(ec)

    cp = su.eased(t, 7.0, 0.7)
    w = max(0.02, CAP_W * cp)
    h = max(0.02, CAP_H * cp)
    su.set_card_bounds(caption_card, 8, 0.78, w, h)
    caption.set_alpha(su.eased(t, 7.3, 0.6))

    if t > 6.5:
        pulse = 1.0 + 0.04 * np.sin((t - 6.5) * 1.8)
        cross.set_fontsize(80 * pulse)

    return [badge, badge_num, header, sub, step1, step2, step3, cross, caption_card, caption]


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_04_condicion1 ->", OUT)
