from app import mongo

def insert_raw_jobs(data):
    collection = mongo["jobs"]["raw_jobs"]
    collection.insert_many(data)