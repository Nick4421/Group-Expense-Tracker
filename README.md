# Group Expense Project

```source .venv/bin/activate``` to activate virtual environment

```deactivate``` to stop running in the virtual environment

Must be running in the virtual environment for this to work

(Input functions are broken otherwise due to the outdated python version)

Init file format
member:
    - member name
    - member balance
expense:
    - expense name
    - expense payer
    - expense amount
    - number of payees
    - list of the payees

TODO
- Large scale test reimbursement function
- Get rid of class and just use variable attributes
- Implement multiple different groups
- Be able to delete expenses