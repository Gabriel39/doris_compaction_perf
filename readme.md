# Doris Compaction Perf
This is a simple example to test Apache Doris compaction performance.

## How to use

### 1. Create Table
```sql

CREATE TABLE IF NOT EXISTS compaction_tbl
(
    `user_id` LARGEINT NOT NULL COMMENT "用户id",
    `date` DATE NOT NULL COMMENT "数据灌入日期时间",
    `city` VARCHAR(20) COMMENT "用户所在城市",
    `age` SMALLINT COMMENT "用户年龄",
    `sex` TINYINT COMMENT "用户性别",
    `last_visit_date` DATETIME REPLACE DEFAULT "1970-01-01 00:00:00" COMMENT "用户最后一次访问时间",
    `cost` BIGINT SUM DEFAULT "0" COMMENT "用户总消费",
    `max_dwell_time` INT MAX DEFAULT "0" COMMENT "用户最大停留时间",
    `min_dwell_time` INT MIN DEFAULT "99999" COMMENT "用户最小停留时间"
)
AGGREGATE KEY(`user_id`, `date`, `city`, `age`, `sex`)
DISTRIBUTED BY HASH(user_id) PROPERTIES("replication_num" = "1");

```

### 2. Datagen and load to Doris
```shell script
python3 stream_load.py
    --data-gen
    --clean
    --group-size ${group size}
    --round ${num_rounds}
    --db ${database}
    --tbl ${table}
```
notes:
* --data-gen: indicates whether generate new data.
* --clean: indicates whether delete data files after loading to Doris.
* --group-size: this parameter determines aggregate degree. -1 indicates no aggregation happens in compaction progress.
* --round: this parameter determines data size. In a single round, we will produce 500,000 records.
* --db: database used to test.
* --tbl: table used to test.
