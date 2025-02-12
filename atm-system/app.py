from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for accounts
accounts = {"12345": 1000.0}  # Sample account with initial balance

@app.route("/accounts/<account_number>/balance", methods=["GET"])
def get_balance(account_number):
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"accountNumber": account_number, "balance": accounts[account_number]})

@app.route("/accounts/<account_number>/withdraw", methods=["POST"])
def withdraw(account_number):
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    
    amount = request.args.get("amount", type=float)
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400
    
    if amount > accounts[account_number]:
        return jsonify({"error": "Insufficient funds"}), 400
    
    accounts[account_number] -= amount
    return jsonify({"message": "Withdrawal successful", "new_balance": accounts[account_number]})

@app.route("/accounts/<account_number>/deposit", methods=["POST"])
def deposit(account_number):
    amount = request.args.get("amount", type=float)
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400
    
    accounts[account_number] = accounts.get(account_number, 0.0) + amount
    return jsonify({"message": "Deposit successful", "new_balance": accounts[account_number]})

if __name__ == "__main__":
    app.run(debug=True)