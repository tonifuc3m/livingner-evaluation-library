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
python main.py -g ../gs-data/sample_entities_subtask2.tsv -p ../toy-data/sample_entities_subtask2_MISSING_ONE_FILE.tsv -s norm
```

+ LivingNER-Clinical IMPACT

This code is still not included

```
cd src
python main.py -g ../gs-data/sample_entities_subtask3.tsv -p ../toy-data/pred_sample_entities_subtask3.tsv -s app
```

# 4. Other interesting stuff:

### Metrics

For LivingNER-Species NER and LivingNER-Species Norm, the relevant metrics are precision, recall and f1-score. The latter will be used to decide the award winners.

For LivingNER-Clinical IMPACT, the relevant metric is still to be disclosed.

For more information about metrics, see the shared task webpage: https://temu.bsc.es/livingner/

### Script Arguments
+ ```-g/--gs_path```: path to Gold Standard TSV file with the annotations
+ ```-p/--pred_path```: path to predictions TSV file with the annotations
+ ```-c/--valid_codes_path```: path to TSV file with valid codes (provided here).
+ ```-s/--subtask```: subtask name (```ner```, ```norm```, or ```app```).

### Examples: 

+ LivingNER-Species NER

```
$ cd src
$ python main.py -g ../gs-data/sample_entities_subtask1.tsv -p ../toy-data/sample_entities_subtask1_MISSING_ONE_FILE.tsv -s ner

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


Micro-average recall = 0.957


Micro-average F-score = 0.978

../toy-data/sample_entities_subtask1_MISSING_ONE_FILE.tsv|1.0|0.957|0.978
```

+ LivingNER-Species Norm

```
$ cd src
$ python main.py -g ../gs-data/sample_entities_subtask2.tsv -p ../toy-data/sample_entities_subtask2_MISSING_ONE_FILE.tsv -s norm

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


Micro-average recall = 0.957


Micro-average F-score = 0.978

../toy-data/sample_entities_subtask2_MISSING_ONE_FILE.tsv|1.0|0.957|0.978
```

+ LivingNER-Clinical IMPACT

```
$ cd src
$ python main.py -g ../gs-data/sample_entities_subtask3.tsv -p ../toy-data/pred_sample_entities_subtask3.tsv -s app
/home/antonio/Documents/Work/BSC/Projects/micro/scripts/livingner-evaluation-library/src/livingner_app.py:17: UserWarning: The Clinical Impact Track evaluation library is still not available

```

