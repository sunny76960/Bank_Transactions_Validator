# Bank Transaction Validator

**Problem Statement No. 30** – Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
B.Tech CSE, First Semester, Section J – Rungta International Skills University

> **Student:** YOUR NAME HERE  |  **Roll No.:** YOUR ROLL NO  |  **Section:** J

## About the project
A Python 3 console program that reads bank transactions from a text file, checks each
one against banking rules, prints **Valid** or **Invalid** with the reason, keeps track of
the balance, shows a summary, and saves the valid transactions to a new file.

**Concepts used:** Functions, Conditions, Exceptions, File Handling.
No external libraries are needed – only the Python standard library.

## Banking rules
| # | Rule | Message when it fails |
|---|------|-----------------------|
| 1 | Type must be `Deposit` or `Withdraw` | `unknown type 'Transfer'.` |
| 2 | Amount must be a number | `amount 'abc' is not a number.` |
| 3 | Amount must be positive | `amount must be positive.` |
| 4 | Amount must not exceed 100000 | `exceeds limit of 100000.` |
| 5 | A withdrawal cannot exceed the balance | `insufficient balance.` |

* Opening balance is **10000**.
* Only **valid** transactions change the balance.

## How to run (VS Code)
1. Install Python 3.8+ from <https://www.python.org> (tick **Add Python to PATH**).
2. In VS Code: **File → Open Folder…** and choose the `bank-transaction-validator` folder.
3. Open the terminal: **Terminal → New Terminal**.
4. Run:

```bash
python bank_transaction_validator.py
```
(On Mac/Linux use `python3`. You can also open the `.py` file and click the ▶ Run button.)

To use a different input file (and optionally a different output file):
```bash
python bank_transaction_validator.py sample_inputs/test_case_3_invalid.txt
python bank_transaction_validator.py my_input.txt my_valid_output.txt
```

## Input file format
`transactions.txt` – one transaction per line as `Type,Amount`:
```
Deposit,5000
Withdraw,2000
```

## Sample output
```
Line 1: Valid │ Balance: 15000
Line 2: Valid │ Balance: 13000
Valid: 2 │ Invalid: 0 │ Final balance: 13000
Valid transactions saved to 'valid_transactions.txt'.
```

## Test cases from the problem statement
Ready-made input files are in `sample_inputs/`.

| Test case | Input file | Expected summary |
|-----------|-----------|------------------|
| 1 – Normal | `test_case_1_normal.txt` | `Valid: 2 │ Invalid: 0 │ Final balance: 13000` |
| 2 – Boundary | `test_case_2_boundary.txt` | `Valid: 1 │ Invalid: 0 │ Final balance: 0` |
| 3 – Invalid | `test_case_3_invalid.txt` | `Valid: 0 │ Invalid: 4 │ Final balance: 10000` |
| 4 – Different | `test_case_4_different.txt` | `Valid: 2 │ Invalid: 1 │ Final balance: 0` |

Run the automated tests (16 tests, includes all 4 above):
```bash
python -m unittest -v
```

## Project structure
```
bank-transaction-validator/
├── bank_transaction_validator.py   # main program (single .py file)
├── transactions.txt                # default input file
├── sample_inputs/                  # the 4 test cases from the problem statement
├── tests/test_validator.py         # automated tests
├── docs/REPORT.md                  # project report
├── docs/VIVA_NOTES.md              # explanation + viva questions
├── README.md
└── .gitignore
```

## Main functions
| Function | Purpose |
|----------|---------|
| `validate_transaction(line, balance)` | Checks type, amount, limit and balance; returns valid/invalid + reason |
| `process_transactions(lines)` | Goes through all lines and updates the balance for valid ones |
| `read_transactions(filename)` | Reads the file (missing file handled with try-except in `main`) |
| `save_valid_transactions(results, filename)` | Saves valid transactions to `valid_transactions.txt` |
| `print_report(results, final_balance)` | Prints each line result and the summary |
| `format_amount(value)` | Shows `13000` instead of `13000.00` |
