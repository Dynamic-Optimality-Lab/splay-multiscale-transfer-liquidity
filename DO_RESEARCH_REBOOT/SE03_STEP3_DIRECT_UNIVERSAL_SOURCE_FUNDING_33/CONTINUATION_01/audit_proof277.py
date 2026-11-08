from pathlib import Path
import sys
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/search_native12_fixed_word_LOW.py'
s=p.read_text().replace('native12_LOW_build_01.pkl','native12_HARD_LOW_build_01.pkl')
s=s.replace('native12_fixed_B_word.json','native12_hard_B_word.json')
s=s.replace('native12_fixed_word_LOW_result','native12_HARD_word_LOW_result')
sys.argv.append('proof277');globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
