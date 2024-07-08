#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 07:39:54 2020

@author: anonym
"""
FILENAME='example.ini'

import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {'ServerAliveInterval': '45','Compression': 'yes','CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here

config['DEFAULT']['ForwardX11'] = 'yes'

with open(FILENAME, 'w') as configfile:
   config.write(configfile)
   
   
config = configparser.ConfigParser()
# print(config.sections())

config.read('example.ini')
print(config.sections())

print('bitbucket.org' in config)
print('bytebong.com' in config)

print(config['bitbucket.org']['User'])

print(config['DEFAULT']['Compression'])
print(config['DEFAULT']['compressionlevel'])
topsecret = config['topsecret.server.com']
print(topsecret['ForwardX11'])
print(topsecret['Port'])

for key in config['bitbucket.org']:  
    print(key)
    
print(config['bitbucket.org']['ForwardX11'])
#As we can see above, the API is pretty straightforward. 
#The only bit of magic involves the DEFAULT section which provides default values 
#for all other sections 1. Note also that keys in sections are case-insensitive 
#and stored in lowercase