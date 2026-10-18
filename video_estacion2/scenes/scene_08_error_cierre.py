"""Escena 8 - Error detectado y cierre (~30 s)
Tarjeta "Error detectado", tarjeta "Conclusión correcta" y cierre "¡Gracias por ver!".
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import scene_utils as su
from matplotlib.animation import FuncAnimation
import numpy as np

DURATION = 30.0
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "scene_08_error_cierre.mp4")

fig, ax = su.make_figure()

title = ax.text(8, 8.5, "Error detectado", **su.title_kwargs(size=30), ha="center",
                 va="center", alpha=0, zorder=10)

# --- Tarjeta 1: error común ---
C1X, C1Y = 8.0, 6.55
C1W, C1H = 13.4, 2.7
card1 = su.rounded_card(ax, C1X, C1Y, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.14, zorder=4)

err_label = ax.text(C1X, C1Y + 1.02, "⚠  Error común", ha="center", va="center",
                     fontsize=18, color=su.RED, fontfamily=su.BODY_FONT,
                     fontweight="bold", alpha=0, zorder=7)
err_wrong = ax.text(C1X, C1Y + 0.38, "“El límite da infinito, entonces la función es continua”",
                     ha="center", va="center", fontsize=16.5, color=su.TEXT_MUTED,
                     fontfamily=su.BODY_FONT, style="italic", alpha=0, zorder=7)
err_strike, = ax.plot([C1X - 4.8, C1X + 4.8], [C1Y + 0.38, C1Y + 0.38], color=su.RED,
                       lw=2.0, alpha=0, zorder=8)

err_right_label = ax.text(C1X, C1Y - 0.32, "✓  En realidad", ha="center", va="center",
                           fontsize=17, color=su.GREEN, fontfamily=su.BODY_FONT,
                           fontweight="bold", alpha=0, zorder=7)
err_right = ax.text(C1X, C1Y - 0.95,
                     "Un límite infinito o inexistente significa que la función NO es continua",
                     ha="center", va="center", fontsize=15.5, color=su.TEXT_LIGHT,
                     fontfamily=su.BODY_FONT, alpha=0, zorder=7)

# --- Tarjeta 2: conclusión correcta ---
C2X, C2Y = 8.0, 3.35
C2W, C2H = 13.4, 2.2
card2 = su.rounded_card(ax, C2X, C2Y, 0.02, 0.02, facecolor=su.CARD_BG, radius=0.14, zorder=4)
ok_label = ax.text(C2X, C2Y + 0.72, "✓  Conclusión correcta", ha="center", va="center",
                    fontsize=18, color=su.GREEN, fontfamily=su.BODY_FONT,
                    fontweight="bold", alpha=0, zorder=7)
ok_line1 = ax.text(C2X, C2Y + 0.1, "h(x) es discontinua en x = 2", ha="center", va="center",
                    fontsize=18, color=su.TEXT_LIGHT, fontfamily=su.BODY_FONT,
                    fontweight="bold", alpha=0, zorder=7)
ok_line2 = ax.text(C2X, C2Y - 0.55,
                    "Discontinuidad inevitable de salto infinito  (asíntota vertical en x = 2)",
                    ha="center", va="center", fontsize=15, color=su.GOLD,
                    fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=7)

# --- Cierre ---
thanks = ax.text(8, 1.3, "¡Gracias por ver!", ha="center", va="center", fontsize=10,
                  color=su.TURQUOISE, fontfamily=su.TITLE_FONT, fontweight="bold",
                  alpha=0, zorder=10)

names = ["Sofía", "Micaela", "Fabrizio", "Jerónimo"]
colors = [su.TURQUOISE, su.ORANGE, su.VIOLET, su.GOLD]
xs = [4.6, 7.2, 9.8, 12.4]
name_texts = [ax.text(nx, 0.45, nm, ha="center", va="center", fontsize=14.5,
                       color=c, fontfamily=su.BODY_FONT, fontweight="bold", alpha=0, zorder=10)
              for nx, nm, c in zip(xs, names, colors)]


def update(frame):
    t = su.frame_time(frame)

    title.set_alpha(su.eased(t, 0.2, 0.7))

    ec1 = su.eased(t, 1.1, 0.8)
    su.set_card_bounds(card1, C1X, C1Y, max(0.02, C1W * ec1), max(0.02, C1H * ec1))

    err_label.set_alpha(su.eased(t, 2.0, 0.6))
    err_wrong.set_alpha(su.eased(t, 2.7, 0.6))
    est = su.eased(t, 3.6, 0.5)
    err_strike.set_data([C1X - 4.8 * est, C1X + 4.8 * est], [C1Y + 0.38, C1Y + 0.38])
    err_strike.set_alpha(est)

    err_right_label.set_alpha(su.eased(t, 4.4, 0.6))
    err_right.set_alpha(su.eased(t, 5.1, 0.7))

    ec2 = su.eased(t, 7.0, 0.8)
    su.set_card_bounds(card2, C2X, C2Y, max(0.02, C2W * ec2), max(0.02, C2H * ec2))
    ok_label.set_alpha(su.eased(t, 7.9, 0.6))
    ok_line1.set_alpha(su.eased(t, 8.6, 0.6))
    ok_line2.set_alpha(su.eased(t, 9.3, 0.7))

    eth = su.eased(t, 11.0, 0.9)
    thanks.set_fontsize(10 + 30 * eth)
    thanks.set_alpha(eth)

    for i, nt in enumerate(name_texts):
        e = su.eased(t, 12.2 + i * 0.18, 0.6)
        nt.set_alpha(e)
        nt.set_position((xs[i], 0.45 + 0.1 * (1 - e)))

    if t > 12.2:
        pulse = 1.0 + 0.03 * np.sin((t - 12.2) * 1.4)
        thanks.set_fontsize(40 * pulse)

    return ([title, card1, err_label, err_wrong, err_strike, err_right_label, err_right,
              card2, ok_label, ok_line1, ok_line2, thanks] + name_texts)


if __name__ == "__main__":
    anim = FuncAnimation(fig, update, frames=su.n_frames(DURATION), blit=False)
    su.save_scene(fig, anim, OUT)
    print("OK scene_08_error_cierre ->", OUT)
