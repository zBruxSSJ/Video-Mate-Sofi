"""
Módulo compartido para las escenas del video "Estación 2 - Caso de Estudio".
Paleta de colores, fuentes, helpers de glow, tarjetas, easing y guardado.

Sistema de coordenadas de los ejes principales: x en [0, 16], y en [0, 9]
(proporción 16:9, independiente de la resolución final).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.animation import FFMpegWriter
import numpy as np

# ---------------------------------------------------------------------------
# Resolución / tiempo
# ---------------------------------------------------------------------------
FPS = 24
WIDTH_PX = 1280
HEIGHT_PX = 720
DPI = 100
FIGSIZE = (WIDTH_PX / DPI, HEIGHT_PX / DPI)  # (12.8, 7.2)

X0, X1 = 0.0, 16.0
Y0, Y1 = 0.0, 9.0

# ---------------------------------------------------------------------------
# Paleta
# ---------------------------------------------------------------------------
BG_TOP = "#150c28"
BG_BOTTOM = "#341a57"

TURQUOISE = "#4cc9f0"   # celeste (antes turquesa)
ORANGE = "#ff8c42"      # coral/ámbar (antes naranja)
RED = "#ff3b5c"         # carmesí (error)
GREEN = "#06d6a0"       # verde esmeralda (correcto)
VIOLET = "#c77dff"      # orquídea (antes violeta lavanda)
GOLD = "#ffd166"        # amarillo dorado (antes dorado más opaco)

TEXT_LIGHT = "#f5eeff"
TEXT_MUTED = "#b7a6d6"
CARD_BG = "#3f2566"
CARD_BG_SOFT = "#2a1845"

PALETTE = {
    "turquoise": TURQUOISE,
    "orange": ORANGE,
    "red": RED,
    "green": GREEN,
    "violet": VIOLET,
    "gold": GOLD,
}

# Colores por integrante (para referencia cruzada con el guion)
PERSON_COLORS = {
    "Sofía": TURQUOISE,
    "Micaela": ORANGE,
    "Fabrizio": VIOLET,
    "Jerónimo": GOLD,
}

# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------
FONT_TITLE = "Poppins"
FONT_TITLE_BOLD = "Poppins"
FONT_BODY = "Inter"


def _font_available(name):
    names = {f.name for f in fm.fontManager.ttflist}
    return name in names


TITLE_FONT = FONT_TITLE if _font_available(FONT_TITLE) else "DejaVu Sans"
BODY_FONT = FONT_BODY if _font_available(FONT_BODY) else "DejaVu Sans"

plt.rcParams["font.family"] = BODY_FONT
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.default"] = "regular"
plt.rcParams["mathtext.it"] = f"{BODY_FONT}:italic"
plt.rcParams["mathtext.rm"] = BODY_FONT
plt.rcParams["mathtext.bf"] = f"{BODY_FONT}:bold"
plt.rcParams["axes.unicode_minus"] = False


def title_kwargs(size=44, color=TEXT_LIGHT, weight="bold"):
    return dict(fontfamily=TITLE_FONT, fontsize=size, color=color, fontweight=weight)


def body_kwargs(size=22, color=TEXT_LIGHT, weight="normal"):
    return dict(fontfamily=BODY_FONT, fontsize=size, color=color, fontweight=weight)


# ---------------------------------------------------------------------------
# Easing
# ---------------------------------------------------------------------------
def clamp01(t):
    return max(0.0, min(1.0, t))


def ease_out_cubic(t):
    t = clamp01(t)
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t):
    t = clamp01(t)
    if t < 0.5:
        return 4 * t ** 3
    return 1 - ((-2 * t + 2) ** 3) / 2


def progress(t, start, dur):
    """Progreso lineal 0..1 entre start y start+dur (segundos)."""
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return clamp01((t - start) / dur)


def eased(t, start, dur, ease=ease_out_cubic):
    return ease(progress(t, start, dur))


# ---------------------------------------------------------------------------
# Figura / fondo degradado
# ---------------------------------------------------------------------------
def make_figure():
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_facecolor(BG_TOP)

    # Eje de fondo con el degradado vertical (detrás de todo)
    bg_ax = fig.add_axes([0, 0, 1, 1])
    bg_ax.set_xlim(0, 1)
    bg_ax.set_ylim(0, 1)
    bg_ax.axis("off")
    bg_ax.set_zorder(-100)

    top_rgb = np.array(matplotlib.colors.to_rgb(BG_TOP))
    bot_rgb = np.array(matplotlib.colors.to_rgb(BG_BOTTOM))
    n = 256
    grad = np.linspace(0, 1, n).reshape(n, 1)
    img = (top_rgb * (1 - grad) + bot_rgb * grad).reshape(n, 1, 3)
    # imshow dibuja fila 0 arriba por defecto -> fila 0 = color top
    bg_ax.imshow(img, extent=[0, 1, 0, 1], aspect="auto", origin="upper", zorder=-100)

    # Eje principal de contenido (coordenadas 0..16 x 0..9)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    ax.axis("off")
    ax.set_facecolor("none")
    ax.set_zorder(1)

    return fig, ax


# ---------------------------------------------------------------------------
# Tarjetas redondeadas (relleno sólido, sin alpha en el parche)
# ---------------------------------------------------------------------------
def rounded_card(ax, cx, cy, w, h, facecolor=CARD_BG, edgecolor=None,
                  lw=0, radius=0.12, zorder=5):
    """Tarjeta redondeada centrada en (cx, cy). Color sólido (sin alpha)."""
    x = cx - w / 2
    y = cy - h / 2
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor if edgecolor else "none",
        linewidth=lw,
        zorder=zorder,
        mutation_aspect=1,
    )
    ax.add_patch(patch)
    return patch


def set_card_bounds(patch, cx, cy, w, h):
    """Actualiza una tarjeta ya creada, centrada en (cx, cy)."""
    x = cx - w / 2
    y = cy - h / 2
    patch.set_bounds(x, y, w, h)


def card_pop_scale(t, start, dur, overshoot=1.0):
    """Factor de escala 0..overshoot..1 tipo 'pop' con ease-out cubic."""
    e = eased(t, start, dur)
    return e


# ---------------------------------------------------------------------------
# Glow para curvas
# ---------------------------------------------------------------------------
def glow_plot(ax, xs, ys, color, lw=3.0, n_layers=4, zorder=3, alpha_core=1.0):
    """Dibuja una curva con efecto glow (varias capas, alpha decreciente).
    Devuelve la lista de Line2D artists (de más ancha/tenue a más fina/sólida),
    para poder actualizarlas luego con set_data.
    """
    lines = []
    for i in range(n_layers, 0, -1):
        width = lw + i * lw * 1.1
        alpha = 0.06 * (n_layers - i + 1)
        ln, = ax.plot(xs, ys, color=color, linewidth=width, alpha=alpha,
                       solid_capstyle="round", zorder=zorder)
        lines.append(ln)
    core, = ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha_core,
                     solid_capstyle="round", zorder=zorder + 1)
    lines.append(core)
    return lines


def glow_update(lines, xs, ys):
    for ln in lines:
        ln.set_data(xs, ys)


def glow_set_visible(lines, visible):
    for ln in lines:
        ln.set_visible(visible)


# ---------------------------------------------------------------------------
# Marcas de check / cruz animadas
# ---------------------------------------------------------------------------
def mark_check(ax, cx, cy, t, start, dur, size=34, color=GREEN):
    e = eased(t, start, dur)
    if e <= 0:
        return None
    fs = size * (0.5 + 0.5 * e)
    return ax.text(cx, cy, "✓", ha="center", va="center",
                    fontsize=fs, color=color, alpha=e,
                    fontfamily=BODY_FONT, fontweight="bold", zorder=20)


def mark_cross(ax, cx, cy, t, start, dur, size=34, color=RED):
    e = eased(t, start, dur)
    if e <= 0:
        return None
    fs = size * (0.5 + 0.5 * e)
    return ax.text(cx, cy, "✗", ha="center", va="center",
                    fontsize=fs, color=color, alpha=e,
                    fontfamily=BODY_FONT, fontweight="bold", zorder=20)


# ---------------------------------------------------------------------------
# Guardado de animación
# ---------------------------------------------------------------------------
def save_scene(fig, anim, out_path, fps=FPS, bitrate=6000):
    writer = FFMpegWriter(fps=fps, bitrate=bitrate, codec="libx264",
                           extra_args=["-pix_fmt", "yuv420p"])
    anim.save(out_path, writer=writer, dpi=DPI)
    plt.close(fig)


def n_frames(duration_s, fps=FPS):
    return int(round(duration_s * fps))


def frame_time(frame, fps=FPS):
    return frame / fps
