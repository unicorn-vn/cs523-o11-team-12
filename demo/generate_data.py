import csv
import random
from faker import Faker
fake = Faker()

rows = 1000000
columns = 4

def generate_random_row(col):
    a = []
    l = [init_id, fake.name(), fake.email(), fake.phone_number(), round(random.uniform(0, 10), 1)]
    a.append(l)
    return a

if __name__ == '__main__':
    f = open('data_test/1m_rows.csv', 'w')
    w = csv.writer(f, lineterminator='\n')
    w.writerows([['MSSV', 'Ten', 'Email', 'SDT', 'Diem']])
    init_id = 19300059
    for i in range(rows):
        print("\r>> You have finished {} rows".format(i), end='')
        w.writerows(generate_random_row(columns))
        init_id += 1
    f.close()