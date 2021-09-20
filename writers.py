import csv
import json
import sqlite3


class TxtWriter:

    def __init__(self):
        self.file = open('./results.txt', 'w')

    def write(self, item: dict):
        self.file.write(f"{item}\n")


class CSVWriter:
    def __init__(self):
        self._file = open('results.csv', 'w')
        self.writer = csv.writer(self._file)
        self._headers = None

    def write(self, item: dict):

        if self._headers is None:
            # write the header
            self.writer.writerow(list(item.keys()))

        # write the data
        self.writer.writerow(list(item.values()))


class DBWriter:

    def write(self, item):
        con = sqlite3.connect('./jobs.db')
        cur = con.cursor()
        sql_create_jobs = """
            CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY,
            id_job INTEGER,
            title VARCHAR(100),
            job_title VARCHAR(100),
            payment VARCHAR(100),
            href VARCHAR(50),
            job_description VARCHAR(10000));
            """
        # It should be create an ability to delete data from user and data from phones will be deleted by cascade
        # Create table
        cur.execute(sql_create_jobs)
        con.commit()
        sql_insert_value_in_users = f"INSERT INTO jobs values (null,'{item['id']}', '{item['title']}', '{item['job_title']}', '{item['payment']}', '{item['href']}','{item['job_description']}');"
        cur.execute(sql_insert_value_in_users)
        con.commit()
        con.close()



# class JSONWriter:
#
#     def __init__(self):
#         self._file = open("results.json", "w", encoding='utf-8')
#
#     def write(self, item: dict):
#         output = []
#         json_list = []
#         for i in item:
#             output.append(item)
#         for list in output:
#             json_list.extend(output)
#         print(json_list)
#         print(type(json_list))
#
#         # json.dumps(json_list, ensure_ascii=False, indent=6)
#         json.dump(json_list, self._file, ensure_ascii=False, indent=6)
#         # for j in json_data:
#         #     json_list.append(parse(json_data))
#         # print(json_data)
#         # self._file.write(json_list)
