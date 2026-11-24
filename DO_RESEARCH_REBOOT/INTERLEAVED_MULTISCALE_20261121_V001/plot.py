"""Scientific schematic from an exact complete multi-scale original witness."""
import json
import os
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,FancyBboxPatch
assert not (HERE/'FINAL_MANIFEST.json').exists()
w=json.loads((HERE/'H5_rho4_Y1_copies2_complete_witness.json').read_text())
p=w['result']['probe_certificates'][1]
colors=['#2563eb','#0891b2','#0f766e','#d97706','#be123c']
fig,(ax,flow)=plt.subplots(1,2,figsize=(12,5.8),gridspec_kw={'width_ratios':[1.2,1]})
fig.patch.set_facecolor('#f8fafc')
for j,(ticket,c) in enumerate(zip(p['selected_seed_runs'],colors)):
    lo,hi=ticket['label'];y=5-j
    ax.plot([lo,hi],[y,y],color=c,lw=9,solid_capstyle='round')
    ax.text(hi+.8,y,f"{hi-lo+1} keys; deficit {j}",va='center',fontsize=10,color=c)
    ax.text(63.6,y,str(ticket['depth']),va='center',ha='right',fontsize=10)
    if j in [2,4]:ax.scatter([lo+hi>>1],[y],s=55,color='white',edgecolor=c,zorder=4)
ax.axvline(66,color='#0f172a',ls='--',lw=1)
ax.text(66,5.7,'one first hit: key 66',ha='left',fontsize=11,color='#0f172a')
ax.set(xlim=(60,157),ylim=(.5,6),xlabel='Original physical key',ylabel='Scale of live original birth run')
ax.set_yticks([]);ax.spines[['top','right','left']].set_visible(False)
ax.set_title('Five scales coexist in ONE 381-key source',loc='left',fontsize=12,pad=18)
flow.set(xlim=(0,1),ylim=(0,1));flow.axis('off')
for j,c in enumerate(colors):
    yy=.88-j*.15
    flow.text(.01,yy,f"scale {j+1}: real B birth",fontsize=10,color=c,va='center')
    flow.add_patch(FancyArrowPatch((.43,yy),(.64,.49),arrowstyle='->',mutation_scale=10,color=c,lw=1.5,connectionstyle='arc3,rad=0'))
box=FancyBboxPatch((.65,.36),.32,.26,boxstyle='round,pad=0.02',facecolor='#e2e8f0',edgecolor='#94a3b8')
flow.add_patch(box)
flow.text(.81,.49,'one real A unit\nA(10770,1,0)',ha='center',va='center',fontsize=11,color='#0f172a')
flow.text(.01,.03,'All five first-hit windows have the same resource.\nFor h scales: h birth demands versus capacity C.\nNo finite uniform C covers the unrestricted stack.',fontsize=10,color='#334155',linespacing=1.6)
flow.set_title('Bounded local pooling fails',loc='left',fontsize=12,pad=18)
fig.suptitle('Interleaved restoration preserves a nested stack until one shared hit',fontsize=14,fontweight='bold',y=.98,color='#0f172a')
fig.text(.07,.075,'White markers: genuine original U frames at this probe, sizes 15 and 63, with full cyclic exposure verified.\nScope: the local-window charging law fails. Other original A work remains available; this is not a global cost counterexample.',fontsize=9,color='#475569')
fig.tight_layout(rect=[.01,.16,.99,.91])
for ext in ['png','svg']:fig.savefig(HERE/('interleaved_multiscale_obstruction.'+ext),dpi=160,facecolor=fig.get_facecolor())
print('Saved exact-source multi-scale figure')
