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
            if 'location_id' in row:
                row['location'] = [row['location_id']]
                del row['location_id']
            record['fields'] = row
            result.append(record)

    with open(json_f, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))


convert_file("ad.csv", 'ads.json', 'ad.ads')
convert_file('category.csv', 'categories.json', 'ad.categories')
convert_file('location.csv', 'location.json', 'users.location')
convert_file('user.csv', 'user.json', 'users.user')
