import csv
import json
import yaml

### Read from CSV file
with open('domain_names.csv') as f:
    csv_reader = csv.reader(f)

# csv.reader() returns an iterable and we can walk through rows and each row is a list
    for row in csv_reader:
        print(row)


### Write to CSV file

headers = ['Name', 'Class', 'Birthday']
children = [('Ann', '1A', '12.01.2010'),
            ('Mark', '1B', '09.03.2015'),
            ['Jim', '1C', '17.09.2008']]

with open('write_csv.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(children)


### Read from CSV with DictReader
with open('domain_names.csv') as f:
    csv_dict_reader = csv.DictReader(f)

    for row in csv_dict_reader:
        print(row)
# csv.DictReader() returns an iterable and we can walk through rows and each row is a dictionary with keys - headers (the first row)


### Write from CSV with DictWriter
rows = [{headers[j] : children[i][j] for j in range(len(headers))} for i in range(len(children))]
print(rows)

with open('write_dict_csv.csv', 'w') as f:
    csv_dict_writer = csv.DictWriter(f, rows[0].keys())
# csv.DictWriter() writes a list of dictionaries where keys are header fields
    csv_dict_writer.writeheader()
    csv_dict_writer.writerows(rows)



### =============================================================================

### Read from JSON
j_s = """{
  "children" : [
    {"Name" :  "Billy",
    "Class" :  "2B",
    "Birthday" :  "13.07.2006"},
    {"Name" :  "Sarah",
    "Class" :  "2C",
    "Birthday" :  "02.06.2007"},
    {"Name" :  "Eric",
    "Class" :  "2A",
    "Birthday" :  "01.03.2008"}

  ]
}
"""

with open('birthdays.json') as f:
    d = json.load(f)
    print(d)

d1 = json.loads(j_s)
print(d1)

with open('write_json.json') as f:
    d2 = json.load(f)
    print(d2)

### Write to JSON

with open('write_json.json', 'w') as f:
    json.dump(rows, f)
with open('write_json2.json', 'w') as f:
    json.dump(d, f, indent=2, sort_keys=True)

print(json.dumps(rows))

### =============================================================================

### Read from YAML

with open('books.yaml') as f:
    books = yaml.safe_load(f)
    print(books)


### Write to YAML
with open('birtdays.yaml', 'w') as f:
    yaml.dump(d, f)