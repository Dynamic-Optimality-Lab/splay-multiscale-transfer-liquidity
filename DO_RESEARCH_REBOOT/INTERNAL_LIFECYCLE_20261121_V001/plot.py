"""Scientific figure from exact complete-source rows; no image-generation model."""
import json
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(HERE/'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

assert not (HERE/'FINAL_MANIFEST.json').exists()
w = json.loads((HERE/'I_p3_q5_d1_m2_complete_witness.json').read_text())
rows = [r for r in w['rows'] if r['phase'].startswith('I1:')]
r = w['source']['r']
packet = w['packets'][0]
u = {tuple(z['id']) for z in w['all_B_double_records'] if z['U_int']}
x = [0]+[z['id'] for z in rows]
phi = [0]+[z['phi_postB'] for z in rows]
phiA = [0]+[z['phi_postA'] for z in rows]
heads = sorted({z['A_payment'][1] for z in packet['seeds']})
fig, axes = plt.subplots(2, 1, figsize=(10.4, 6.9), sharex=True, gridspec_kw={'height_ratios':[1.35, 1]})
fig.patch.set_facecolor('#f8fafc')
for ax in axes:
    ax.set_facecolor('#ffffff')
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y', color='#e2e8f0', linewidth=0.7)
    for a,b,col in [(0,r-1,'#dbeafe'),(r-1,2*r-1,'#fef3c7'),(2*r-1,3*r-1,'#dcfce7'),(3*r-1,4*r-2,'#ede9fe')]:
        ax.axvspan(a,b,color=col,alpha=.42,zorder=0)
axes[0].step(x, phiA, where='post', color='#94a3b8', lw=1, label='after original A phase')
axes[0].step(x, phi, where='post', color='#0f766e', lw=1.6, label='after original B phase')
burst = r+7
recharge = 2*r+2
axes[0].scatter([burst,recharge], [phi[burst],phi[recharge]], color=['#dc2626','#7c3aed'],zorder=6,s=30)
axes[0].annotate('last critical burst: '+r'$\Delta_B\Phi=-5$', (burst,phi[burst]),xytext=(burst+22,phi[burst]+8),fontsize=10,arrowprops={'arrowstyle':'-','color':'#475569'})
axes[0].annotate('one restoration access: '+r'$\Delta_B\Phi=+4$'+'\nincoming original A gap = 1', (recharge,phi[recharge]),xytext=(recharge+30,-12),fontsize=10,arrowprops={'arrowstyle':'-','color':'#475569'})
axes[0].set_ylabel(r'Frozen potential $\Phi_{\mathcal{M}}$',fontsize=11)
axes[0].legend(frameon=False,loc='lower left',fontsize=9)
critical_cum = [0]+[sum(z[0]<=op for z in u if z[0] in packet['critical_operations']) for op in x[1:]]
life_cum = [0]+[sum(z[0]<=op for z in u if z[0] in packet['critical_operations']+packet['restoration_operations']) for op in x[1:]]
heads_cum = [0]+[sum(t<=op for t in heads) for op in x[1:]]
axes[1].step(x,life_cum,where='post',color='#be123c',label='original lifecycle U demands (55)',lw=1.5)
axes[1].step(x,heads_cum,where='post',color='#2563eb',label='distinct real A payment heads (45)',lw=1.5)
axes[1].step(x,critical_cum,where='post',color='#d97706',label='critical U demands (39)',lw=1,ls='--')
axes[1].set_ylabel('Exact occurrence count',fontsize=11)
axes[1].set_xlabel('Original operation in the first inner lifecycle',fontsize=11)
axes[1].legend(frameon=False,loc='upper left',fontsize=9)
axes[1].set_ylim(-2,65)
axes[1].set_xlim(0,4*r-2)
for label,a,b in [('A preparation',0,r-1),('critical descent',r-1,2*r-1),('forward restoration',2*r-1,3*r-1),('reverse',3*r-1,4*r-2)]:
    axes[0].text((a+b)/2,1.03,label,transform=axes[0].get_xaxis_transform(),ha='center',fontsize=9,color='#334155')
fig.suptitle('Restoration recharges the potential; renewed birth runs locate the A work',fontsize=14,fontweight='bold',y=.99,color='#0f172a')
fig.text(.08,.015,'Exact I(p=3,q=5,d=1) data. Zoom: one inner lifecycle; the saved 5,919-operation source includes both copies and full closure.\nCharging is cyclic and aggregate. The plotted counts are evidence for this source; uniform constants come from the symbolic proof.',fontsize=8.5,color='#475569')
fig.tight_layout(rect=[0,.07,1,.945])
for ext in ['png','svg']:
    fig.savefig(HERE/('internal_lifecycle_accounting.'+ext),dpi=160,facecolor=fig.get_facecolor())
print('Saved exact-data lifecycle figure')
