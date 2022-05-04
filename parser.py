class KeyValDict(dict):
    def __init__(self, val=None):
        if val is None:
            val = {}
        for k in val.keys():
            validateKey(k)
            validateVal(val[k])
        super().__init__(val)

    def __setitem__(self, key, val):
        validateKey(key)
        validateVal(val)
        super().__setitem__(key, val)
        

    def __getitem__(self, key):
        return super().__getitem__(key)

class Parser(dict):
    def __init__(self):
        super().__init__()        

    def __setitem__(self, key, val):
        validateSection(key)
        if key not in self.keys():
            super().__setitem__(key, KeyValDict(val))
        else :
            self[key].update(KeyValDict(val))

    def __getitem__(self, key):
        return super().__getitem__(key)
    
    def addFromString(self, str):
        lines = str.splitlines()
        section = 'default'
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if isSection(line):
                candidateSection = line.strip('[]')
                validateSection(candidateSection)
                if candidateSection not in self.__dict__:
                    self[candidateSection] = KeyValDict()
                section = candidateSection

            elif isKeyVal(line):
                candidateKey, candidateVal = line.split('=')
                candidateKey = candidateKey.strip()
                candidateVal = candidateVal.strip()
                validateKey(candidateKey)
                validateVal(candidateVal)
                self[section][candidateKey] = candidateVal

            else:
                raise ValueError(f'Syntax error: line "{line}" is nor a valid section nor a valid key-value pair.')

    def readFile(self, filename):
        with open(filename, "r") as f:
            self.addFromString(f.read())

    def writeToFile(self, filename):
        page = ''
        for section, pairs in self.items():
            page += f"[{section}]\n".format(section)
            for key, val in pairs.items():
                page += f"{key} = {val}\n".format(key, val)

        with open(filename, "w") as f:
            f.write(page)

    def __str__(self):
        return super().__str__



def validateKey(key):
    if key == '' or ' ' in key or ';' in key :
        raise ValueError(f'Syntax error: key "{key}" is not valid.')
    

def validateVal(val):
    if val == '' or ' ' in val or ';' in val :
        raise ValueError(f'Syntax error: value "{val}" is not valid.')

def validateSection(section):
    if section == '' or ' ' in section or ';' in section :
        raise ValueError(f'Syntax error: section "{section}" is not valid.')

def isSection(str):
    return str.startswith('[') and str.endswith(']') and len(str) > 2

def isKeyVal(str):
    return str.count('=') == 1 and len(str) > 1


