"""SRT timing editor. Originals are only replaced when explicitly selected on export."""
import re,sys,unittest
from pathlib import Path
def millis(text):
    h,m,s,ms=map(int,re.split('[:,]',text));return ((h*60+m)*60+s)*1000+ms
def stamp(value):
    value=max(0,value);s,ms=divmod(value,1000);m,s=divmod(s,60);h,m=divmod(m,60);return f'{h:02}:{m:02}:{s:02},{ms:03}'
def parse(text):
    rows=[]
    for block in re.split(r'\n\s*\n',text.replace('\r\n','\n').strip()):
        lines=block.splitlines()
        if len(lines)<3 or not re.fullmatch(r'\d+',lines[0]):raise ValueError('Expected numbered SRT blocks')
        m=re.fullmatch(r'(\d{2,}:\d{2}:\d{2},\d{3}) --> (\d{2,}:\d{2}:\d{2},\d{3})',lines[1])
        if not m:raise ValueError('Invalid SRT timestamp line')
        a,b=map(millis,m.groups())
        if b<a:raise ValueError('Cue ends before it begins')
        rows.append((a,b,'\n'.join(lines[2:])))
    return rows
def render(rows,offset):return '\n\n'.join(f'{i+1}\n{stamp(a+offset)} --> {stamp(b+offset)}\n{text}'for i,(a,b,text)in enumerate(rows))+'\n'
class Tests(unittest.TestCase):
    def test_roundtrip(self):
        rows=parse('1\n00:00:01,100 --> 00:00:02,200\nHello\nworld\n');self.assertEqual(parse(render(rows,500))[0],(1600,2700,'Hello\nworld'));self.assertEqual(parse(render(rows,-2000))[0][:2],(0,200))
    def test_invalid(self):
        with self.assertRaises(ValueError):parse('bad')
        self.assertEqual(stamp(3600123),'01:00:00,123')
def ui():
    import tkinter as tk
    from tkinter import ttk,filedialog,messagebox
    root=tk.Tk();root.title('Subtitle Sync Studio');root.geometry('900x640');rows=[]
    panel=ttk.Frame(root,padding=18);panel.pack(fill='both',expand=True);ttk.Label(panel,text='Move the words into time.',font=('Segoe UI',24)).pack(anchor='w')
    offset=tk.StringVar(value='0');ttk.Label(panel,text='Global offset in milliseconds (negative = earlier)').pack(anchor='w');ttk.Entry(panel,textvariable=offset).pack(fill='x');preview=tk.Text(panel,wrap='word');preview.pack(fill='both',expand=True,pady=12)
    def draw(*args):
        try:result=render(rows,int(offset.get()));preview.delete('1.0','end');preview.insert('1.0',result)
        except ValueError:pass
    def load():
        nonlocal rows
        path=filedialog.askopenfilename(filetypes=[('SRT','*.srt')])
        if path:
            try:rows=parse(Path(path).read_text(encoding='utf-8-sig'));offset.set('0');draw()
            except (OSError,ValueError)as e:messagebox.showerror('Open failed',str(e))
    def save():
        if not rows:return
        try:
            value=int(offset.get());path=filedialog.asksaveasfilename(defaultextension='.srt')
            if path:Path(path).write_text(render(rows,value),encoding='utf-8')
        except (OSError,ValueError)as e:messagebox.showerror('Export failed',str(e))
    ttk.Button(panel,text='Open SRT',command=load).pack(side='left');ttk.Button(panel,text='Export shifted SRT',command=save).pack(side='left');offset.trace_add('write',draw);root.mainloop()
if __name__=='__main__':unittest.main(argv=[sys.argv[0]])if '--self-test'in sys.argv else ui()
