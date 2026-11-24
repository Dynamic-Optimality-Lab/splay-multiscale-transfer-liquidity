from base0 import *

def archive(p):
    x=load(p)
    return x if isinstance(x,list) else x.get('sources',x.get('inherited_sources',[])+x.get('new_sources',[]))

def controls():
    rows=[]
    def add(s,p,scope):
        rows.append({'source':s,'archive':str(p),'archive_sha256':hfile(p),
                     'source_sha256':digest(s),'prior_scope':scope})
    p=C5/'SOURCE_WITNESSES.json'
    for s in archive(p):add(s,p,'C05 independent primitive Pi/cohorts for small cases; physical-only516 screen.')
    p=BASE/'CONT03B_PACKET_OBSTRUCTIONS/DILATED_PACKET_SOURCES.json'
    add(archive(p)[-1],p,'577 complete independently checked original C repeat; periodic paid.')
    p=BASE/'CONTINUATION_04_PACKET_OVERFLOW/SOURCE_WITNESSES.json'
    add(archive(p)[0],p,'1027 full original Pi/cohort certification;40 R_star gaps; actual overflow empty.')
    p=BASE/'CONTINUATION_01_COVERAGE_PROOF/OWNERSHIP_SOURCES.json'
    add(archive(p)[0],p,'65 exact frozen-cover escape; repaired hybrid pays.')
    p=BASE/'CONTINUATION_02_HARD_RESIDUAL_CONSERVATION/PRIVATE_ANCESTOR_SOURCES.json'
    add(archive(p)[0],p,'193 upper-parent original source; periodic paid.')
    p=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/EXP01_SOURCE_WITNESSES.json'
    aa=archive(p)
    for name in ['G_4_1_L31_r1_z1','H_4_1','DH_4_1_at31_c1','DW_5_1_at31','DW_6_1_at31']:
        add(next(s for s in aa if s['name']==name),p,'Original EXP01 full physical and Pi/R6 records; old Hall scope retained.')
    p=REPO/'DO_RESEARCH_REBOOT/EXP03_FINAL_R6_ESCAPE_CONSERVATION/EXP03_SOURCE_WITNESSES.json'
    add(next(s for s in archive(p) if s['name']=='mixed_p5_Gcopies2'),p,'Original mixed-ownership last-loss obstruction.')
    def source(n,word,state,name):
        return {'name':name,'initial_A':state,'initial_B':state,'diagonal_initial':state,
                'reaching_prefix':[],'operations':word}
    one={'root':1,'children':{'1':[None,None]}}
    fresh=[source(1,[],one,'M0_empty_word'),
           source(1,[['K',1]]*3,one,'M0_zero_work_repeated_root')]
    vine={'root':1,'children':{'1':[None,2],'2':[None,3],'3':[None,None]}}
    fresh.append(source(3,[['D',2],['D',1]],vine,'M0_no_KEEP'))
    sparse={'root':1,'children':{'1':[None,3],'2':[None,None],'3':[2,5],
            '4':[None,None],'5':[4,6],'6':[None,7],'7':[None,None]}}
    fresh.append(source(7,[['K',5],['K',1]],sparse,'M0_sparse_S_rigid_private_hangers'))
    write('DEGENERATE_SOURCES.json',fresh)
    for s in fresh:add(s,ROOT/'DEGENERATE_SOURCES.json','Fresh exact degenerate or sparse-core control, no residual asserted.')
    assert len(rows)==20
    return rows
