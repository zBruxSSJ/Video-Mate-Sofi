"""Escena 3 - El caso (~25 s)
Presenta h(x) = 1/(x-2), x = 2 resaltado en una recta numérica,
y la pregunta: ¿es continua en x = 2?
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
import numpy as np

DURATION = 25.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_03_el_caso.mp4")

fig, ax = su.make_figure()

title = ax.text(8, 8.1, "El caso de estudio", ha="center", va="center",
                 **su.title_kwargs(size=30), alpha=0, zorder=10)

formula = ax.text(8, 6.85, r"$h(x) = \dfrac{1}{x-2}$", ha="center", va="center",
                   fontsize=34, color=su.TURQUOISE, alpha=0, zorder=10)

# --- Recta numérica ---
LINE_Y = 4.15
V0, V1 = -1, 5  # rango de valores
X_START, X_END = 2.2, 13.8


def to_screen(v):
    return X_START + (v - V0) * (X_END - X_START) / (V1 - V0)


line_lines = su.glow_plot(ax, [X_START, X_START], [LINE_Y, LINE_Y], su.TEXT_MUTED,
                           lw=2.2, n_layers=2, zorder=3, alpha_core=0.9)

tick_marks = []
tick_labels = []
for v in range(V0, V1 + 1):
    sx = to_screen(v)
    tm, = ax.plot([sx, sx], [LINE_Y - 0.09, LINE_Y + 0.09], color=su.TEXT_MUTED,
                  lw=1.8, alpha=0, zorder=4)
    tick_marks.append(tm)
    lbl = ax.text(sx, LINE_Y - 0.45, str(v), ha="center", va="center",
                   fontsize=15, color=su.TEXT_MUTED, fontfamily=su.BODY_FONT, alpha=0, zorder=4)
    tick_labels.append(lbl)

x2_screen = to_screen(2)
highlight = ax.scatter([x2_screen], [LINE_Y], s=0, color=su.ORANGE, zorder=8,
                        edgecolors=su.TEXT_LIGHT, linewidths=1.6)
guide, = ax.plot([x2_screen, x2_screen], [LINE_Y, LINE_Y], color=su.ORANGE,
                  lw=2.2, linestyle=(0, (5, 4)), alpha=0, zorder=5)
x2_label = ax.text(x2_screen, LINE_Y + 1.15, "x = 2", ha="center", va="center",
                    fontsize=20, color=su.ORANGE, fontfamily=su.BODY_FONT,
                    fontweight="bold", alpha=0, zorder=8)

q_card = su.rounded_card(ax, 8, 1.55, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.22, zorder=4)
question = ax.text(8, 1.55, "¿Es continua h(x) en x = 2?", ha="center", va="center",
                    fontsize=24, color=su.TEXT_LIGHT, fontfamily=su.TITLE_FONT,
                    fontweight="bold", alpha=0, zorder=7)
Q_W, Q_H = 8.6, 1.3


def update(frame):
    t = su.frame_time(frame)

    title.set_alpha(su.eased(t, 0.2, 0.7))
    formula.set_alpha(su.eased(t, 0.9, 0.7))

    e_line = su.eased(t, 1.7, 1.0)
    xs = [X_START, X_START + (X_END - X_START) * e_line]
    su.glow_update(line_lines, xs, [LINE_Y, LINE_Y])

    for i, v in enumerate(range(V0, V1 + 1)):
        sx = to_screen(v)
        frac = (sx - X_START) / (X_END - X_START)
        a = 1.0 if e_line >= frac else 0.0
        a2 = su.eased(t, 2.7, 0.8)
        tick_marks[i].set_alpha(min(a, 1.0) * a2)
        tick_labels[i].set_alpha(min(a, 1.0) * a2)

    eh = su.eased(t, 3.6, 0.6)
    highlight.set_sizes([260 * eh])
    guide.set_alpha(0.8 * su.eased(t, 3.9, 0.5))
    guide.set_data([x2_screen, x2_screen], [LINE_Y - 0.4 * eh, LINE_Y + 0.9 * eh])
    x2_label.set_alpha(su.eased(t, 4.3, 0.6))

    eq = su.eased(t, 5.4, 0.8)
    w = max(0.02, Q_W * eq)
    h = max(0.02, Q_H * eq)
    su.set_card_bounds(q_card, 8, 1.55, w, h)
    question.set_alpha(su.eased(t, 5.8, 0.7))

    if t > 4.6:
        pulse = 1.0 + 0.08 * np.sin((t - 4.6) * 1.6)
        highlight.set_sizes([260 * pulse])

    return [title, formula, guide, x2_label, q_card, question, highlight] + tick_marks + tick_labels + line_lines


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_03_el_caso ->", OUT)
