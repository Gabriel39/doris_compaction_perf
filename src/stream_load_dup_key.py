import json
import random
import os
import argparse


def run(data_gen, clean, group_size, db, tbl, num_rounds):
    arr = []
    for j in range(num_rounds):
        print('===================== round %s ====================' % j)
        file_name = 'file_%s.json' % j
        if data_gen:
            print("====== data_gen is True so gen data")
            with open(file_name, 'w') as f:
                for i in range(j * 500000, j * 500000 + 500000):
                    item = {'user_id': i % group_size if group_size > 0 else i, 'timestamp': '2020-01-01 10:00:0%s' % (i % 10 if group_size > 0 else i),
                            'type': i % group_size if group_size > 0 else i, 'error_code': 18, 'error_msg': 'error_msg',
                            'op_id': 1, 'op_time': '2020-01-01 10:00:00'}
                    arr.append(item)
                json.dump(arr, f)
        load_output = os.popen('curl -v --location-trusted -u root: -H "format: json" -H "strip_outer_array: true" '
                               '-H "disable_auto_compaction: true" -T %s '
                               'http://127.0.0.1:8030/api/%s/%s/_stream_load' % (file_name, db, tbl)).read()
        print(load_output)
        if clean and os.path.exists(file_name):
            print("====== clean is True so delete json files")
            os.remove(file_name)
        arr = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--data-gen', action='store_true')
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--group-size', type=int, default=-1)
    parser.add_argument('--round', type=int, default=100)
    parser.add_argument('--db', type=str, default='compaction')
    parser.add_argument('--tbl', type=str, default='compaction_tbl')

    args = parser.parse_args()
    run(args.data_gen, args.clean, args.group_size, args.db, args.tbl, args.round)
