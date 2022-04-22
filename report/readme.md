# Doris Compaction Perf

## Settings
* Doris Version: master branch, commit: 2cecb5dc824fc83b8a4312bf9dc4afc94af39ffe
* Cluster: 1 FE, 1 BE
* configurations: default with setting `enable_vectorized_compaction` true or false

## Aggregation Model (Distinct Key)
### Datagen
```shell script
python3 stream_load.py --data-gen --clean --round 100 --db ${database} --tbl ${table}
```

This script will produce **50,000,000 records** and aggregate keys are **distinct** (e.g no aggregation will act in compaction progress).

In addition, these **50,000,000 records** are stored in **10 tablets** and each tablet contains **100 segments**.

### Performance Report
Since 10 tablets are produced, **10 cumulative compactions** will act for compaction.
Compaction duration for compaction is shown in table below:

```
+----------+------------+-----------+
|  tablet  | row-based  |    vec    |
+----------+------------+-----------+
|     0    |  4.50651s  |  3.23533s |
+----------+------------+-----------+
|     1    |  4.60466s  |  3.2464s  |
+----------+------------+-----------+
|     2    |  4.5381s   |  3.29479s |
+----------+------------+-----------+
|     3    |  4.44604s  |  4.3077s  |
+----------+------------+-----------+
|     4    |  4.51567s  |  3.08577s |
+----------+------------+-----------+
|     5    |  4.63237s  |  3.05695s |
+----------+------------+-----------+
|     6    |  5.1851s   |  3.05781s |
+----------+------------+-----------+
|     7    |  4.66245s  |  3.13026s |
+----------+------------+-----------+
|     8    |  4.52761s  |  3.09593s |
+----------+------------+-----------+
|     9    |  4.62887s  |  3.1628s  |
+----------+------------+-----------+
```

## Aggregation Model (Non-distinct Key)
### Datagen
```shell script
python3 stream_load.py --data-gen --clean --group-size 500000 --round 100 --db ${database} --tbl ${table}
```

This script will produce **50,000,000 records** and aggregate keys are **non-distinct** and 500,000 * 9 records will be produced after aggregation.

In addition, these **50,000,000 records** are stored in **10 tablets** and each tablet contains **100 segments**.

### Performance Report
Since 10 tablets are produced, **10 cumulative compactions** will act for compaction.
Compaction duration for compaction is shown in table below:

```
+----------+------------+-----------+
|  tablet  | row-based  |    vec    |
+----------+------------+-----------+
|     0    |  3.45384s  |  3.24612s |
+----------+------------+-----------+
|     1    |  3.51909s  |  3.27603s |
+----------+------------+-----------+
|     2    |  3.17696s  |  3.31839s |
+----------+------------+-----------+
|     3    |  4.46113s  |  3.30366s |
+----------+------------+-----------+
|     4    |  3.2543s   |  3.34808s |
+----------+------------+-----------+
|     5    |  3.25182s  |  3.38383s |
+----------+------------+-----------+
|     6    |  3.24022s  |  3.3118s  |
+----------+------------+-----------+
|     7    |  4.43363s  |  3.40851s |
+----------+------------+-----------+
|     8    |  3.31978s  |  3.4708s  |
+----------+------------+-----------+
|     9    |  3.27898s  |  3.78173s |
+----------+------------+-----------+
```

## Unique Model
### Datagen
```shell script
python3 stream_load_uniq_key.py --data-gen --clean --round 100 --db ${database} --tbl ${table}
```

This script will produce **50,000,000 records** and unique keys are **distinct**.

In addition, these **50,000,000 records** are stored in **10 tablets** and each tablet contains **100 segments**.

### Performance Report
Since 10 tablets are produced, **10 cumulative compactions** will act for compaction.
Compaction duration for compaction is shown in table below:

```
+----------+------------+-----------+
|  tablet  | row-based  |    vec    |
+----------+------------+-----------+
|     0    |  5.0958s   |  3.24098s |
+----------+------------+-----------+
|     1    |  5.31967s  |  3.30468s |
+----------+------------+-----------+
|     2    |  5.18312s  |  3.31836s |
+----------+------------+-----------+
|     3    |  5.26865s  |  3.24619s |
+----------+------------+-----------+
|     4    |  5.27723s  |  3.2069s  |
+----------+------------+-----------+
|     5    |  5.09684s  |  3.87789s |
+----------+------------+-----------+
|     6    |  5.14861s  |  3.29264s |
+----------+------------+-----------+
|     7    |  5.21604s  |  3.20101s |
+----------+------------+-----------+
|     8    |  5.24844s  |  3.19146s |
+----------+------------+-----------+
|     9    |  6.0967s   |  3.31636s |
+----------+------------+-----------+
```

## Duplicate Model
### Datagen
```shell script
python3 stream_load_dup_key.py --data-gen --clean --round 100 --db ${database} --tbl ${table}
```

This script will produce **50,000,000 records** and unique keys are **distinct**.

In addition, these **50,000,000 records** are stored in **10 tablets** and each tablet contains **100 segments**.

### Performance Report
Since 10 tablets are produced, **10 cumulative compactions** will act for compaction.
Compaction duration for compaction is shown in table below:

```
+----------+------------+-----------+
|  tablet  | row-based  |    vec    |
+----------+------------+-----------+
|     0    |  3.78454s  |  2.40708s |
+----------+------------+-----------+
|     1    |  3.86628s  |  2.44498s |
+----------+------------+-----------+
|     2    |  3.76453s  |  2.33053s |
+----------+------------+-----------+
|     3    |  3.83636s  |  2.86924s |
+----------+------------+-----------+
|     4    |  3.73134s  |  2.61043s |
+----------+------------+-----------+
|     5    |  3.86787s  |  2.32863s |
+----------+------------+-----------+
|     6    |  3.81543s  |  2.33837s |
+----------+------------+-----------+
|     7    |  4.03008s  |  2.33692s |
+----------+------------+-----------+
|     8    |  4.14989s  |  2.42682s |
+----------+------------+-----------+
|     9    |  4.25672s  |  2.40349s |
+----------+------------+-----------+
```

Based this result, we can reasonably assume that vectorized compaction is more efficient.
