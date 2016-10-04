Customized mongodb's mtools (query tool)

# Install

Needs python 2.7

## Virtualenv (optional, else `sudo pip install`)

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

    ./mloginfo2.py /var/log/mongod.log --queries2

# Tips

To execute only on log after "DateTime":

a. Find the first "DateTime" line number in the mongodb log

b. Copy the contents after that line in another file:

    tail -n +LineNumber /var/log/mongod.log > /var/log/mongod_latest.log
