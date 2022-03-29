#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:22:29 2022

@author: tonifuc3m
"""
# TODO
import ann_parsing
import warnings
import pandas as pd

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line

def isNaN(num):
    return num != num

def sort_codes(codes):
    return '+'.join(sorted(list(set(codes.split('+')))))
    
def main(gs_path, pred_path):
    
    gs = ann_parsing.main_subtrack3(gs_path)
    pred = ann_parsing.main_subtrack3(pred_path)
    
    # Remove predicted duplicated codes & Order them to allow string comparison with
    # Gold Standard
    # E.g. if "3847+9913+9913" was predicted, set it to 3847+9913
    colnames = ['Pet', 'Attack', 'Food']
    for colname in colnames:
        pred[colname.lower() + '_codes'] = pred[colname.lower() + '_codes'].\
            apply(lambda k: sort_codes(k) if isNaN(k) == False else k)
    
        gs[colname.lower() + '_codes'] = gs[colname.lower() + '_codes'].\
            apply(lambda k: sort_codes(k) if isNaN(k) == False else k)
    
    # Compute metrics
    colnames = ['Pet', 'Attack', 'Food']
    print("Basic metrics (not taking into account NCBI codes, just Y/N assignment)")
    print('-----------------------------------------------------')
    for colname in colnames: 
        print(colname)
        P_simple, R_simple, F1_simple, _, _, _ = compute_metrics(gs, pred, colname)
        print(f"Precision = {P_simple}")
        print(f"Recall = {R_simple}")
        print(f"F1score = {F1_simple}")
        print('-----------------------------------------------------')
    print('\n\n')
        
    print("Complex metrics (taking into account NCBI codes)")
    print('-----------------------------------------------------')
    for colname in colnames: 
        print(colname)
        _, _, _ , P_complex, R_complex, F1_complex = compute_metrics(gs, pred, colname)
        print(f"Precision = {P_complex}")
        print(f"Recall = {R_complex}")
        print(f"F1score = {F1_complex}")
        print('-----------------------------------------------------')
    print('\n\n')
    
    # TODO: consider accepting parents and/or children? In several cases, it is described that
    # "an insect" bites, and several sentences below it is specified that the
    # insect is actually a mosquito, or other animal
    # I am worried about this in the attack category, mainly. Food does not
    # present this problem. And in pets the problem is almost non-eistent
    # The main problem I see with food is my bias when annotating. We are annotating
    # all SPECIES that are "eatable". I am not annotating dogs, but I include cows
    # The issue I see with Pets are the distinction between sporadic and regular contacts.
    
    warnings.warn("The Clinical Impact Track evaluation library is still not available")
    
def compute_metrics(gs, pred, colname):
    
    colname_v1 = 'is' + colname
    colname_v2 = colname.lower() + '_codes'
    
    pred_this = pred[["filename", colname_v1, colname_v2]]
    gs_this = gs[["filename", colname_v1, colname_v2]]
    
    Pred_Pos = pred_this.loc[pred_this[colname_v1]=='Y'].shape[0]
    GS_Pos = gs_this.loc[gs_this[colname_v1]=='Y'].shape[0]
    
    df_sel = pd.merge(pred_this, gs_this,  how="right", on=["filename"])
    
    TP_simple = df_sel.loc[(df_sel[colname_v1 + '_y']=='Y') & 
                    (df_sel[colname_v1 + '_y']==df_sel[colname_v1 + '_x']),:].shape[0]
    
    # I am doing a string comparison to get the complex scores. This means,
    # The final metric is going to be macro-averaged by document. 
    # TODO: decide whether I want this macro-metric or something more micro-metric
    # based on codes. 
    # TODO: Finally, also decide if I am allowing child or parent nodes
    TP_complex = df_sel.loc[(df_sel[colname_v1 + '_y']=='Y') & 
                    (df_sel[colname_v2 + '_y']==df_sel[colname_v2 + '_x']),:].shape[0]
    
    if (Pred_Pos) == 0:
        P_simple = 0
        P_complex = 0
        warnings.warn('Precision score automatically set to zero because there are no predicted positives')
    else:
        P_simple = TP_simple/Pred_Pos
        P_complex = TP_complex/Pred_Pos
    if GS_Pos == 0:
        R_simple = 0
        R_complex = 0
        warnings.warn('Recall score automatically set to zero because there are no Gold Standard positives')
    else:
        R_simple = TP_simple/GS_Pos
        R_complex = TP_complex/GS_Pos
        
    if P_simple+R_simple == 0:
        F1_simple = 0
        warnings.warn('Global F1 score automatically set to zero for simple metrics to avoid division by zero')
    else:
        F1_simple = (2 * P_simple * R_simple) / (P_simple + R_simple)
        
    if P_complex+R_complex == 0:
        F1_complex = 0
        warnings.warn('Global F1 score automatically set to zero for complex metrics to avoid division by zero')
    else:
        F1_complex = (2 * P_complex * R_complex) / (P_complex + R_complex)
    
    return P_simple, R_simple, F1_simple, P_complex, R_complex, F1_complex