# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 16:38:44 2016

@author: jerry
"""
# abstract class. superclass star, planet, system.
class planetary_obj:
    def __init__(self):
        self.data = dict();
    # return field value for that class. type can be list, string, float, etc   
    def getval(self, key):
        return self.data[key];

    def __str__(self):
        out = "";
        for i in self.data:
            out += (i + ":");
            out += str(self.data[i]);
            out += " ";
        return out;
    class Builder:
        def __init__(self, name):
            self._data = {"name": name};
        # adds new field with key being name, value being val    
        def addVal(self, name, val):
            val = self._fixVal(val);
            self._data[name] = val;
            return self;
        # adds a field connected to a list, initiates starts of list 
        def addValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] = [val]
            return self
        # adds a field value to an existing list
        def addToValList(self, name, val):
            val = self._fixVal(val)
            self._data[name] += [val]
            return self

        def compile(self):
            po = planetary_obj();
            po.data = self._data;
            return po;
        
        def _fixVal(self, val):
            temp = None;
            if(val != ''):
                try:
                    temp = float(val);
                except ValueError:
                    temp = val;
                except TypeError:
                    temp = "N/A";
            else:
                temp = "N/A";
            return temp;
        