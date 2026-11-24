"""Scientific plot of proved parametric formulas, not empirical fitting."""
import os
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'plot-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    s=list(range(1,65))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(1,2,figsize=(11.4,4.5),layout='constrained')
    fig.suptitle('Whole-period cover changes cannot supply a universal load bound',fontsize=15,fontweight='bold')
    ax[0].plot(s,[v*v for v in s],color='#167d8d',lw=2.5,label=r'Original demands: $s^2$')
    ax[0].plot(s,[8*v for v in s],color='#d08821',lw=2.5,label=r'Eligible A units: $8s$')
    ax[0].set(xlabel=r'Family parameter $p=q=s$',ylabel='Exact count',title='A complete source at every integer s')
    ax[0].legend(frameon=False,loc='upper left')
    ax[1].step(s,[(v+7)//8 for v in s],where='post',color='#8851a6',lw=2.7)
    ax[1].set(xlabel=r'Family parameter $p=q=s$',ylabel='Minimum integer load per A unit',title=r'Exact selected-demand optimum: $\lceil s/8\rceil$')
    ax[1].scatter([9],[2],s=45,color='#167d8d',zorder=4)
    ax[1].annotate('Independently replayed source\ns = 9: 81 demands, 72 units',xy=(9,2),xytext=(14,1.2),fontsize=9,arrowprops={'arrowstyle':'-','color':'#666666'})
    for a in ax:
        a.grid(axis='y',alpha=.17)
        a.set_xlim(1,64)
    fig.supxlabel('Parametric proof: for every finite K, choose s > 8K. Universal CD itself remains open.',fontsize=10)
    fig.savefig(HERE/'cover_policy_obstruction.png',dpi=180)
    fig.savefig(HERE/'cover_policy_obstruction.svg')


if __name__=='__main__':
    main()
