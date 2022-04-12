#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:22:29 2022

@author: tonifuc3m
"""
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
    
def main(gs_path, pred_path, codes_path):
    
    gs = ann_parsing.main_subtrack3(gs_path, codes_path)
    pred = ann_parsing.main_subtrack3(pred_path, codes_path)
    
    clinical_application = ['Pet', 'AnimalInjury', 'Food', 'Nosocomial']
    
    # Remove predicted duplicated codes & Order them to allow string comparison with
    # Gold Standard
    # E.g. if "3847+9913+9913" was predicted, set it to 3847+9913
    for colname in clinical_application:
        pred[colname + 'IDs'] = pred[colname + 'IDs'].\
            apply(lambda k: sort_codes(k) if isNaN(k) == False else k)
    
        gs[colname + 'IDs'] = gs[colname + 'IDs'].\
            apply(lambda k: sort_codes(k) if isNaN(k) == False else k)
    
    # TODO: check codes are in terminology

    # Compute metrics
    print("Basic metrics (not taking into account NCBI codes, just Y/N assignment)")
    print('-----------------------------------------------------')
    for colname in clinical_application: 
        print(colname)
        P_simple, R_simple, F1_simple, _, _, _ = compute_metrics(gs, pred, colname)
        print(f"Precision = {round(P_simple, 4)}")
        print(f"Recall = {round(R_simple, 4)}")
        print(f"F1score = {round(F1_simple, 4)}")
        print('-----------------------------------------------------')
    print('\n\n')
        
    print("Complex metrics (taking into account NCBI codes)")
    print('-----------------------------------------------------')
    for colname in clinical_application: 
        print(colname)
        _, _, _ , P_complex, R_complex, F1_complex = compute_metrics(gs, pred, colname)
        print(f"Precision = {round(P_complex, 4)}")
        print(f"Recall = {round(R_complex, 4)}")
        print(f"F1score = {round(F1_complex, 4)}")
        print('-----------------------------------------------------')
    print('\n\n')

    
def compute_metrics(gs, pred, colname):
    
    colname_v1 = 'is' + colname
    colname_v2 = colname + 'IDs'
    
    pred_this = pred[["filename", colname_v1, colname_v2]].copy()
    gs_this = gs[["filename", colname_v1, colname_v2]].copy()
    
    Pred_Pos = pred_this.loc[pred_this[colname_v1]=='Yes'].shape[0]
    GS_Pos = gs_this.loc[gs_this[colname_v1]=='Yes'].shape[0]
    
    df_sel = pd.merge(pred_this, gs_this,  how="right", on=["filename"])
    
    TP_simple = df_sel.loc[(df_sel[colname_v1 + '_y']=='Yes') & (df_sel[colname_v1 + '_x']=='Yes'),:].shape[0]
    
    # I am doing a string comparison to get the complex scores. This means,
    # The final metric is going to be macro-averaged by document. 
    # TODO: macro-metric (based on documents, current) vs micro-metric based on codes. 
    # TODO: allowing vs not allowing child or parent nodes
    TP_complex = df_sel.loc[(df_sel[colname_v1 + '_y']=='Yes') & (df_sel[colname_v1 + '_x']=='Yes') & 
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