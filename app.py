from flask import Flask, render_template, request, redirect, jsonify
import os

app = Flask(__name__)

COMMIT_ID = os.environ.get("RENDER_GIT_COMMIT", "local-development")

expenses = []


@app.route("/")
def home():
    total = sum(expense["amount"] for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        commit_id=COMMIT_ID
    )


@app.route("/add", methods=["POST"])
def add_expense():
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "").strip()
    amount = request.form.get("amount", "").strip()

    if not description:
        return "Description is required.", 400

    if not amount:
        return "Amount is required.", 400

    try:
        amount = float(amount)
    except ValueError:
        return "Amount must be a valid number.", 400

    if amount <= 0:
        return "Amount must be greater than zero.", 400

    expenses.append({
        "description": description,
        "category": category,
        "amount": amount
    })

    return redirect("/")


@app.route("/api/expenses")
def api_expenses():
    return jsonify(expenses)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
