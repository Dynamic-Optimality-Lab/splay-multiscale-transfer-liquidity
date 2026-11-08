"""Strict read-only streaming of pinned integer-potential dictionaries."""
import mmap,re,json
from pathlib import Path
ENTRY=re.compile(rb'\s*"([0-9]+)"\s*:\s*(-?[0-9]+)\s*')
SPACE=re.compile(rb'\s*')
class Values:
    def __init__(self,path):self.path=Path(path);self.count=0
    def __enter__(self):
        self.file=self.path.open('rb');self.mm=mmap.mmap(self.file.fileno(),0,access=mmap.ACCESS_READ)
        p=self.mm.find(b'"values"');assert p>=0
        self.header=json.loads(self.mm[:p]+b'"values":{}}');assert set(self.header)=={'N','default','values'} and self.header['default']=='-psi(B)'
        p=SPACE.match(self.mm,p+8).end();assert self.mm[p:p+1]==b':'
        p=SPACE.match(self.mm,p+1).end();assert self.mm[p:p+1]==b'{'
        self.start=p+1;return self
    def __iter__(self):
        p=SPACE.match(self.mm,self.start).end();self.count=0
        if self.mm[p:p+1]!=b'}':
            while True:
                match=ENTRY.match(self.mm,p);assert match is not None,('invalid integer entry',p)
                key=int(match.group(1));value=int(match.group(2));p=match.end();self.count+=1
                yield key,value
                char=self.mm[p:p+1]
                if char==b'}':break
                assert char==b',',('invalid entry separator',p)
                p=SPACE.match(self.mm,p+1).end();assert self.mm[p:p+1]!=b'}','trailing comma'
        p=SPACE.match(self.mm,p+1).end();assert self.mm[p:p+1]==b'}'
        assert SPACE.match(self.mm,p+1).end()==len(self.mm),'unexpected trailing fields'
    def __exit__(self,*args):self.mm.close();self.file.close()
