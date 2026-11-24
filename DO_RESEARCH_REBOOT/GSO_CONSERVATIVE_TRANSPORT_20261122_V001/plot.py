"""Scientific illustration of proved local retention and warmup identities."""
import os
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'mpl_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed checkpoint'
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(13.6,6.2),gridspec_kw={'width_ratios':[1.15,1]})
    old=np.array([8,8,8,8,8,7]);new=np.array([8,8,8,7,8,8]);x=np.arange(6)
    axes[0].bar(x-.19,old,.36,label='Old rank priority',color='#8798ae')
    axes[0].bar(x+.19,new,.36,label='Selected structural priority',color=['#246bce']*3+['#d9667a','#246bce','#159e84'])
    axes[0].set_xticks(x,['Target','External','Grandparent','Retiring\nroot','Parent','Persistent\nroot'])
    axes[0].set_ylim(0,10.4);axes[0].set_ylabel('Credit after one double')
    axes[0].set_title('Full-input template: redirect the one-credit loss',loc='left',fontweight='bold',pad=20)
    axes[0].text(.02,.89,'H = 8; both rules conserve 47 remaining credits',transform=axes[0].transAxes,color='#40536b')
    axes[0].text(.02,.81,'Reusable profile: old 22; selected rule 24',transform=axes[0].transAxes,color='#40536b')
    axes[0].legend(loc='upper center',bbox_to_anchor=(.5,-.17),ncol=2,frameon=False,fontsize=9)
    for i in (3,5):
        axes[0].text(x[i]-.19,old[i]+.12,str(old[i]),ha='center',fontsize=9)
        axes[0].text(x[i]+.19,new[i]+.12,str(new[i]),ha='center',fontsize=9)
    steps=list(range(11));target=[min(5,k) for k in steps];persistent=[0 if k<=5 else 1 for k in steps]
    axes[1].plot(steps,target,'o-',lw=2.5,color='#246bce',label='Target reserve')
    axes[1].step(steps,persistent,where='post',lw=2.5,color='#159e84',label='Persistent-root output')
    axes[1].set_ylim(-.25,7.5);axes[1].set_xlim(-.2,10.2)
    axes[1].set_xlabel('Consecutive certified doubles');axes[1].set_ylabel('Credit')
    axes[1].set_title('Weaker entry: two spine credits rebuild the reserve',loc='left',fontweight='bold',pad=20)
    axes[1].text(.03,.89,'H = 5; initial target/carry = 0',transform=axes[1].transAxes,color='#40536b')
    axes[1].text(.03,.81,'Each step: two fresh spine banks supply >= 1 each',transform=axes[1].transAxes,color='#40536b')
    axes[1].legend(loc='center right',frameon=False)
    for axis in axes:axis.grid(axis='y',alpha=.15);axis.set_axisbelow(True)
    fig.suptitle('A local renewal rule is proved; its global entry condition remains open',fontsize=17,fontweight='bold',x=.06,ha='left',y=.98)
    fig.text(.06,.035,'Exact local examples. The theorems cover arbitrary capacity H >= 1 in this template; they do not establish Universal CD.',fontsize=10,color='#40536b')
    fig.subplots_adjust(left=.06,right=.98,bottom=.24,top=.80,wspace=.30)
    for suffix in ('png','svg'):fig.savefig(HERE/f'conservative_spine_renewal_v2.{suffix}',dpi=160,facecolor='white')
    print({'figure':'conservative_spine_renewal_v2.png','scope':'Proved local identities; global bound OPEN'})


if __name__=='__main__':main()
