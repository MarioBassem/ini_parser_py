from parser import Parser, validateKey, validateSection, validateVal, isSection, isKeyVal
import pytest

@pytest.fixture
def input():
    return [' ', 's s', 's;s']

def test_SectionValidation(input):
    for section in input:
        with pytest.raises(ValueError):
            validateSection(section)
    
def test_KeyValidation(input):
    for key in input:
        with pytest.raises(ValueError):
            validateKey(key)

def test_ValueValidation(input):
    for val in input:
        with pytest.raises(ValueError):
            validateVal(val)

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
    #test adding a non-valid string
    nonValidStr = "[s1]\nk1=v1\n\n[s2]\nk2=\n\n"
    with pytest.raises(ValueError):
        p.addFromString(nonValidStr)
    
    # test adding a valid string
    validStr = "[s1]\nk1=v1\n\n[s2]\nk2=v2\n\n"
    p.addFromString(validStr)
    assert ('s1' in p.keys()) == True
    assert p['s1']['k1'] == 'v1'
    assert ('s2' in p.keys()) == True
    assert ('k2=' not in p['s2'].keys()) == True


#TODO
def test_addKeyValPair():
    pass

def test_addSection():
    pass

def test_writeToFile():
    pass

def test_addFromFile():
    pass