"""Escena 2 - Condiciones de continuidad (~30 s)
3 tarjetas animadas con las condiciones de continuidad en x = a.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np

DURATION = 30.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_02_condiciones.mp4")

fig, ax = su.make_figure()

title = ax.text(8, 8.05, "Condiciones de continuidad en x = a",
                 ha="center", va="center", **su.title_kwargs(size=32), alpha=0, zorder=10)
sub = ax.text(8, 7.35, "Deben cumplirse las TRES para que una función sea continua",
              ha="center", va="center", fontsize=18, color=su.TEXT_MUTED,
              fontfamily=su.BODY_FONT, alpha=0, zorder=10)

COND_COLORS = [su.TURQUOISE, su.ORANGE, su.VIOLET]
COND_X = [3.2, 8.0, 12.8]
COND_Y = 4.1
CARD_W, CARD_H = 4.5, 3.6

cards = []
badges = []
badge_nums = []
formulas = []
captions = []

formula_tex = [
    r"$h(a)\ \mathrm{existe}$",
    r"$\lim_{x\to a} h(x)\ \mathrm{existe}$",
    r"$\lim_{x\to a} h(x) = h(a)$",
]
caption_txt = ["La función está\ndefinida en a", "El límite tiene\nun valor finito", "El límite coincide\ncon el valor de la función"]
numbers = ["1", "2", "3"]

for i in range(3):
    cx = COND_X[i]
    c = su.rounded_card(ax, cx, COND_Y, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.22, zorder=4)
    cards.append(c)

    badge = Circle((cx, COND_Y + 1.15), 0.01, facecolor=COND_COLORS[i], edgecolor="none", zorder=6)
    ax.add_patch(badge)
    badges.append(badge)
    num = ax.text(cx, COND_Y + 1.15, numbers[i], ha="center", va="center",
                   fontsize=22, color=su.BG_TOP, fontfamily=su.TITLE_FONT,
                   fontweight="bold", alpha=0, zorder=7)
    badge_nums.append(num)

    f = ax.text(cx, COND_Y + 0.15, formula_tex[i], ha="center", va="center",
                fontsize=21, color=su.TEXT_LIGHT, alpha=0, zorder=7)
    formulas.append(f)

    cap = ax.text(cx, COND_Y - 1.0, caption_txt[i], ha="center", va="center",
                   fontsize=14.5, color=su.TEXT_MUTED, fontfamily=su.BODY_FONT,
                   alpha=0, zorder=7, linespacing=1.5)
    captions.append(cap)

START = [3.0, 5.6, 8.2]


def update(frame):
    t = su.frame_time(frame)

    title.set_alpha(su.eased(t, 0.2, 0.8))
    sub.set_alpha(su.eased(t, 0.9, 0.8))

    for i in range(3):
        st = START[i]
        e = su.eased(t, st, 0.9)
        w = max(0.02, CARD_W * e)
        h = max(0.02, CARD_H * e)
        su.set_card_bounds(cards[i], COND_X[i], COND_Y, w, h)

        eb = su.eased(t, st + 0.35, 0.5)
        badges[i].set_radius(max(0.001, 0.46 * eb))
        badge_nums[i].set_alpha(eb)

        ef = su.eased(t, st + 0.55, 0.6)
        formulas[i].set_alpha(ef)

        ec = su.eased(t, st + 0.8, 0.6)
        captions[i].set_alpha(ec)

        # pulso suave de respiración una vez asentado
        if t > st + 1.6:
            pulse = 1.0 + 0.03 * np.sin((t - st - 1.6) * 1.3)
            badges[i].set_radius(0.46 * pulse)

    return cards + badges + badge_nums + formulas + captions + [title, sub]


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_02_condiciones ->", OUT)
