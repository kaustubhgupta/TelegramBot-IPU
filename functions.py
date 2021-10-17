import numpy as np
import matplotlib.pyplot as plt


def marksImage(data: list, user: str):

    fig_background_color = 'skyblue'
    fig_border = 'steelblue'

    column_headers = ['Int', 'Ext', 'Total', 'Grd']
    row_headers = [x.pop(0) for x in data]
    cell_text = data
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    plt.figure(linewidth=2,
               edgecolor=fig_border,
               facecolor=fig_background_color,
               #    tight_layout={'pad': 1},
               )
    the_table = plt.table(cellText=cell_text,
                          rowLabels=row_headers,
                          rowColours=rcolors,
                          rowLoc='right',
                          colColours=ccolors,
                          colLabels=column_headers,
                          loc='center')
    the_table.scale(1, 1.5)
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.box(on=None)
    fig = plt.gcf()
    plt.savefig(f'marks_image_{user}.png',
                # bbox='tight',
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=150,
                bbox_inches='tight'
                )
