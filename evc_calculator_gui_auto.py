
import tkinter as tk
from tkinter import messagebox
import requests

def fetch_evc_price():
    try:
        # Placeholder API - replace with real one if available
        # For now, let's simulate price for demo purposes
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=evolvcoin&vs_currencies=usd")
        data = response.json()
        return float(data["evolvcoin"]["usd"])
    except:
        return None

def calculate():
    try:
        usd = float(entry_usd.get())
        price_now = fetch_evc_price()
        if price_now is None:
            raise ValueError("Could not fetch EVC price.")
        entry_price_now.delete(0, tk.END)
        entry_price_now.insert(0, f"{price_now:.4f}")

        price_future = float(entry_price_future.get())
        months = int(entry_months.get())

        tokens = usd / price_now
        future_value = tokens * price_future
        profit = future_value - usd

        result = f"""
Tokens acquired:      {tokens:,.2f} EVC
Future value:         ${future_value:,.2f}
Expected profit/loss: ${profit:,.2f}
Holding period:       {months} months
"""

        if profit > 0:
            result += "\n🚀 Positive projection. Potential profit ahead."
        elif profit == 0:
            result += "\n⏸️ Break-even scenario. Reassess projections."
        else:
            result += "\n⚠️ Potential loss. Stay informed on EvolvCoin updates."

        text_output.config(state="normal")
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, result)
        text_output.config(state="disabled")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("EvolvCoin Investment Calculator")
root.geometry("460x420")
root.resizable(False, False)

# Input fields
tk.Label(root, text="💵 USD to invest:").pack(pady=(10, 0))
entry_usd = tk.Entry(root, width=30)
entry_usd.pack()

tk.Label(root, text="📌 Current EVC price (auto-fetched):").pack(pady=(10, 0))
entry_price_now = tk.Entry(root, width=30)
entry_price_now.pack()

tk.Label(root, text="🔮 Future EVC price (USD):").pack(pady=(10, 0))
entry_price_future = tk.Entry(root, width=30)
entry_price_future.pack()

tk.Label(root, text="📆 Holding period (months):").pack(pady=(10, 0))
entry_months = tk.Entry(root, width=30)
entry_months.pack()

# Calculate button
tk.Button(root, text="Calculate", command=calculate, bg="#2e86de", fg="white", padx=10, pady=5).pack(pady=15)

# Output box
text_output = tk.Text(root, height=10, width=55, state="disabled", wrap="word", bg="#f0f0f0")
text_output.pack(padx=10, pady=5)

# Run the app
root.mainloop()
