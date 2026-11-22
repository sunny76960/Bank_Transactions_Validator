"""
Bank Transaction Validator  (Problem Statement No. 30)
------------------------------------------------------
Reads bank transactions from a text file (one "Type,Amount" per line),
checks each one against the banking rules, prints Valid / Invalid with the
reason, updates the balance only for valid transactions, shows a summary and
saves the valid transactions to a file.

Banking rules
  1. Type must be Deposit or Withdraw.
  2. Amount must be a number.
  3. Amount must be positive.
  4. Amount must not exceed 100000 per transaction.
  5. A withdrawal cannot be more than the current balance.

Run:  python bank_transaction_validator.py
      python bank_transaction_validator.py my_file.txt
"""

import sys
from decimal import Decimal, InvalidOperation

OPENING_BALANCE = Decimal("10000")
MAX_AMOUNT = Decimal("100000")
VALID_TYPES = ("Deposit", "Withdraw")

DEFAULT_INPUT_FILE = "transactions.txt"
DEFAULT_OUTPUT_FILE = "valid_transactions.txt"


def format_amount(value):
    """Show whole numbers without decimals (13000) and others with 2 (13000.50)."""
    if value == value.to_integral_value():
        return str(int(value))
    return f"{value:.2f}"


def validate_transaction(line, balance):
    """
    Check one line of the file against all banking rules.

    Returns a tuple: (is_valid, reason, kind, amount)
      is_valid -> True / False
      reason   -> why it is invalid ("" when valid)
      kind     -> "Deposit" or "Withdraw" (None if the type was invalid)
      amount   -> Decimal amount (None if the amount was invalid)
    """
    parts = line.split(",")
    if len(parts) != 2:
        return False, "line must be in the format Type,Amount.", None, None

    type_text = parts[0].strip()
    amount_text = parts[1].strip()

    # Rule 1: type
    kind = type_text.capitalize()
    if kind not in VALID_TYPES:
        return False, f"unknown type '{type_text}'.", None, None

    # Rule 2: amount must be a number (reject nan / inf too)
    try:
        amount = Decimal(amount_text)
        if not amount.is_finite():
            raise InvalidOperation
    except InvalidOperation:
        return False, f"amount '{amount_text}' is not a number.", kind, None

    # Rule 3: positive
    if amount <= 0:
        return False, "amount must be positive.", kind, amount

    # Rule 4: per-transaction limit
    if amount > MAX_AMOUNT:
        return False, f"exceeds limit of {format_amount(MAX_AMOUNT)}.", kind, amount

    # Rule 5: withdrawal cannot exceed balance
    if kind == "Withdraw" and amount > balance:
        return False, "insufficient balance.", kind, amount

    return True, "", kind, amount


def process_transactions(lines, opening_balance=OPENING_BALANCE):
    """
    Validate every line in order. Only valid transactions change the balance.

    Returns (results, balance) where results is a list of dicts:
      {"line_no", "valid", "reason", "kind", "amount", "balance"}
    """
    balance = opening_balance
    results = []

    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if line == "":              # ignore blank lines (line numbers still count)
            continue

        is_valid, reason, kind, amount = validate_transaction(line, balance)

        if is_valid:
            if kind == "Deposit":
                balance += amount
            else:
                balance -= amount

        results.append({
            "line_no": line_no,
            "valid": is_valid,
            "reason": reason,
            "kind": kind,
            "amount": amount,
            "balance": balance,
        })

    return results, balance


def read_transactions(filename):
    """Read all lines of the file. Raises FileNotFoundError if it is missing."""
    # utf-8-sig also handles files saved with a BOM by Windows Notepad
    with open(filename, "r", encoding="utf-8-sig") as file:
        return file.readlines()


def save_valid_transactions(results, filename):
    """Write only the valid transactions to a file, in Type,Amount format."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in results:
            if item["valid"]:
                file.write(f"{item['kind']},{format_amount(item['amount'])}\n")


def print_report(results, final_balance):
    """Print one line per transaction and then the summary."""
    for item in results:
        if item["valid"]:
            print(f"Line {item['line_no']}: Valid │ Balance: {format_amount(item['balance'])}")
        else:
            print(f"Line {item['line_no']}: Invalid – {item['reason']}")

    valid_count = sum(1 for item in results if item["valid"])
    invalid_count = len(results) - valid_count
    print(f"Valid: {valid_count} │ Invalid: {invalid_count} │ "
          f"Final balance: {format_amount(final_balance)}")


def main(argv=None):
    """Program entry point. Returns 0 on success, 1 on error."""
    # Make sure symbols like │ and – print correctly on the Windows console too
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = sys.argv[1:] if argv is None else argv
    input_file = args[0] if len(args) >= 1 else DEFAULT_INPUT_FILE
    output_file = args[1] if len(args) >= 2 else DEFAULT_OUTPUT_FILE

    try:
        lines = read_transactions(input_file)
    except FileNotFoundError:
        print(f"Error: file '{input_file}' not found. "
              f"Create it with lines like: Deposit,5000")
        return 1
    except OSError as error:
        print(f"Error: could not read '{input_file}' ({error.strerror}).")
        return 1

    results, final_balance = process_transactions(lines)

    if not results:
        print(f"No transactions found in '{input_file}'.")

    print_report(results, final_balance)

    try:
        save_valid_transactions(results, output_file)
        print(f"Valid transactions saved to '{output_file}'.")
    except OSError as error:
        print(f"Error: could not save '{output_file}' ({error.strerror}).")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
