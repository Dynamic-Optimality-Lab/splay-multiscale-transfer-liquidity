import os
from pathlib import Path
HERE=Path(__file__).resolve().parent;os.environ['MPLCONFIGDIR']=str(HERE/'plot-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from kernel import load


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    summary=load(HERE/'run_001/GRAPH_SUMMARY.json')['cases'];fig=plt.figure(figsize=(12.5,6.2),facecolor='#fafcfd')
    a=fig.add_axes([.075,.30,.37,.46]);a.set_facecolor('#fafcfd')
    x=[r['support'] for r in summary];y=[float(__import__('fractions').Fraction(r['exact_finite_C'])) for r in summary]
    a.plot(x,y,'o-',color='#307b83',lw=2,ms=7);a.set(xticks=x,yticks=[0,.5,1,1.5,2],ylim=(-.1,2),xlabel='Physical key count',ylabel='Exact optimum finite constant C_n')
    a.grid(axis='y',alpha=.2);a.spines[['top','right']].set_visible(False)
    a.set_title('Complete finite-state teacher',loc='left',weight='bold',pad=15)
    for xx,yy,label in zip(x,y,['0','0','1','1','3/2','3/2']):a.annotate(label,(xx,yy),xytext=(0,10),textcoords='offset points',ha='center',color='#22525e')
    fig.text(.075,.14,'Exact potential certificates; attaining cycles for positive optima.\nNo bound at larger support is inferred.',fontsize=10,color='#45616b')
    b=fig.add_axes([.52,.18,.44,.63]);b.axis('off');b.set(xlim=(0,1),ylim=(0,1))
    def box(y,text,face,edge):
        b.add_patch(FancyBboxPatch((.03,y),.91,.17,boxstyle='round,pad=0.015',facecolor=face,edgecolor=edge,lw=1.2));b.text(.485,y+.085,text,ha='center',va='center',fontsize=11,color='#18333f',linespacing=1.45)
    box(.75,'Seven complete-source templates\nproduce universal necessary constraints.','#e9f3f6','#507e8b')
    box(.43,'Exact proof-core optimization\nfive templates suffice among the recorded seven.','#e9f4ef','#43806c')
    box(.11,'Nonnegative dual combination:  0 ≤ −1\nBoth declared frontier grammars are excluded.','#fff0d9','#b48643')
    for y1,y2 in [(.73,.62),(.41,.30)]:b.annotate('',xy=(.485,y2),xytext=(.485,y1),arrowprops={'arrowstyle':'->','color':'#527684','lw':1.4})
    fig.text(.06,.92,'GSO version 1: exact teachers and symbolic pruning',fontsize=19,weight='bold',color='#15313c')
    fig.text(.06,.855,'A working bounded research engine. Every universal conclusion keeps its precise proof scope.',fontsize=11,color='#52707c')
    fig.text(.06,.045,'Universal Coarse Double remains OPEN. The obstruction concerns the specified whole-operation potential family.',fontsize=11,weight='bold',color='#7a3244')
    for ext in ('png','svg'):fig.savefig(HERE/('gso_v1_certificate.'+ext),dpi=180,facecolor=fig.get_facecolor())


if __name__=='__main__':main()
