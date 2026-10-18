"""Escena 1 - Intro (~15 s)
Título, función destacada, integrantes y colegio.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation

DURATION = 15.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_01_intro.mp4")

fig, ax = su.make_figure()

# --- Elementos estáticos (alpha inicial 0, se anima en update) ---
title = ax.text(8, 7.55, "CASO DE ESTUDIO", ha="center", va="center",
                 **su.title_kwargs(size=50), alpha=0, zorder=10)
subtitle = ax.text(8, 6.75, "Estación 2  ·  Matemática  ·  3° BATIN",
                    ha="center", va="center", fontsize=22, color=su.TURQUOISE,
                    fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=10)

card = su.rounded_card(ax, 8, 5.0, 7.6, 1.7, facecolor=su.CARD_BG, radius=0.22, zorder=4)
card.set_bounds(8 - 0.01, 5.0 - 0.01, 0.02, 0.02)  # arranca colapsada
formula = ax.text(8, 5.0, r"$h(x) = \dfrac{1}{x-2}$", ha="center", va="center",
                   fontsize=40, color=su.TURQUOISE, zorder=12, alpha=0)

school = ax.text(8, 3.35, "San Ignacio de Loyola School — Paraguay",
                  ha="center", va="center", fontsize=19, color=su.TEXT_MUTED,
                  fontfamily=su.BODY_FONT, alpha=0, zorder=10)

group_label = ax.text(8, 2.55, "GRUPO 4", ha="center", va="center",
                       fontsize=18, color=su.GOLD, fontfamily=su.TITLE_FONT,
                       fontweight="bold", alpha=0, zorder=10)

names = ["Sofía Cabrera", "Micaela Cubilla", "Fabrizio Riquelme", "Jerónimo Lovera"]
colors = [su.TURQUOISE, su.ORANGE, su.VIOLET, su.GOLD]
xs = [2.4, 6.1, 9.9, 13.6]
name_dots = []
name_texts = []
for nx, nm, c in zip(xs, names, colors):
    dot = ax.scatter([nx], [1.55], s=0, color=c, zorder=11)
    txt = ax.text(nx, 1.05, nm, ha="center", va="center", fontsize=15.5,
                   color=su.TEXT_LIGHT, fontfamily=su.BODY_FONT, alpha=0, zorder=11)
    name_dots.append(dot)
    name_texts.append(txt)

CARD_W, CARD_H = 7.6, 1.7
NAME_START = 4.3
NAME_STAGGER = 0.28


def update(frame):
    t = su.frame_time(frame)

    e = su.eased(t, 0.25, 0.8)
    title.set_alpha(e)
    title.set_position((8, 7.3 + 0.25 * (1 - e)))

    e = su.eased(t, 1.0, 0.7)
    subtitle.set_alpha(e)

    e = su.eased(t, 1.9, 0.8)
    w = max(0.02, CARD_W * e)
    h = max(0.02, CARD_H * e)
    su.set_card_bounds(card, 8, 5.0, w, h)
    formula.set_alpha(su.eased(t, 2.3, 0.6))

    school.set_alpha(su.eased(t, 3.1, 0.7))
    group_label.set_alpha(su.eased(t, 3.8, 0.6))

    for i, (dot, txt) in enumerate(zip(name_dots, name_texts)):
        st = NAME_START + i * NAME_STAGGER
        e = su.eased(t, st, 0.55)
        dot.set_sizes([140 * e])
        txt.set_alpha(e)
        txt.set_position((xs[i], 1.05 + 0.15 * (1 - e)))

    return [title, subtitle, card, formula, school, group_label] + name_dots + name_texts


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_01_intro ->", OUT)
