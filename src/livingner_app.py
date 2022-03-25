#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:22:29 2022

@author: tonifuc3m
"""
# TODO

import warnings

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line

def main(gs_path, pred_path):
    warnings.warn("The Clinical Impact Track evaluation library is still not available")
    
    