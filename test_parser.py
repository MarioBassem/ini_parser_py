from parser import Parser, validateKey, validateSection, validateValue, isSection, isKeyVal
import pytest

@pytest.fixture
def input():
    return [['s', True], ['', False], ['s s', False], ['s;s', False]]

def test_SectionValidation(input):
    for section, validity in input:
        assert validateSection(section) == validity
    
def test_KeyValidation(input):
    for key, validity in input:
        assert validateKey(key) == validity

def test_ValueValidation(input):
    for val, validity in input:
        assert validateValue(val) == validity

def test_isSection():
    notSection = ['[]', '[', ']', 's = s', '']
    for s in notSection:
        assert isSection(s) == False
    assert isSection('[s]') == True

def test_isKeyVal():
    notKeyVal = ['', '=', 'k v']
    for p in notKeyVal:
        assert isKeyVal(p) == False
    assert isKeyVal('k=v') == True

def test_addFromString():
    p = Parser()
    str = "[s1]\nk1=v1\n\n[s2]\nk2=\n\n"
    p.addFromString(str)
    assert ('s1' in p._parser.keys()) == True
    assert p._parser['s1']['k1'] == 'v1'
    assert ('s2' in p._parser.keys()) == True
    assert ('k2=' not in p._parser['s2'].keys()) == True



def test_addFromDict():
    p = Parser()
    d = {'s' : {'k': 'v'}, 's2' : {'k2': 'v2'}}
    p.addFromDict(d)
    for s, kv in d.items():
        assert (s in p._parser.keys()) == True
        for key, val in kv.items():
            assert p._parser[s][key] == d[s][key]
        


def test_addKeyValPair():
    p = Parser()
    p._Parser__addKeyValuePair({'k': 'v'})
    assert ('default' in p._parser.keys()) == True
    assert p._parser['default']['k'] == 'v'

def test_addSection():
    p = Parser()
    p._Parser__addSection('s')
    assert ('s' in p._parser.keys()) == True

#TODO

def test_writeToFile():
    pass

def test_addFromFile():
    pass