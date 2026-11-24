import os
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'plot-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def box(ax,x,y,w,h,text,fc='#e9f3f6',edge='#366371',size=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.016,rounding_size=0.022',facecolor=fc,edgecolor=edge,lw=1.2))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,color='#15313c',linespacing=1.55)


def arrow(ax,x,y,x2,y2):ax.annotate('',xy=(x2,y2),xytext=(x,y),arrowprops={'arrowstyle':'->','color':'#527684','lw':1.4})


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    fig=plt.figure(figsize=(13,7),facecolor='#fafcfd');ax=fig.add_axes([0.035,0.08,0.93,0.82]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    fig.text(.04,.945,'Global accounting: an exact exclusion certificate',fontsize=19,weight='bold',color='#15313c')
    fig.text(.04,.903,'One fixed linear potential, ten full physical state features, any finite charging constant C.',fontsize=11,color='#52707c')
    box(ax,.02,.72,.285,.17,'If every original operation had\n'+r'$q_t+\Delta\Phi\leq C a_t$'+'\nexact pair closure would cancel Φ.')
    box(ax,.36,.72,.28,.17,'Inverse one-zig sources F1–F4\nforce depth and size terms to zero,\nand opposite cross coefficients.')
    arrow(ax,.315,.805,.345,.805)
    box(ax,.695,.72,.28,.17,'Restoration parity, unbounded p\nforces the remaining cross term\nto have coefficient zero.')
    arrow(ax,.65,.805,.68,.805)
    box(ax,.06,.39,.37,.16,'Complete restoration family\n'+r'$H_{p,5},\quad p\to\infty$'+'\nforces 2μ ≤ −1.',fc='#e9f4ef',edge='#43806c',size=12)
    box(ax,.57,.39,.37,.16,'Complete compressed burst family\n'+r'$\widehat H_{3,q},\quad q\to\infty$'+'\nforces −μ ≤ −1.',fc='#fbecef',edge='#ad5668',size=12)
    arrow(ax,.835,.70,.755,.565);arrow(ax,.5,.70,.245,.565)
    box(ax,.28,.10,.44,.17,'Exact nonnegative combination: first + 2 × second\n'+r'$0\leq -3$'+'\nNo coefficients in this declared span can work.',fc='#fff0d9',edge='#b48643',size=12)
    arrow(ax,.245,.37,.40,.285);arrow(ax,.755,.37,.60,.285)
    fig.text(.04,.035,'This excludes the specified per-operation potential architecture. Universal Coarse Double remains OPEN.',fontsize=11,weight='bold',color='#7a3244')
    fig.savefig(HERE/'global_accounting_certificate.png',dpi=180,facecolor=fig.get_facecolor())
    fig.savefig(HERE/'global_accounting_certificate.svg',facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__=='__main__':main()
