"""Escena 6 - Condición 3 y conclusión parcial (~25 s)
h(2) != lim x->2 h(x). No se cumplen las 3 condiciones (resumen con 3 X).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np

DURATION = 25.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_06_condicion3.mp4")

fig, ax = su.make_figure()

badge = Circle((1.7, 8.35), 0.01, facecolor=su.VIOLET, edgecolor="none", zorder=7)
ax.add_patch(badge)
badge_num = ax.text(1.7, 8.35, "3", ha="center", va="center", fontsize=19,
                     color=su.BG_TOP, fontfamily=su.TITLE_FONT, fontweight="bold",
                     alpha=0, zorder=8)
header = ax.text(2.2, 8.35, r"Condición 3:  $\lim_{x\to a} h(x) = h(a)$", ha="left", va="center",
                  **su.title_kwargs(size=22), alpha=0, zorder=8)

sub = ax.text(8, 7.55, "Comparamos el valor de la función con el límite",
              ha="center", va="center", fontsize=17, color=su.TEXT_MUTED,
              fontfamily=su.BODY_FONT, alpha=0, zorder=8)

main_eq = ax.text(8, 6.45, r"$h(2) \;\neq\; \lim_{x\to 2} h(x)$", ha="center", va="center",
                   fontsize=32, color=su.RED, fontfamily=su.BODY_FONT, fontweight="bold",
                   alpha=0, zorder=8)
explain = ax.text(8, 5.65, "porque ninguno de los dos existe",
                   ha="center", va="center", fontsize=18, color=su.TEXT_LIGHT,
                   fontfamily=su.BODY_FONT, alpha=0, zorder=8)

cross1 = ax.text(8, 4.75, "✗", ha="center", va="center", fontsize=10,
                  color=su.RED, fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=9)

summary_title = ax.text(8, 3.75, "No se cumplen las 3 condiciones",
                         **su.title_kwargs(size=25, color=su.RED), ha="center", va="center",
                         alpha=0, zorder=8)

COLS_X = [3.2, 8.0, 12.8]
labels = ["h(a) existe", r"$\lim_{x\to a} h(x)$ existe", r"$\lim_{x\to a} h(x) = h(a)$"]
COND_COLORS = [su.TURQUOISE, su.ORANGE, su.VIOLET]
CARD_Y = 1.75
CARD_W, CARD_H = 4.5, 2.0

mini_cards = []
mini_labels = []
mini_crosses = []
for i in range(3):
    c = su.rounded_card(ax, COLS_X[i], CARD_Y, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.2, zorder=4)
    mini_cards.append(c)
    lbl = ax.text(COLS_X[i], CARD_Y + 0.5, labels[i], ha="center", va="center",
                   fontsize=15, color=COND_COLORS[i], fontfamily=su.BODY_FONT,
                   fontweight="bold", alpha=0, zorder=7)
    mini_labels.append(lbl)
    cr = ax.text(COLS_X[i], CARD_Y - 0.35, "✗", ha="center", va="center", fontsize=10,
                 color=su.RED, fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=7)
    mini_crosses.append(cr)

CARD_START = [7.6, 8.1, 8.6]


def update(frame):
    t = su.frame_time(frame)

    eb = su.eased(t, 0.2, 0.5)
    badge.set_radius(max(0.001, 0.38 * eb))
    badge_num.set_alpha(eb)
    header.set_alpha(su.eased(t, 0.45, 0.6))
    sub.set_alpha(su.eased(t, 1.2, 0.6))

    main_eq.set_alpha(su.eased(t, 2.3, 0.7))
    explain.set_alpha(su.eased(t, 3.5, 0.7))

    ec1 = su.eased(t, 4.6, 0.5)
    cross1.set_fontsize(10 + 50 * ec1)
    cross1.set_alpha(ec1)

    summary_title.set_alpha(su.eased(t, 5.8, 0.7))

    for i in range(3):
        st = CARD_START[i]
        e = su.eased(t, st, 0.8)
        w = max(0.02, CARD_W * e)
        h = max(0.02, CARD_H * e)
        su.set_card_bounds(mini_cards[i], COLS_X[i], CARD_Y, w, h)
        mini_labels[i].set_alpha(su.eased(t, st + 0.3, 0.6))
        ecr = su.eased(t, st + 0.55, 0.5)
        mini_crosses[i].set_fontsize(10 + 36 * ecr)
        mini_crosses[i].set_alpha(ecr)

    if t > 10.0:
        pulse = 1.0 + 0.04 * np.sin((t - 10.0) * 1.6)
        for cr in mini_crosses:
            cr.set_fontsize(46 * pulse)

    return ([badge, badge_num, header, sub, main_eq, explain, cross1, summary_title]
             + mini_cards + mini_labels + mini_crosses)


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_06_condicion3 ->", OUT)
