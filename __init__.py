import re
from cudatext import *
from cudax_lib import get_opt

TAG_ICON = -1
TAB_SIZE = ed.get_prop(PROP_TAB_SIZE,'')
OPT_YAML1 = get_opt('yaml_codetree_show_comment',0)

def get_indent(str): 
    match = re.search(r"^\s*", str) 
    return 0 if not match else match.end()

def get_indent_fast(str): 
    return len(str) - len(str.lstrip())
    
def get_headers(filename, lines):
    y = -1
    getter = []
    for line in lines:
        y += 1
        line = line.replace('\t',' ' * TAB_SIZE)
        
        if line.lstrip().startswith('#'):
            if OPT_YAML1 == 0:
                continue
            if OPT_YAML1 == 1:
                yup = max([0,y-1])
                if yup != y:
                    lineup = lines[yup]
                    if lineup.lstrip().startswith('#'):
                        continue                                     
        
        caption = ''
        posdpt = line.find(':')            
        posrem = line.rfind('#')
        postag1 = line.find('<')
        postag2 = line.rfind('>')        
        if posdpt == -1 and posrem == -1:
            continue
        if (posdpt != -1) and ((postag1 == -1) or (postag1 > posdpt)):
            caption = line[:posdpt + 1]
        if (posrem != -1) and ((postag2 == -1) or (postag2 < posrem)):
            if caption != '':
                caption = caption + ' '
            caption = caption + line[posrem + 1:].lstrip()   
        if caption == '':
            continue                         
        getter.append(((0,y,len(line),y),1,caption,TAG_ICON))
        # getter.append(((0,y,len(line),y),get_indent(line),caption,TAG_ICON))         
        # getter.append(((0,y,len(line),y),get_indent_fast(line),caption,TAG_ICON))        
            
    return getter