#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:20:04 2020

@author: antonio
"""

import pandas as pd
import warnings
import csv

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line

def main(datapath, relevant_labels):
    
    df = pd.read_csv(datapath, sep='\t', header=0, quoting=csv.QUOTE_NONE)

    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df

    df_ok = df.loc[df['label'].isin(relevant_labels),:].copy()
    df_ok['offset'] = df_ok['off0'].astype(str) + ' ' + df_ok['off1'].astype(str)
    
    if df_ok.shape[0] != df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).shape[0]:
        warnings.warn(f"There are duplicated entries in {datapath}. Removing them...")
        df_ok = df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).copy()
        
    return df_ok


def main_subtrack3(datapath):
    
    df = pd.read_csv(datapath, sep='\t', header=0, quoting=csv.QUOTE_NONE)

    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df
    
    if df.shape[0] != df.drop_duplicates(subset=['filename']).shape[0]:
        warnings.warn(f"There are filenames with more than one row in {datapath}. Keeping just the first one...")
        df = df.drop_duplicates(subset=['filename']).copy()
    return df