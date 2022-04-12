# 1. Introduction

Scripts to compute LivingNER evaluation metrics.

Written in Python 3.7

Output is printed in terminal.

# 2. Requirements

+ Python3
+ pandas

To install them: 
```
pip install -r requirements.txt
```


# 3. Execution
+ LivingNER-Species NER

```
cd src  
python main.py -g ../gs-data/sample_entities_subtask1.tsv -p ../toy-data/sample_entities_subtask1_MISSING_ONE_FILE.tsv -s ner
```

+ LivingNER-Species Norm

```
cd src
python main.py -g ../gs-data/sample_entities_subtask2.tsv -p ../toy-data/sample_entities_subtask2_predictions.tsv -s norm
```

+ LivingNER-Clinical IMPACT

This code is still not included

```
cd src
python main.py -g ../gs-data/sample_subtask3.tsv -p ../toy-data/sample_subtask3_predictions.tsv -s app
```

# 4. Other interesting stuff:

### Metrics

For the three subtasks, the relevant metrics are precision, recall and f1-score. The latter will be used to decide the award winners.

For more information about metrics, see the shared task webpage: https://temu.bsc.es/livingner/

### Script Arguments
+ ```-g/--gs_path```: path to Gold Standard TSV file with the annotations
+ ```-p/--pred_path```: path to predictions TSV file with the annotations
+ ```-c/--valid_codes_path```: path to TSV file with valid codes (provided here). Default is ../ncbi_codes_unique.tsv
+ ```-s/--subtask```: subtask name (```ner```, ```norm```, or ```app```).

### Examples: 

+ LivingNER-Species NER

```
$ cd src
$ python main.py -g ../gs-data/sample_entities_subtask1.tsv -p ../toy-data/sample_entities_subtask1_MISSING_ONE_FILE.tsv -s ner
According to file headers, you are on subtask ner
According to file headers, you are on subtask ner

-----------------------------------------------------
Clinical case name			Precision
-----------------------------------------------------
32032497_ES		nan
-----------------------------------------------------
caso_clinico_medtropical54		1.0
-----------------------------------------------------
casos_clinicos_infecciosas1		1.0
-----------------------------------------------------
casos_clinicos_infecciosas141		1.0
-----------------------------------------------------
cc_onco908		1.0
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			Recall
-----------------------------------------------------
32032497_ES		0.0
-----------------------------------------------------
caso_clinico_medtropical54		1.0
-----------------------------------------------------
casos_clinicos_infecciosas1		1.0
-----------------------------------------------------
casos_clinicos_infecciosas141		1.0
-----------------------------------------------------
cc_onco908		1.0
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			F-score
-----------------------------------------------------
32032497_ES		nan
-----------------------------------------------------
caso_clinico_medtropical54		1.0
-----------------------------------------------------
casos_clinicos_infecciosas1		1.0
-----------------------------------------------------
casos_clinicos_infecciosas141		1.0
-----------------------------------------------------
cc_onco908		1.0
-----------------------------------------------------

-----------------------------------------------------
Micro-average metrics
-----------------------------------------------------

Micro-average precision = 1.0


Micro-average recall = 0.9568


Micro-average F-score = 0.9779

../toy-data/sample_entities_subtask1_MISSING_ONE_FILE.tsv|1.0|0.9568|0.9779
```

+ LivingNER-Species Norm

```
$ cd src
$ python main.py -g ../gs-data/sample_entities_subtask2.tsv -p ../toy-data/sample_entities_subtask2_predictions.tsv -s norm
According to file headers, you are on subtask norm, GS file
According to file headers, you are on subtask norm, predictions file
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/ann_parsing.py:46: UserWarning: There are duplicated entries in ../toy-data/sample_entities_subtask2_predictions.tsv. Keeping just the first one...
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/ann_parsing.py:59: UserWarning: Lines 1 in ../toy-data/sample_entities_subtask2_predictions.tsv contain unvalid codes. Valid codes are those that appear in ../ncbi_codes_unique.tsv. Ignoring lines with valid codes...

-----------------------------------------------------
Clinical case name			Precision
-----------------------------------------------------
32032497_ES		0.5
-----------------------------------------------------
caso_clinico_medtropical54		1.0
-----------------------------------------------------
casos_clinicos_infecciosas1		1.0
-----------------------------------------------------
casos_clinicos_infecciosas141		1.0
-----------------------------------------------------
cc_onco908		1.0
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			Recall
-----------------------------------------------------
32032497_ES		0.3333
-----------------------------------------------------
caso_clinico_medtropical54		1.0
-----------------------------------------------------
casos_clinicos_infecciosas1		1.0
-----------------------------------------------------
casos_clinicos_infecciosas141		1.0
-----------------------------------------------------
cc_onco908		1.0
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			F-score
-----------------------------------------------------
32032497_ES		0.4
-----------------------------------------------------
caso_clinico_medtropical54		1.0
-----------------------------------------------------
casos_clinicos_infecciosas1		1.0
-----------------------------------------------------
casos_clinicos_infecciosas141		1.0
-----------------------------------------------------
cc_onco908		1.0
-----------------------------------------------------

-----------------------------------------------------
Micro-average metrics
-----------------------------------------------------

Micro-average precision = 0.9854


Micro-average recall = 0.9712


Micro-average F-score = 0.9783

../toy-data/sample_entities_subtask2_predictions.tsv|0.9854|0.9712|0.9783
```

+ LivingNER-Clinical IMPACT

```
$ cd src
$ python main.py -g ../gs-data/sample_subtask3.tsv -p ../toy-data/sample_subtask3_predictions.tsv -s app
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/ann_parsing.py:99: UserWarning: Lines 5 in ../toy-data/sample_subtask3_predictions.tsv contain unvalid codes. Valid codes are those that appear in ../ncbi_codes_unique.tsv. Ignoring lines with valid codes...
Basic metrics (not taking into account NCBI codes, just Y/N assignment)
-----------------------------------------------------
Pet
Precision = 1.0
Recall = 1.0
F1score = 1.0
-----------------------------------------------------
AnimalInjury
Precision = 1.0
Recall = 1.0
F1score = 1.0
-----------------------------------------------------
Food
Precision = 1.0
Recall = 1.0
F1score = 1.0
-----------------------------------------------------
Nosocomial
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/livingner_app.py:90: UserWarning: Precision score automatically set to zero because there are no predicted positives
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/livingner_app.py:104: UserWarning: Global F1 score automatically set to zero for simple metrics to avoid division by zero
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/livingner_app.py:110: UserWarning: Global F1 score automatically set to zero for complex metrics to avoid division by zero
Precision = 0
Recall = 0.0
F1score = 0
-----------------------------------------------------



Complex metrics (taking into account NCBI codes)
-----------------------------------------------------
Pet
Precision = 1.0
Recall = 1.0
F1score = 1.0
-----------------------------------------------------
AnimalInjury
Precision = 1.0
Recall = 1.0
F1score = 1.0
-----------------------------------------------------
Food
Precision = 1.0
Recall = 1.0
F1score = 1.0
-----------------------------------------------------
Nosocomial
Precision = 0
Recall = 0.0
F1score = 0
-----------------------------------------------------
```

