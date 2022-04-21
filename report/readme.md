# Doris Compaction Perf

## Settings
* Doris Version: master branch, commit: 2cecb5dc824fc83b8a4312bf9dc4afc94af39ffe
* Cluster: 1 FE, 1 BE
* configurations: default with setting `enable_vectorized_compaction` true or false

## Datagen
```shell script
python3 stream_load.py --data-gen --clean --round 100 --db ${database} --tbl ${table}
```

This script will produce **50,000,000 records** and aggregate keys are **distinct** (e.g no aggregation will act in compaction progress).

In addition, these **50,000,000 records** are stored in **10 tablets** and each tablet contains **100 segments**.

## Performance Report
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

Based this result, we can reasonably assume that vectorized compaction is more efficient.
