from matplotlib import cm
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import pandas as pd
# Import seaborn
import seaborn as sns
from matplotlib.transforms import TransformedBbox


def annotate_yranges(groups, ax=None):
    """
    Annotate a group of consecutive yticklabels with a group name.

    Arguments:
    ----------
    groups : dict
        Mapping from group label to an ordered list of group members.
    ax : matplotlib.axes object (default None)
        The axis instance to annotate.
    """
    if ax is None:
        ax = plt.gca()

    label2obj = {ticklabel.get_text() : ticklabel for ticklabel in ax.get_yticklabels()}

    for ii, (group, members) in enumerate(groups.items()):
        first = members[0]
        last = members[-1]

        bbox0 = _get_text_object_bbox(label2obj[first], ax)
        bbox1 = _get_text_object_bbox(label2obj[last], ax)

        set_yrange_label(group, bbox0.y0 + bbox0.height/2,
                         bbox1.y0 + bbox1.height/2,
                         min(bbox0.x0, bbox1.x0),
                         -2,
                         ax=ax)


def set_yrange_label(label, ymin, ymax, x, dx=-0.5, ax=None, *args, **kwargs):
    """
    Annotate a y-range.

    Arguments:
    ----------
    label : string
        The label.
    ymin, ymax : float, float
        The y-range in data coordinates.
    x : float
        The x position of the annotation arrow endpoints in data coordinates.
    dx : float (default -0.5)
        The offset from x at which the label is placed.
    ax : matplotlib.axes object (default None)
        The axis instance to annotate.
    """

    if not ax:
        ax = plt.gca()

    dy = ymax - ymin
    props = dict(connectionstyle='angle, angleA=90, angleB=180, rad=0',
                 arrowstyle='-',
                 shrinkA=10,
                 shrinkB=10,
                 lw=1)
    ax.annotate(label,
                xy=(x, ymin),
                xytext=(x + dx, ymin + dy/2),
                annotation_clip=False,
                arrowprops=props,
                *args, **kwargs,
    )
    ax.annotate(label,
                xy=(x, ymax),
                xytext=(x + dx, ymin + dy/2),
                annotation_clip=False,
                arrowprops=props,
                *args, **kwargs,
    )

def _get_text_object_bbox(text_obj, ax):
    # https://stackoverflow.com/a/35419796/2912349
    transform = ax.transData.inverted()
    # the figure needs to have been drawn once, otherwise there is no renderer?
    plt.ion(); plt.show(); plt.pause(0.001)
    bb = text_obj.get_window_extent(renderer = ax.get_figure().canvas.renderer)
    # handle canvas resizing
    return TransformedBbox(bb, transform)

# Apply the default theme
sns.set_theme()
df = pd.read_pickle("exp2_df")


x = df.explode('Spearman').reset_index()
grouped_df = df.groupby(["Algorithm","dim","Effective dim", "Samples"], as_index=False)
df_mean = grouped_df.mean()#.groupby('Seed').mean()


plotdf = df_mean.pivot(index=["Effective dim","dim","Algorithm"], columns='Samples', values='Spearman')
#sns.set(rc = {'figure.figsize':(8,12)})
sns.heatmap(plotdf, cmap="RdYlGn", xticklabels=1, yticklabels=1, vmin=-1, vmax=1)
plt.tight_layout()
plt.savefig("spearman-per-samplesize.png")
plt.clf()

plotdf = df_mean.pivot(index=["Effective dim","dim","Algorithm"], columns='Samples', values='Time')
sns.heatmap(plotdf, cmap="coolwarm")
plt.tight_layout()
plt.savefig("time-per-samplesize.png")
plt.clf()

grouped_df = df.groupby(["Algorithm","dim","Effective dim"], as_index=False)
df_mean2 = grouped_df.mean()#.groupby('Seed').mean()

plotdf = df_mean2.pivot(index="Algorithm", columns='dim', values='Spearman')
#sns.set(rc = {'figure.figsize':(6,6)})
sns.heatmap(plotdf, cmap="RdYlGn", xticklabels=1, yticklabels=1, vmin=-1, vmax=1)
plt.tight_layout()
plt.savefig("spearman-per-dim.png")
plt.clf()

plotdf = df_mean2.pivot(index="Algorithm", columns='dim', values='Time')
sns.heatmap(plotdf, cmap="coolwarm")
plt.tight_layout()
plt.savefig("time-per-dim.png")
plt.clf()