# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:35:41 2017

Scans through a Python file and autoamtically runs *conda install* if possilbe
 or *pip install* if not for every package. 

@author: John Roberts
"""
import unittest
import subprocess as sp
import os

def GetModules(filepath):
    
    modulelist = []
    
    #Load file
    with(open(filepath,'r'))as file:
        #find any line with an import or from statement in
        for line in file:
            if line.startswith("import") or line.startswith("from"):
                #Grab the second word if it does; that's the module
                modulelist.append(line.split()[1])

    return modulelist


def test_GetModules(): 
    assert GetModules('testFile.py') == ['foo','bar']
    
    
def ImportModules(modulelist):
    failedlist = []
    for module in modulelist:
        #Try Conda
        out = sp.call(['conda', 'install', module], stdout=sp.PIPE)
        #If it didn't work, try pip
        if out.returncode == 0:
            continue
        out = sp.call(['pip', 'install', module], stdout=sp.PIPE)
        if out.returncode == 0:
            continue
        #If it still didn't work, add to list
        failedlist.append(module)
        
    if len(failedlist > 0):
        print("failed modules:\n")
        for module in failedlist:
            print("\t" + module + "\n")
 
           
def PrintModuleList(filepath):
    modules = GetModules(filepath)
    outpath = os.path.join(os.path.curdir, 'modulelist.txt')
    with open(outpath, 'w') as fp:
        for module in modules:
            fp.write(module + '\n')

