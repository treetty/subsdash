"""
Database ingestion and querying
"""

import csv

from app import db, Mapping, Product


# Initiate Database
db.create_all()


# Populate Database

ATTR_PATH = 'csv/prod_attr.tsv'
MAPPING_PATH = 'csv/subs_mapping.tsv'

with open(ATTR_PATH, 'r') as f:
    csvreader = csv.reader(f, delimiter='\t')
    for row in csvreader:
        prod_id = row[0]
        name = row[1]
        size = row[3]
        uom = row[4]
        brand_desc = row[6]
        db.session.add(Product(prod_id, name, size, uom, brand_desc))
    db.session.commit()


with open(MAPPING_PATH, 'r') as f:
    csvreader = csv.reader(f, delimiter='\t')
    for row in csvreader:
        page = row[0]
        orig_id = row[1]
        pc_id = row[2]
        db.session.add(Mapping(page, orig_id, pc_id))
    db.session.commit()