"""Table serialization and chart style shared by research reports.

These helpers do not load study inputs, select samples or write artifacts.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUE, ORANGE = "#2a78d6", "#eb6834"


def to_markdown(df: pd.DataFrame, index_name: str = "") -> str:
    header = "| " + " | ".join([index_name] + [str(c) for c in df.columns]) + " |"
    sep = "|" + "---|" * (len(df.columns) + 1)
    body = ["| " + " | ".join([str(i)] + [str(v) for v in r]) + " |" for i, r in zip(df.index, df.values)]
    return "\n".join([header, sep, *body])



def to_latex(df: pd.DataFrame, caption: str) -> str:
    esc = lambda s: str(s).replace("%", r"\%").replace("&", r"\&").replace("$", r"\$").replace("_", r"\_")
    lines = [
        r"\begin{table}[htbp]\centering\small",
        rf"\caption{{{esc(caption)}}}",
        r"\begin{tabular}{l" + "r" * len(df.columns) + "}",
        r"\hline",
        " & ".join([""] + [esc(c) for c in df.columns]) + r" \\",
        r"\hline",
        *(" & ".join([esc(i)] + [esc(v) for v in r]) + r" \\" for i, r in zip(df.index, df.values)),
        r"\hline",
        r"\end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)



def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(SURFACE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelcolor=INK2, length=0, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)



def pct_axis(ax: plt.Axes, axis: str = "y") -> None:
    fmtr = matplotlib.ticker.FuncFormatter(lambda v, _: f"{100 * v:.0f}%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmtr)



def new_fig(*args, **kw):
    fig, ax = plt.subplots(*args, **kw)
    fig.patch.set_facecolor(SURFACE)
    return fig, ax

