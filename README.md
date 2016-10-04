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
- hints regarding

# Run

    ./mloginfo2.py mongod.log --queries2
