import csv
import json


def convert_file(csv_f, json_f, model):
    result = []
    with open(csv_f, encoding='utf-8') as csv_file:
        for row in csv.DictReader(csv_file):
            record = {'model': model, 'pk': row['id']}
            del row['id']
            if 'price' in row:
                row['price'] = int(row['price'])
            if 'is_published' in row:
                if row['is_published'] == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            record['fields'] = row
            result.append(record)

    with open(json_f, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))


convert_file("ads.csv", 'ads.json', 'ad.ads')
convert_file('categories.csv', 'categories.json', 'ad.categories')
