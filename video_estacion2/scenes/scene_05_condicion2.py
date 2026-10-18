"""Escena 5 - Condición 2 (~40 s)
Límites laterales lado a lado, con tabla animada de valores acercándose a 2.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np

DURATION = 40.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_05_condicion2.mp4")

fig, ax = su.make_figure()

IZQ = su.VIOLET
DER = su.GOLD

badge = Circle((1.7, 8.3), 0.01, facecolor=su.ORANGE, edgecolor="none", zorder=7)
ax.add_patch(badge)
badge_num = ax.text(1.7, 8.3, "2", ha="center", va="center", fontsize=19,
                     color=su.BG_TOP, fontfamily=su.TITLE_FONT, fontweight="bold",
                     alpha=0, zorder=8)
header = ax.text(2.2, 8.3, r"Condición 2:  $\lim_{x\to a} h(x)$ existe", ha="left", va="center",
                  **su.title_kwargs(size=23), alpha=0, zorder=8)

sub = ax.text(8, 7.55, "Límites laterales en x = 2", ha="center", va="center",
              fontsize=18, color=su.TEXT_MUTED, fontfamily=su.BODY_FONT, alpha=0, zorder=8)

LX, RX = 4.3, 11.7
head_izq = ax.text(LX, 6.85, "x → 2⁻  (lado izquierdo)", ha="center", va="center",
                    fontsize=17, color=IZQ, fontfamily=su.BODY_FONT, fontweight="bold",
                    alpha=0, zorder=8)
head_der = ax.text(RX, 6.85, "x → 2⁺  (lado derecho)", ha="center", va="center",
                    fontsize=17, color=DER, fontfamily=su.BODY_FONT, fontweight="bold",
                    alpha=0, zorder=8)

rows_izq_vals = [("1.9", "−10"), ("1.99", "−100"), ("1.999", "−1 000")]
rows_der_vals = [("2.1", "+10"), ("2.01", "+100"), ("2.001", "+1 000")]
ROW_YS = [6.15, 5.55, 4.95]

row_izq_texts = []
row_der_texts = []
for (xv, yv), ry in zip(rows_izq_vals, ROW_YS):
    t_ = ax.text(LX, ry, f"x = {xv}    h(x) = {yv}", ha="center", va="center",
                 fontsize=16.5, color=su.TEXT_LIGHT, fontfamily=su.BODY_FONT, alpha=0, zorder=8)
    row_izq_texts.append(t_)
for (xv, yv), ry in zip(rows_der_vals, ROW_YS):
    t_ = ax.text(RX, ry, f"x = {xv}    h(x) = {yv}", ha="center", va="center",
                 fontsize=16.5, color=su.TEXT_LIGHT, fontfamily=su.BODY_FONT, alpha=0, zorder=8)
    row_der_texts.append(t_)

limit_izq = ax.text(LX, 4.1, r"$\lim_{x\to 2^-} h(x) = -\infty$", ha="center", va="center",
                     fontsize=21, color=IZQ, fontfamily=su.BODY_FONT, fontweight="bold",
                     alpha=0, zorder=8)
limit_der = ax.text(RX, 4.1, r"$\lim_{x\to 2^+} h(x) = +\infty$", ha="center", va="center",
                     fontsize=21, color=DER, fontfamily=su.BODY_FONT, fontweight="bold",
                     alpha=0, zorder=8)

divider, = ax.plot([8, 8], [3.6, 6.9], color=su.TEXT_MUTED, lw=1.3, alpha=0, zorder=3,
                    linestyle=(0, (4, 4)))

comp_left = ax.text(6.6, 2.95, "−∞", ha="right", va="center", fontsize=34,
                     color=IZQ, fontfamily=su.TITLE_FONT, fontweight="bold", alpha=0, zorder=8)
comp_mid = ax.text(8, 2.95, "≠", ha="center", va="center", fontsize=34,
                    color=su.TEXT_LIGHT, fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=8)
comp_right = ax.text(9.4, 2.95, "+∞", ha="left", va="center", fontsize=34,
                      color=DER, fontfamily=su.TITLE_FONT, fontweight="bold", alpha=0, zorder=8)

conclusion = ax.text(8, 1.85, "No existe  lim x→2 h(x)", ha="center", va="center",
                      fontsize=23, color=su.RED, fontfamily=su.BODY_FONT,
                      fontweight="bold", alpha=0, zorder=8)
cross = ax.text(8, 0.8, "✗", ha="center", va="center", fontsize=10,
                 color=su.RED, fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=9)


def update(frame):
    t = su.frame_time(frame)

    eb = su.eased(t, 0.2, 0.5)
    badge.set_radius(max(0.001, 0.38 * eb))
    badge_num.set_alpha(eb)
    header.set_alpha(su.eased(t, 0.45, 0.6))
    sub.set_alpha(su.eased(t, 1.1, 0.6))

    divider.set_alpha(0.5 * su.eased(t, 1.7, 0.6))
    head_izq.set_alpha(su.eased(t, 1.9, 0.6))
    head_der.set_alpha(su.eased(t, 2.2, 0.6))

    row_start_izq = 2.9
    row_start_der = 3.3
    for i in range(3):
        e_i = su.eased(t, row_start_izq + i * 1.0, 0.6)
        row_izq_texts[i].set_alpha(e_i)
        e_d = su.eased(t, row_start_der + i * 1.0, 0.6)
        row_der_texts[i].set_alpha(e_d)

    limit_izq.set_alpha(su.eased(t, 6.6, 0.7))
    limit_der.set_alpha(su.eased(t, 7.0, 0.7))

    ec = su.eased(t, 8.2, 0.7)
    comp_left.set_alpha(ec)
    comp_mid.set_alpha(ec)
    comp_right.set_alpha(ec)

    econ = su.eased(t, 9.6, 0.7)
    conclusion.set_alpha(econ)
    conclusion.set_position((8, 1.85 - 0.08 * (1 - econ)))

    ecr = su.eased(t, 10.8, 0.5)
    cross.set_fontsize(10 + 60 * ecr)
    cross.set_alpha(ecr)

    if t > 10.0:
        pulse = 1.0 + 0.05 * np.sin((t - 10.0) * 1.5)
        comp_left.set_fontsize(34 * pulse)
        comp_right.set_fontsize(34 * pulse)

    return ([badge, badge_num, header, sub, divider, head_izq, head_der,
              limit_izq, limit_der, comp_left, comp_mid, comp_right, conclusion, cross]
             + row_izq_texts + row_der_texts)


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_05_condicion2 ->", OUT)
