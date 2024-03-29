#!/usr/bin/python

import sys
import os
import copy
import yaml
from rtk_tools import dictlib

dir="recipe.d"
files=["param.yaml"]

def merge(f):
  entry=os.listdir(dir)
  print("entry",entry)
  rc=entry[0]
  yf=open(dir+"/"+rc+"/"+f, "r")
  master = yaml.safe_load(yf)

  for rc in entry[1:]:
    yf=open(dir+"/"+rc+"/"+f,"r")
    dictlib.merge(master,yaml.safe_load(yf))
    yf.close()

  for rc in entry:
    yf=open(dir+"/"+rc+"/"+f,"r")
    dictlib.merge(master,yaml.safe_load(yf))
    yf.close()
    yf=open(dir+"/"+rc+"/"+f,"w")
    yaml.dump(master,yf,default_flow_style=False)
    yf.close()

def trim(f):
  entry=os.listdir(dir)
  rc=entry[0]
  yf=open(dir+"/"+rc+"/"+f, "r")
  master=yaml.safe_load(yf)

  for rc in entry[1:]:
    yf=open(dir+"/"+rc+"/"+f,"r")
    dictlib.intersect(master,yaml.safe_load(yf))
    yf.close()

  for rc in entry:
    dm=copy.deepcopy(master)
    yf=open(dir+"/"+rc+"/"+f,"r")
    dictlib.intersect(dm,yaml.safe_load(yf))
    yf.close()
    yf=open(dir+"/"+rc+"/"+f,"w")
    yaml.dump(dm,yf,default_flow_style=False)
    yf.close()

if len(sys.argv)>1:
  if sys.argv[1]=='trim':
    print('run as trim mode')
    for f in files: trim(f)
  else:
    print('run as merge mode')
    for f in files: merge(f)
else:
  print('run as merge mode')
  for f in files: merge(f)
