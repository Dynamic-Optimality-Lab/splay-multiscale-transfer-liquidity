from exp03_core import *


def total(rows):
    return {'sources':len(rows),'operations':sum(s['operations'] for s in rows),'A':sum(s['A'] for s in rows),
        'Q_B':sum(s['Q_B'] for s in rows),'unhandled_gaps':sum(len(s['unhandled_events']) for s in rows),
        'distinct_parents':sum(s['parent_interface']['parent_count'] for s in rows),
        'gap_types':{k:sum(sum(e['type']==k for e in s['unhandled_events']) for s in rows) for k in ('O','G','X')},
        'parent_types':{k:sum(s['parent_interface']['counts'][k] for s in rows) for k in ('O','G','X')},
        'restart_paid':sum(s['restart_comparison']['paid_gap_count'] for s in rows),
        'remaining':sum(len(s['remaining_after_restart']) for s in rows)}


if __name__=='__main__':
    meter=Meter('finalize_data')
    results=json.loads((ROOT/'EXP03_CAUSAL_EPISODE_RESULTS.json').read_text())
    old=results['inherited_sources'];new=results['new_sources'];allrows=old+new;byname={s['source']:s for s in allrows}
    archive=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
    for s in archive['new_sources']:
        assert s['name'] in byname and byname[s['name']]['complete_paired_closure']
        s.update(closing_A=s['initial_A'],closing_B=s['initial_B'],
            certificate_location='EXP03_CAUSAL_EPISODE_RESULTS.json: new_sources, by source name')
    write('EXP03_SOURCE_WITNESSES.json',archive)
    inv=json.loads((ROOT/'EXP03_UNHANDLED_PARENT_INVENTORY.json').read_text())
    inv['new_sources']=[{k:s[k] for k in ('source','population','operations','A','Q_B','parent_interface','original_parents','unhandled_events','remaining_after_restart')} for s in new]
    inv['new_totals']=total(new)
    inv['all_source_count']=len(archive['inherited_sources'])+len(new)
    write('EXP03_UNHANDLED_PARENT_INVENTORY.json',inv)
    for typ,file in [('O','EXP03_OMITTED_HIT_EPISODES.json'),('G','EXP03_MISSING_GRANDPARENT_EPISODES.json')]:
        z=json.loads((ROOT/file).read_text());z['stage']='final exact original inventory, physical ancestry and causal/restart episodes'
        z['new_parent_records']=[{'source':s['source'],**p} for s in new for p in s['original_parents'] if p['type']==typ]
        z['causal_links']=[{'source':s['source'],'parent_ids':[p['original_parent'] for p in s['original_parents'] if p['type']==typ],
            'actual_episode_ids':sorted({p['actual_episode'] for p in s['original_parents'] if p['type']==typ}),
            'comparison_windows':[d['window_index'] for d in s['comparison_divergence']],
            'file':'EXP03_CAUSAL_EPISODE_RESULTS.json'} for s in allrows if s['parent_interface']['counts'][typ]]
        if typ=='G':
            for p in z['inherited_parent_records']:
                source_row=byname[p['source']];t=p['original_parent'][0]
                for f in sorted((ROOT/'EXP02_TRAJECTORIES').glob(digest(p['source'])[:16]+'_*.json')):
                    tr=json.loads(f.read_text());acc=next((a for a in tr['retained_accesses'] if a['original_operation']==t),None)
                    if acc is None:continue
                    pool=tr['state_pool'];states={k:pool[acc[k]['state_sha256']] for k in ('actual_pre','actual_post','shadow_pre','shadow_post')}
                    p['at_consumer']={'operation':t,'actual_path':acc['actual_path'],'shadow_path':acc['shadow_path'],
                        'actual_Q':acc['actual_q'],'shadow_Q':acc['shadow_q'],**states,
                        'actual_doubles':list(frame_records(states['actual_pre'],acc['target'],states['actual_post']).values()),
                        'shadow_doubles':list(frame_records(states['shadow_pre'],acc['target'],states['shadow_post']).values()),
                        'shadow_terminal_zig':(len(acc['shadow_path'])-1)%2==1,'trajectory_file':str(f.relative_to(ROOT))}
                    break
                assert p['at_consumer']['shadow_doubles']==[]
        write(file,z)
    write('EXP03_OUTSIDE_WINDOW_EPISODES.json',{'parent_records':[{'source':s['source'],**p} for s in new for p in s['original_parents'] if p['type']=='X'],
        'source_words':'EXP03_SOURCE_WITNESSES.json','causal_results':'EXP03_CAUSAL_EPISODE_RESULTS.json',
        'status':'nonempty exact class; no universal A bound established'})
    fams=defaultdict(list)
    for s in new:fams[s['family']].append(s)
    summary={'inherited_reanalyzed':total(old),'new':total(new),'new_families':{k:total(v) for k,v in fams.items()},
        'source_count':len(archive['inherited_sources'])+len(new),
        'distinct_corpus_operations':sum(len(s['operations']) for s in archive['inherited_sources']+archive['new_sources']),
        'maximum_population':max(s['population'] for s in new),'maximum_source_operations':max(s['operations'] for s in new),
        'max_last_loss_primitive_load':max(s['last_loss_selector']['maximum_primitive_load'] for s in allrows),
        'last_loss_undefined_parents':sum(s['last_loss_selector']['undefined_parents'] for s in allrows),
        'max_observed_raw_divergence_A_overlap':max(s['raw_divergence_A_maximum_overlap'] for s in allrows),
        'remaining_types':dict(Counter(e['type'] for s in allrows for e in s['remaining_after_restart'])),
        'maximum_unhandled_over_A':max(((Fraction(len(s['unhandled_events']),s['A']),s['source']) for s in new if s['A']),key=lambda p:p[0])}
    summary['maximum_unhandled_over_A']=[str(summary['maximum_unhandled_over_A'][0]),summary['maximum_unhandled_over_A'][1]]
    write('EXP03_SUMMARY.json',summary)
    table=['# EXP-03 complete new-source measurements','',
        'Finite exact counts; P is a distinct original parent occurrence, R is an original gap. Restart is payment by the independently defined equality-restarted comparison. No row establishes a universal ratio.','',
        '| Source | n | ops | A | Q_B | R_O/P_O | R_G/P_G | R_X/P_X | Restart | Remaining | Last-loss max load |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for s in new:
        counts=Counter(e['type'] for e in s['unhandled_events']);p=s['parent_interface']['counts']
        table.append(f"| {s['source']} | {s['population']} | {s['operations']} | {s['A']} | {s['Q_B']} | {counts['O']}/{p['O']} | {counts['G']}/{p['G']} | {counts['X']}/{p['X']} | {s['restart_comparison']['paid_gap_count']} | {len(s['remaining_after_restart'])} | {s['last_loss_selector']['maximum_primitive_load']} |")
    (ROOT/'EXP03_FULL_MEASUREMENTS.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
    meter.success=True;meter.details.update(new_sources=len(new));print(json.dumps(summary,indent=2),flush=True)
