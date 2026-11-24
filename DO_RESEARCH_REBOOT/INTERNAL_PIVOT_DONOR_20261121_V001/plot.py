"""Full original 17-key snapshot illustration, with no tree contraction."""
import json
import os
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'plot-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    record=json.loads((HERE/'SHORTCUT_SNAPSHOTS.json').read_text());a,b=record['frame']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,axes=plt.subplots(1,3,figsize=(14.4,7.2))
    fig.subplots_adjust(left=.025,right=.99,top=.87,bottom=.18,wspace=.1)
    fig.suptitle('Touching the frame does not make an A step eligible',fontsize=16,fontweight='bold')
    titles=['Before A(21,5,0)','After bit 0: promote 10 over 11','After bit 1: promote 1 over 10']
    for idx,(ax,s,title) in enumerate(zip(axes,record['snapshots'],titles)):
        children={int(k):v for k,v in s['children'].items()};depth={};stack=[(s['root'],0)]
        while stack:
            k,d=stack.pop();depth[k]=d
            stack.extend((c,d+1) for c in children[k] if c is not None)
        pair=(11,10) if idx==0 else (10,1) if idx==1 else None
        for k,cs in children.items():
            for c in cs:
                if c is not None:
                    highlight=pair==(k,c)
                    ax.plot([k,c],[-depth[k],-depth[c]],color='#db7938' if highlight else '#aab2bb',lw=3 if highlight else 1.2,zorder=1)
        for k in sorted(children):
            color='#238a9c' if a<=k<=b else '#dce1e6'
            ax.scatter([k],[-depth[k]],s=210,c=color,edgecolor='#ad7f13' if k==14 else 'white',linewidth=2.6 if k==14 else .8,zorder=3)
            ax.text(k,-depth[k],str(k),ha='center',va='center',fontsize=8,color='white' if a<=k<=b else '#323b44',zorder=4)
        ax.set_title(title,fontsize=11);ax.set_xlim(.1,17.9);ax.set_ylim(-max(depth.values())-.7,.8);ax.axis('off')
        ax.text(.02,.97,'LCA(11,16) = 14\ncover = [1,17]',transform=ax.transAxes,ha='left',va='top',fontsize=11,color='#6a531d')
    fig.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor='#238a9c',markersize=9,label='Frame keys 11 through 16'),Line2D([0],[0],color='#db7938',lw=3,label='Next rotating pair'),Line2D([0],[0],marker='o',color='w',markerfacecolor='#238a9c',markeredgecolor='#ad7f13',markeredgewidth=2,markersize=9,label='Unchanged LCA 14')],loc='lower center',bbox_to_anchor=(.5,.065),ncol=3,frameon=False)
    fig.supxlabel('Complete W_2,1 source: A=65, Q_B=24. Original demand (18,1); original A unit (21,5).',fontsize=10,y=.025)
    fig.savefig(HERE/'rejected_pivot_shortcut.png',dpi=180,bbox_inches='tight')
    fig.savefig(HERE/'rejected_pivot_shortcut.svg',bbox_inches='tight')


if __name__=='__main__':main()
