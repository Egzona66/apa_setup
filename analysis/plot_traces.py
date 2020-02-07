# %%
import sys
sys.path.append('./')

import matplotlib.pyplot as plt
import os
import seaborn as sns

from fcutils.file_io.utils import check_file_exists
from fcutils.plotting.colors import salmon
from fcutils.plotting.utils import set_figure_subplots_aspect

# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #

# --------------------------------- Load data -------------------------------- #
# main_fld = "D:\\Egzona\\2020"
# savepath = os.path.join(main_fld, "data.hdf")
# check_file_exists(savepath, raise_error=True)
# data = pd.read_hdf(savepath, key='hdf')

sensors = ['fr', 'fl', 'hr', 'hl']

# --------------------------------- Variables -------------------------------- #
calibrated_data = True # Set as true if the data are calibrated Volts -> Grams
plot_centered_CoG = False # if true the centered CoG is used (all trials starts at 0,0)


# %%

# ------------------------------- Create figure ------------------------------ #
f = plt.figure(figsize=(20, 14))

grid = (5, 7)
axes = {}
axes['CoG'] = plt.subplot2grid(grid, (1, 0), rowspan=2, colspan=3)
axes['fr'] = plt.subplot2grid(grid, (0, 4), colspan=3)
axes['fl'] = plt.subplot2grid(grid, (1, 4), colspan=3, sharex=axes['fr'])
axes['hr'] = plt.subplot2grid(grid, (2, 4),  colspan=3, sharex=axes['fr'])
axes['hl'] = plt.subplot2grid(grid, (3, 4),  colspan=3, sharex=axes['fr'])

# Style axes
for ch in ['fr', 'fl', 'hr']:
    axes[ch].set(xticks=[])
    
sns.despine(offset=10)
for title, ax in axes.items():
    ax.set(title=title.upper())

# %%
# -------------------------- Plot individual trials -------------------------- #
for trn, row in data.iterrows():
    for ch in sensors:
        if trn == 0:
            label='trials'
        else:
            label=None
        axes[ch].plot(trial[ch].values, color=k, alpha=.4, lw=2, ls='--', label=label)

    

# --------------------------- Plot sensors medians --------------------------- #
# TODO find how data are stored in df and take medians
medians = {ch:XXX for ch in sensors}

for ch in sensors:
    axes[ch].plot(medians[ch], color=salmon, lw=4, label='median')

# --------------------------------- Plot CoG --------------------------------- #
if plot_centered_CoG:
    CoG = data['centered_CoG']
else:
    CoG = data['CoG']

median_CoG = XXX
time = np.arange(len(CoG))
cgax.scatter(median_CoG[:, 0], median_CoG[:, 1], c=time, 
                alpha=1, cmap="Reds")



# -------------------------------- Style plots ------------------------------- #
for ch in sensors:
    axes[ch].legend()

    if calibrated_data:
        ylabel = '$g$'
    else:
        ylabel = '$V$'
    axes[ch].set(ylabel=ylabel)

    
# TODO style x ticks to go from frames to time
# Style figures and axes

# %%