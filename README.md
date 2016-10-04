Customized mongodb's mtools (query tool)

# Install

Needs python 2.7.

## Virtualenv

    virtualenv venv
    source venv/bin/activate

## Pip packages

    pip install -r requirements.freeze.txt

# What does it do
    
- grouping by collection (useful for multitenant implemented by separate dbs)
- limit to top 30 elements
- sorting by total time
- [TODO] connects to db, displays hints on existing indexes

# Run

    ./mloginfo2.py mongod.log --queries2

# Tips

To execute only on log after "DateTime":

a. Find the first "DateTime" line number in the mongodb log

b. Copy the contents after that line in another file:

    tail -n +LineNumber /path/to/file > /var/log/mongodb_latest.log
