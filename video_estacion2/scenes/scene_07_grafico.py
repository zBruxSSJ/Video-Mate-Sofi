"""Escena 7 - Gráfico (~40 s)
Gráfico animado de h(x) = 1/(x-2): dos ramas dibujándose, asíntota vertical
punteada en x=2, flechas al infinito, panel lateral con la conclusión.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
import numpy as np

DURATION = 40.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_07_grafico.mp4")

fig, ax = su.make_figure()

title = ax.text(5.6, 8.45, "Gráfico de h(x) = 1/(x − 2)", ha="center", va="center",
                 **su.title_kwargs(size=26), alpha=0, zorder=10)

# --- Panel de gráfico (inset Axes real, coordenadas matemáticas) ---
# Región en fracción de figura: ocupa la mitad izquierda del cuadro
graph_ax = fig.add_axes([0.035, 0.09, 0.595, 0.76])
graph_ax.set_facecolor("none")
XMIN, XMAX = -2, 6
YMIN, YMAX = -8, 8
graph_ax.set_xlim(XMIN, XMAX)
graph_ax.set_ylim(YMIN, YMAX)
for s in graph_ax.spines.values():
    s.set_visible(False)
graph_ax.set_xticks(range(XMIN, XMAX + 1))
graph_ax.set_yticks(range(YMIN, YMAX + 1, 2))
graph_ax.tick_params(colors=su.TEXT_MUTED, labelsize=10)
for lbl in graph_ax.get_xticklabels() + graph_ax.get_yticklabels():
    lbl.set_fontfamily(su.BODY_FONT)
graph_ax.grid(True, color=su.TEXT_MUTED, alpha=0.0, linewidth=0.6)
graph_ax.set_zorder(2)

axis_x = graph_ax.axhline(0, color=su.TEXT_MUTED, lw=1.4, alpha=0, zorder=3)
axis_y = graph_ax.axvline(0, color=su.TEXT_MUTED, lw=1.4, alpha=0, zorder=3)

asymptote = graph_ax.axvline(2, color=su.RED, lw=2.2, linestyle=(0, (5, 4)), alpha=0, zorder=4)
asym_label = graph_ax.text(-1.85, 6.9, "x = 2", ha="left", va="center", fontsize=14,
                            color=su.RED, fontfamily=su.BODY_FONT, fontweight="bold",
                            alpha=0, zorder=6)
asym_sub = graph_ax.text(-1.85, 5.75, "asíntota\nvertical", ha="left", va="center",
                          fontsize=10.5, color=su.RED, fontfamily=su.BODY_FONT,
                          alpha=0, zorder=6, linespacing=1.4)

IZQ = su.VIOLET
DER = su.GOLD
LEFT_OUTER, LEFT_INNER = -2.0, 1.875   # y = -8 en el extremo interno
RIGHT_OUTER, RIGHT_INNER = 6.0, 2.125  # y = +8 en el extremo interno
N = 200

left_lines = su.glow_plot(graph_ax, [LEFT_OUTER], [1 / (LEFT_OUTER - 2)], IZQ, lw=2.6,
                           n_layers=4, zorder=5)
right_lines = su.glow_plot(graph_ax, [RIGHT_OUTER], [1 / (RIGHT_OUTER - 2)], DER, lw=2.6,
                            n_layers=4, zorder=5)

arrow_left = graph_ax.annotate("", xy=(1.875, -7.9), xytext=(1.875, -7.0),
                                arrowprops=dict(arrowstyle="-|>", color=IZQ, lw=2.2),
                                zorder=6, alpha=0)
arrow_right = graph_ax.annotate("", xy=(2.125, 7.9), xytext=(2.125, 7.0),
                                 arrowprops=dict(arrowstyle="-|>", color=DER, lw=2.2),
                                 zorder=6, alpha=0)

# --- Panel lateral de conclusión ---
panel_cx, panel_cy = 13.1, 4.35
panel = su.rounded_card(ax, panel_cx, panel_cy, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.18, zorder=4)
PANEL_W, PANEL_H = 5.3, 5.6

panel_title = ax.text(panel_cx, panel_cy + 2.2, "CONCLUSIÓN", ha="center", va="center",
                       fontsize=18, color=su.GOLD, fontfamily=su.TITLE_FONT,
                       fontweight="bold", alpha=0, zorder=7)
panel_line1 = ax.text(panel_cx, panel_cy + 1.35, "h(x) es discontinua\nen x = 2", ha="center",
                       va="center", fontsize=19, color=su.TEXT_LIGHT, fontfamily=su.BODY_FONT,
                       fontweight="bold", alpha=0, zorder=7, linespacing=1.5)
panel_div, = ax.plot([panel_cx - 2.0, panel_cx + 2.0], [panel_cy + 0.35, panel_cy + 0.35],
                      color=su.TEXT_MUTED, lw=1.0, alpha=0, zorder=7)
panel_class = ax.text(panel_cx, panel_cy - 0.5, "Discontinuidad\ninevitable\nde salto infinito",
                       ha="center", va="center", fontsize=18, color=su.RED,
                       fontfamily=su.TITLE_FONT, fontweight="bold", alpha=0, zorder=7,
                       linespacing=1.5)
panel_note = ax.text(panel_cx, panel_cy - 2.25, "(la recta x = 2 es\nasíntota vertical)",
                      ha="center", va="center", fontsize=13.5, color=su.TEXT_MUTED,
                      fontfamily=su.BODY_FONT, alpha=0, zorder=7, linespacing=1.5)


def branch_xy(progress_e, outer, inner, n=N):
    cur = outer + progress_e * (inner - outer)
    xs = np.linspace(outer, cur, max(2, int(n * max(progress_e, 0.02))))
    ys = 1.0 / (xs - 2)
    return xs, ys


def update(frame):
    t = su.frame_time(frame)

    title.set_alpha(su.eased(t, 0.2, 0.7))

    ea = su.eased(t, 1.0, 0.7)
    axis_x.set_alpha(0.8 * ea)
    axis_y.set_alpha(0.8 * ea)
    graph_ax.grid(True, alpha=0.08 * ea)

    eas = su.eased(t, 2.0, 0.7)
    asymptote.set_alpha(eas)
    asym_label.set_alpha(su.eased(t, 2.5, 0.6))
    asym_sub.set_alpha(su.eased(t, 3.0, 0.6))

    e_left = su.eased(t, 4.0, 2.6)
    xs, ys = branch_xy(e_left, LEFT_OUTER, LEFT_INNER)
    su.glow_update(left_lines, xs, ys)

    e_right = su.eased(t, 4.4, 2.6)
    xs2, ys2 = branch_xy(e_right, RIGHT_OUTER, RIGHT_INNER)
    su.glow_update(right_lines, xs2, ys2)

    arrow_left.set_alpha(su.eased(t, 6.8, 0.5))
    arrow_right.set_alpha(su.eased(t, 7.2, 0.5))

    ep = su.eased(t, 8.2, 0.8)
    w = max(0.02, PANEL_W * ep)
    h = max(0.02, PANEL_H * ep)
    su.set_card_bounds(panel, panel_cx, panel_cy, w, h)

    panel_title.set_alpha(su.eased(t, 9.2, 0.7))
    panel_line1.set_alpha(su.eased(t, 10.2, 0.7))
    panel_div.set_alpha(0.6 * su.eased(t, 11.0, 0.5))
    panel_class.set_alpha(su.eased(t, 11.3, 0.8))
    panel_note.set_alpha(su.eased(t, 12.5, 0.7))

    if t > 10.0:
        pulse = 0.85 + 0.15 * np.sin((t - 10.0) * 1.2)
        asymptote.set_alpha(eas * pulse)

    return ([title, axis_x, axis_y, asymptote, asym_label, asym_sub, arrow_left, arrow_right,
              panel, panel_title, panel_line1, panel_div, panel_class, panel_note]
             + left_lines + right_lines)


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_07_grafico ->", OUT)
