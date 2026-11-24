"""Scientific proof diagram of the exact fixed-priority coarsening leak."""
import os
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'mpl_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    fig=plt.figure(figsize=(13,6.8),facecolor='#f6f8fc');gs=fig.add_gridspec(1,2,width_ratios=[1.15,1],left=.065,right=.96,top=.77,bottom=.21,wspace=.28)
    ax=fig.add_subplot(gs[0]);roles=['Target','External\ncarry','Next left\nroot','Retired\nroot','Parent\ncarry','Next spine\nroot'];vals=[8,8,8,8,8,7];colors=['#627895','#627895','#13887d','#cf5a52','#627895','#7953b3']
    ax.bar(range(6),vals,color=colors,width=.68,zorder=3);ax.set_ylim(0,9.4);ax.set_xticks(range(6),roles,fontsize=9);ax.set_yticks([0,2,4,6,8]);ax.set_ylabel('Credits after one RR step');ax.set_title('One unit paid; the retired root stays full',loc='left',fontsize=12,pad=18,fontweight='bold')
    for j,v in enumerate(vals):ax.text(j,v+.15,str(v),ha='center',fontsize=12,fontweight='bold',color=colors[j])
    ax.axhline(8,color='#8a96a9',linestyle='--',lw=.9,zorder=2);ax.text(3,8.9,'retired ≥ persistent',ha='center',fontsize=10,color='#9a3b36')
    ax.grid(axis='y',color='#dbe2ee',zorder=0);ax.set_axisbelow(True)
    ar=fig.add_subplot(gs[1]);H=8;a=b=H;mass=[2*a+b]
    while mass[-1]>=1:
        I=2*a+b;a,b=max(0,I-2*H-1),min(H,I-1);mass.append(2*a+b)
    ar.plot(range(len(mass)),mass,color='#7953b3',lw=2.6,marker='o',ms=4.5);ar.fill_between(range(len(mass)),mass,color='#7953b3',alpha=.09)
    ar.set_xlabel('Coarsening steps after the base phase');ar.set_ylabel('Reusable profile bound  M = 2a + b');ar.set_title('The exact upper-profile recurrence, H = 8',loc='left',fontsize=12,pad=18,fontweight='bold');ar.grid(color='#dbe2ee',lw=.7);ar.set_ylim(-.5,26);ar.set_xlim(-.2,len(mass)-.8)
    ar.text(5.3,18.8,r'$M_{j+1}\leq M_j-1$'+'\nwhile '+r'$M_j\geq 1$',fontsize=13,color='#49356e');ar.annotate('No fresh credit remains\nfor a long interior packet',xy=(len(mass)-1,0),xytext=(4.8,10.5),fontsize=10,arrowprops={'arrowstyle':'->','color':'#7953b3'},color='#49356e',bbox={'facecolor':'white','edgecolor':'none','alpha':.86,'pad':3})
    for axy in (ax,ar):
        axy.set_facecolor('#ffffff');axy.spines[['top','right']].set_visible(False);axy.spines[['left','bottom']].set_color('#a9b4c4');axy.tick_params(colors='#38465a')
    fig.text(.065,.935,'A cyclic bank can close and still fail to pay',fontsize=21,fontweight='bold',color='#24324a')
    fig.text(.065,.875,'The fixed priority stores credit in roots that leave the later coarsening path.',fontsize=12,color='#52627c')
    fig.text(.065,.105,'For every finite capacity, a complete original H-source supplies enough scales and a longer dry packet.',fontsize=11,color='#38465a')
    fig.text(.065,.055,'This refutes the frozen transfer law. Universal Coarse Double remains OPEN.',fontsize=11,fontweight='bold',color='#9a3b36')
    fig.savefig(HERE/'physical_bank_stranding_v2.png',dpi=165,facecolor=fig.get_facecolor());fig.savefig(HERE/'physical_bank_stranding_v2.svg',facecolor=fig.get_facecolor());plt.close(fig)
    print('Created exact-recurrence proof diagram; no finite-coverage chart.')


if __name__=='__main__':main()
