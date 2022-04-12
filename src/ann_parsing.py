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

    if ','.join(df.columns) == ','.join(['filename','mark','label','off0','off1','span']):
        print("According to file headers, you are on subtask ner")
    elif ','.join(df.columns) == ','.join(['filename','mark','label','off0','off1',
                                           'span', 'NCBITax']):
        print("According to file headers, you are on subtask norm, predictions file")
    elif ','.join(df.columns) == ','.join(['filename','mark','label','off0','off1',
                                           'span','isH','isN','iscomplex','NCBITax']):
        print("According to file headers, you are on subtask norm, GS file")
    else:
        raise Exception(f'Error! File headers are not correct {datapath}. Check https://temu.bsc.es/livingner/submission/')

    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df

    df_ok = df.loc[df['label'].isin(relevant_labels),:].copy()
    df_ok['offset'] = df_ok['off0'].astype(str) + ' ' + df_ok['off1'].astype(str)
    
    if df_ok.shape[0] != df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).shape[0]:
        warnings.warn(f"There are duplicated entries in {datapath}. Keeping just the first one...")
        df_ok = df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).copy()
        
    if "NCBITax" in df_ok.columns:
        # Remove "|" at the beginning and end of code column, in case they exist
        df_ok.NCBITax = df_ok.NCBITax.apply(lambda k: k.strip("|"))
        
    return df_ok


def main_subtrack3(datapath):
    
    df = pd.read_csv(datapath, sep='\t', header=0, quoting=csv.QUOTE_NONE)

    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df
    
    if df.shape[0] != df.drop_duplicates(subset=['filename']).shape[0]:
        warnings.warn(f"There are filenames with more than one row in {datapath}. Keeping just the first one...")
        df = df.drop_duplicates(subset=['filename']).copy()
        
    if ','.join(df.columns) != ','.join(['filename','isPet','PetIDs','isAnimalInjury',
                                         'AnimalInjuryIDs','IsFood','FoodIDs',
                                         'isNosocomial','NosocomialIDs']):
        raise Exception(f'Error! File headers are not correct {datapath}. Check https://temu.bsc.es/livingner/submission/')
    # Remove "|" and "+" at the beginning and end of code columns, in case they exist
    df.PetIDs = df.PetIDs.apply(lambda k: k.strip("|"))
    df.PetIDs = df.PetIDs.apply(lambda k: k.strip("+"))
    df.AnimalInjuryIDs = df.AnimalInjuryIDs.apply(lambda k: k.strip("|"))
    df.AnimalInjuryIDs = df.AnimalInjuryIDs.apply(lambda k: k.strip("+"))
    df.FoodIDs = df.FoodIDs.apply(lambda k: k.strip("|"))
    df.FoodIDs = df.FoodIDs.apply(lambda k: k.strip("+"))
    df.NosocomialIDs = df.NosocomialIDs.apply(lambda k: k.strip("|"))
    df.NosocomialIDs = df.NosocomialIDs.apply(lambda k: k.strip("+"))
    
    
    return df