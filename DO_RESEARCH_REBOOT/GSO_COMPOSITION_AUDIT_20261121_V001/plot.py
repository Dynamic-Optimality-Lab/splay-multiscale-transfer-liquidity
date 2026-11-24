"""Scientific illustration of the exact original-source composition obstruction."""
import json
import os
from pathlib import Path
HERE=Path(__file__).resolve().parent
assert not (HERE/'FINAL_MANIFEST.json').exists()
os.environ['MPLCONFIGDIR']=str(HERE/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


def tree(ax,t,title):
    positions={};edges=[]
    def rec(v,depth=0):
        if v is None:return
        positions[v[0]]=(v[0],-depth)
        for child in v[1:]:
            if child:edges.append((v[0],child[0]));rec(child,depth+1)
    rec(t)
    for p,c in edges:
        xs,ys=zip(positions[p],positions[c]);ax.plot(xs,ys,color='#64748b',lw=2,zorder=1)
    for key,(x,y) in positions.items():
        color='#f59e0b' if key==4 else '#2563eb';ax.scatter([x],[y],s=560,color=color,zorder=2);ax.text(x,y,str(key),ha='center',va='center',color='white',fontsize=12,fontweight='bold')
    ax.set_title(title,fontsize=11,pad=13);ax.set_xlim(.45,4.55);ax.set_ylim(-3.5,.7);ax.axis('off')


def main():
    z=json.loads((HERE/'NONCOMMUTATION_DISCOVERY.json').read_text());full_before=(1,None,(2,None,(4,(3,None,None),None)));full_after=(3,(1,None,(2,None,None)),(4,None,None))
    fig=plt.figure(figsize=(12.8,7.8),facecolor='#f8fafc');gs=fig.add_gridspec(2,3,hspace=.15)
    tree(fig.add_subplot(gs[0,0]),full_before,'Original four-key tree')
    ax=fig.add_subplot(gs[0,1]);ax.axis('off');ax.text(.5,.64,'KEEP 3',ha='center',fontsize=17,fontweight='bold',color='#0f172a');ax.text(.5,.40,'A genuine original splay\nkey 4 stays physically present',ha='center',fontsize=12,color='#475569');ax.annotate('',xy=(.88,.17),xytext=(.12,.17),arrowprops={'arrowstyle':'->','lw':2,'color':'#64748b'})
    tree(fig.add_subplot(gs[0,2]),full_after,'Actual full tree after KEEP 3')
    tree(fig.add_subplot(gs[1,0]),z['projected_before'],'Component {1,2,3} before')
    tree(fig.add_subplot(gs[1,1]),z['ordinary_splay_after'],'Ordinary local splay result')
    tree(fig.add_subplot(gs[1,2]),z['actual_projection_after'],'Actual projected result — different')
    fig.suptitle('The missing composition interface is a real state transition',x=.5,y=.985,fontsize=19,fontweight='bold',color='#0f172a')
    fig.text(.5,.022,'Complete original period: KEEP 3, 4, 2, 1. Both full trees close exactly. A = 6, Q_B = 2.\nThe actual projected result is unreachable from the component start by any ordinary local splay word.',ha='center',fontsize=10,color='#334155')
    fig.subplots_adjust(top=.88,bottom=.12,left=.04,right=.97)
    for ext in ('png','svg'):
        path=HERE/f'composition_obstruction.{ext}';assert not path.exists();fig.savefig(path,dpi=170,facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__=='__main__':main()
