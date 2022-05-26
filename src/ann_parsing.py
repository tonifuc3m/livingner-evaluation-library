#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:20:04 2020

@author: antonio
"""
import re
import pandas as pd
import warnings
import csv

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line


def main(datapath, relevant_labels, codes_path):
    
    # Load
    valid_codes = set(map(lambda k: k.strip(), open(codes_path).readlines()))
    df = pd.read_csv(datapath, sep='\t', header=0, quoting=csv.QUOTE_NONE, keep_default_na=False, dtype=str)

    # Check column names are correct
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

    # Check if there are annotations in file
    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df

    # Format DataFrame
    df_ok = df.loc[df['label'].isin(relevant_labels),:].copy()
    df_ok['offset'] = df_ok['off0'].astype(str) + ' ' + df_ok['off1'].astype(str)
    
    # Check if there are duplicated entries
    if df_ok.shape[0] != df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).shape[0]:
        warnings.warn(f"There are duplicated entries in {datapath}. Keeping just the first one...")
        df_ok = df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).copy()
        
    # Format code columns
    if "NCBITax" not in df_ok.columns:
        return df_ok
   
    # Format codes
    df_ok.loc[:,"NCBITax"] = df_ok["NCBITax"].apply(lambda k: format_codes(k))
    
    # Check all codes are valid, return lines with unvalid codes
    unvalid_lines = check_valid_codes_in_column(df_ok, "NCBITax", valid_codes)
    if len(unvalid_lines)>0:
        unvalid_lines_str = list(map(lambda k: str(k+2), unvalid_lines))
        warnings.warn(f"Lines {','.join(unvalid_lines_str)} in {datapath} contain unvalid codes. " +
                  f"Valid codes are those that appear in {codes_path}. " + 
                  "Ignoring ALL PREDICTIONS in lines with unvalid codes...")
        df_ok = df_ok.drop(unvalid_lines).copy()
    return df_ok


def main_subtrack3(datapath, codes_path):
    
    # Load
    valid_codes = set(map(lambda k: k.strip(), open(codes_path).readlines()))
    valid_codes.add('NA')
    df = pd.read_csv(datapath, sep='\t', header=0, quoting=csv.QUOTE_NONE, keep_default_na=False, dtype=str)

    # Check column names are correct
    colnames = ['filename','isPet','PetIDs','isAnimalInjury', 'AnimalInjuryIDs',
                'isFood','FoodIDs', 'isNosocomial','NosocomialIDs']
    if ','.join(df.columns) != ','.join(colnames):
        raise Exception(f'Error! File headers are not correct {datapath}. Check https://temu.bsc.es/livingner/submission/')
        
    # Check if there are annotations in file
    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df
    
    # Check if there are duplicated entries
    if df.shape[0] != df.drop_duplicates(subset=['filename']).shape[0]:
        warnings.warn(f"There are filenames with more than one row in {datapath}. Keeping just the first one...")
        df = df.drop_duplicates(subset=['filename']).copy()
        
    code_columns = ['PetIDs', 'AnimalInjuryIDs', 'FoodIDs', 'NosocomialIDs']

    # Format codes
    for colname in code_columns:
        df.loc[:,colname] = df[colname].apply(lambda k: format_codes_task3(k))
    
    # Check all codes are valid, return lines with unvalid codes
    for colname in code_columns:
        unvalid_lines = check_valid_codes_in_column(df, colname, valid_codes)
        if len(unvalid_lines)>0:
            unvalid_lines_str = list(map(lambda k: str(k+2), unvalid_lines))
            warnings.warn(f"Lines {','.join(unvalid_lines_str)} in {datapath} contain unvalid codes. " +
                  f"Valid codes are those that appear in {codes_path}. " + 
                  "Ignoring ALL PREDICTIONS in lines with unvalid codes...")
            df = df.drop(unvalid_lines).copy()
    
    return df


def format_codes(codes, good_separator='|', bad_separator='+'):
    '''
    Format codes
    1. Force that code separator is correct
    2. In case the code is multiple, sort them and remove duplicated
    3. Remove code separators at the beginning and end of code string
    
    Parameters
    ----------
    codes : string
        Input code string.

    Returns
    -------
    codes_final : string
        Output (formatted) code string.

    '''
    # Make sure separator is "|"
    codes_good_separator = codes.strip().replace(bad_separator, good_separator)
    
    # In case the code is multiple, sort them and remove duplicated
    # E.g. if "9913|9913|3847" was predicted, set it to 3847|9913
    codes_sorted = good_separator.join(sorted(set(codes_good_separator.split(good_separator))))
    
    # Remove separator at the beginning and end of code, in case they exist
    codes_final = codes_sorted.strip(good_separator)
    
    return codes_final


def split_all_codes(k):
    '''
    Split code list using any of the valid separators (+ and |)

    Parameters
    ----------
    k : string
        Codes.

    Returns
    -------
    codes : list
        Codes splitted without |H.

    '''
    codes = k.replace('+', '|').replace('|H','').split('|')
    return codes

def check_valid_codes_in_column(df, colname, valid_codes):
    '''
    Return index with rows that have at least one code not valid

    Parameters
    ----------
    df : pandas DataFrame
        DESCRIPTION.
    colname : string
        DESCRIPTION.
    valid_codes : set
        set of valid codes.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return df.loc[df[colname].apply(lambda k: any([code not in valid_codes for code in split_all_codes(k)])),:].index
    

def isNaN(num):
    return num != num


def format_codes_task3(codes):
    if isNaN(codes) == True:
        return codes
    
    codes_final = ''
    for code in codes.split('+'):
        # Format codes
        codes_final = codes_final + '+' + format_codes(code)
        
    codes_final = format_codes(codes_final, good_separator='+', bad_separator='++')
    
    return codes_final           
            