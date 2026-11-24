"""Scientific illustration from one exact original witness; not proof by plot."""
import json
import os
from pathlib import Path
HERE=Path(__file__).resolve().parent
if (HERE/'FINAL_MANIFEST.json').exists():
    raise RuntimeError('Sealed run: output generation requires a new versioned directory.')
os.environ['MPLCONFIGDIR']=str(HERE/'plot-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

w=json.loads((HERE/'H_p3_q7_complete_witness.json').read_text())
n=w['source']['N'];rows=w['operations'];xs=[0];ys=[0]
for row in rows:
    xs.extend([row['id']-.3,row['id']]);ys.extend([row['phi_postA']['M'],row['phi_postB']['M']])
fig,ax=plt.subplots(figsize=(11.5,4.8),layout='constrained')
bounds=[0,n-1,2*n-1,3*n-1,4*n-2]
names=['A preparation','Descent and B bursts','Forward restoration','Reverse restoration']
for i,(a,b) in enumerate(zip(bounds,bounds[1:])):
    ax.axvspan(a,b,color=['#dceaf8','#f8e2dc','#e2f0e7','#efe7f6'][i],alpha=.72,zorder=0)
    ax.text((a+b)/2,5,names[i],ha='center',va='center',fontsize=10)
ax.step(xs,ys,where='post',color='#183c62',lw=1.7)
ax.axhline(0,color='#8a96a0',lw=.7)
ax.annotate('First KEEP N: +6',xy=(n,0),xytext=(n-75,-21),arrowprops={'arrowstyle':'->','color':'#435666'},fontsize=10,color='#183c62')
t=n+7;after=rows[t-1]['phi_postB']['M']
ax.annotate('Last critical burst: −7',xy=(t,after),xytext=(t+25,after+11),arrowprops={'arrowstyle':'->','color':'#435666'},fontsize=10,color='#183c62')
ax.set(xlim=(0,4*n-2),ylim=(-58,9),xlabel='Original operation ID',ylabel=r'$\Phi_{\mathcal{M}}(A,B;S)$',
       title=r'Complete $H_{3,7}$: signed size-layer potential, including all preparation and return work')
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18)
fig.text(.5,-.015,'Exact replay illustration: N = 129, A = 512, Q_B = 221. Parametric conclusions use the separate symbolic proof.',ha='center',fontsize=9,color='#4b5660')
fig.savefig(HERE/'H3q_potential_profile.png',dpi=170,bbox_inches='tight')
fig.savefig(HERE/'H3q_potential_profile.svg',bbox_inches='tight')
plt.close(fig)
print('Profile PNG and SVG written from complete original source.')
