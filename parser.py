
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Parser:
    def __init__(self):
        self._parser = dict(dict())

    def __addSection(self, section):
        if section not in self._parser.keys():
            self._parser[section] = dict()
        

    def __addKeyValuePair(self, keyValuePairs, section='default'):
        self.__addSection(section)
        for key, val in keyValuePairs.items():
            self._parser[section][key] = val


    def addFromDict(self, dict):
        for section, keyValPairs in dict.items():
            section = section.strip(' ')
            if validateSection(section) :
                for key, val in keyValPairs.items():
                    key = key.strip(' ')
                    val = val.strip(' ')
                    if validateKey(key) and validateValue(val):
                        self.__addKeyValuePair({key: val}, section)
                    else:
                        logging.info('key val pair: "' + key + ' = ' + val + '" is not valid')
            else:
                logging.info('sectino: ' + section + ' is not valid')
            # self.__addKeyValuePair(keyValPairs, section)

    def addFromString(self, str):
        lines = str.splitlines()
        section = 'default'
        for line in lines:
            line = line.strip(' ')
            if isSection(line):
                lineWithoutBrackets = line.strip('[]')
                if validateSection(lineWithoutBrackets):
                    section = lineWithoutBrackets
                    self.__addSection(section)
            elif isKeyVal(line):
                key, val = line.split('=')
                key = key.strip(' ')
                val = val.strip(' ')
                if validateKey(key) and validateValue(val):
                    self.__addKeyValuePair({key: val}, section)
                else:
                    logging.info('line: ' + line + ' is not a section or key/val pair')
            else:
                logging.info('line: ' + line + ' is not a section or key/val pair')

                
    def addFromFile(self, filename):
        with open(filename, "r") as f:
            self.addFromString(f.read())

    def writeToFile(self, filename):
        page = ''
        for section, pairs in p._parser.items():
            page += f"[{section}]\n".format(section)
            for key, val in pairs.items():
                page += f"{key} = {val}\n".format(key, val)

        with open(filename, "w") as f:
            f.write(page)

    def __str__(self):
        str = ""
        for section, pair in self._parser.items():
            str += section + "\n"
            for key, val in pair.items():
                str += key + " = " + val + "\n"
        return str


def validateSection(section):
    return section != '' and ' ' not in section and ';' not in section

def validateKey(key):
    return key != '' and ' ' not in key and ';' not in key

def validateValue(val):
    return val != '' and ' ' not in val and ';' not in val

def isSection(str):
    return str.startswith('[') and str.endswith(']') and len(str) > 2

def isKeyVal(str):
    return str.count('=') == 1 and len(str) > 1
