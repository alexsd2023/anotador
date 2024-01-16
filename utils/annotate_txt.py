#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.colors  as mcolors

def annotate_line(line, df):
    print(df.head)
    result= []
    pivote= 0

    for index in df.index:
        
        start= df.loc[index, 'Start']
        text= df.loc[index, 'Text']
        entity= df.loc[index, 'Entity']
        
        if pivote < start:
            result.append(line[pivote:start])
            print(line)
            print(line[pivote:start])
            print(pivote)
            print(start)

        result.append((text, entity))  
        pivote= start + len(text)
        
    if pivote < len(line):
        result.append(line[pivote:len(line)])

    print(result)
    return result


def format_color_groups(df, color):
    x = df.copy()
    i = 0
    for factor in color:
        x.iloc[i, :-1] = ''
        if color[i] != None:
            style = f'background-color: {color[i]}'
            #style='background-color: yellow'
            
            x.loc[i, 'Background'] = style
        i = i + 1
    
    return x

def format_color_stats(df, color):
    x = df.copy()
    i = 0
    for index in x.index:
        x.iloc[index, :-1] = ''
        if color[i] != None:
            style = f'background-color: {color[i]}'
            x.loc[index, 'Background'] = style
        i = i + 1
    
    return x

if __name__ == "__main__": 
    print('')  