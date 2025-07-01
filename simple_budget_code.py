from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

transactions = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Budget Tracker</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 30px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 30px;
        }
        input[type="text"], input[type="number"], select {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        button {
            padding: 10px;
            background-color: #5cb85c;
            border: none;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #4cae4c;
        }
        .summary {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .summary div {
            font-size: 18px;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        canvas {
            max-width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💸 Budget Tracker</h1>

        <form method="POST" action="/">
            <input type="text" name="description" placeholder="Description" required>
            <input type="number" step="0.01" name="amount" placeholder="Amount" required>
            <select name="type">
                <option value="income">Income</option>
                <option value="expense">Expense</option>
            </select>
            <button type="submit">Add Transaction</button>
        </form>

        <div class="summary">
            <div>Total Income: ${{ income }}</div>
            <div>Total Expenses: ${{ expenses }}</div>
            <div>Balance: ${{ balance }}</div>
        </div>

        <canvas id="budgetChart"></canvas>

        <table>
            <thead>
                <tr><th>Description</th><th>Amount</th><th>Type</th></tr>
            </thead>
            <tbody>
                {% for t in transactions %}
                    <tr>
                        <td>{{ t['description'] }}</td>
                        <td>${{ t['amount'] }}</td>
                        <td>{{ t['type'].capitalize() }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <script>
        const ctx = document.getElementById('budgetChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Income', 'Expenses'],
                datasets: [{
                    label: 'Budget Overview',
                    data: [{{ income }}, {{ expenses }}],
                    backgroundColor: ['#28a745', '#dc3545']
                }]
            }
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        t_type = request.form["type"]

        transactions.append({
            "description": description,
            "amount": amount,
            "type": t_type
        })
        return redirect("/")

    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = income - expenses

    return render_template_string(
        HTML_TEMPLATE,
        transactions=transactions,
        income=round(income, 2),
        expenses=round(expenses, 2),
        balance=round(balance, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)
