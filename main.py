import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =====================================================
# 1. LOAD DATASET
# =====================================================

FILE_NAME = r"c:\Users\Rajeev\Desktop\MINI PROJECT\college_canteen_dataset_v8.csv"

df = pd.read_csv(FILE_NAME)
df.columns = df.columns.str.strip()

# Find columns even when the dataset uses different names
def find_column(names):
    for name in names:
        for col in df.columns:
            if col.lower().strip() == name.lower():
                return col
    return None

date_col = find_column(["Date", "Order_Date", "Order Date"])
item_col = find_column(["Item", "Food_Item", "Food Item"])
qty_col = find_column(["Quantity", "Qty"])
amount_col = find_column(["Total_Amount", "Total Amount", "Amount"])
price_col = find_column(["Price_per_item", "Actual_Item_Price",
                         "Price Per Item", "Unit_Price"])
price_alt = find_column(["Price"])
rating_col = find_column(["Rating", "Customer_Rating"])
meal_col = find_column(["Meal_Time", "Meal Time", "Time_Slot"])
payment_col = find_column(["Payment_Mode", "Payment Mode"])
student_col = find_column(["Student_ID", "Student ID", "Customer_ID"])
order_col = find_column(["Order_ID", "Order ID"])
time_col = find_column(["Time", "Order_Time"])
day_col = find_column(["DayOfWeek", "Day_Of_Week", "Day of Week"])

if item_col is None:
    raise ValueError("Dataset must contain an Item or Food_Item column.")

df = df.dropna(how="all").copy()

# Create standard columns for analysis
df["Food_Item"] = df[item_col].fillna("Unknown").astype(str)

if qty_col:
    df["Quantity_Analysis"] = pd.to_numeric(
        df[qty_col], errors="coerce"
    ).fillna(0)
else:
    df["Quantity_Analysis"] = 1

# Find or calculate total sales
if amount_col:
    df["Sales_Analysis"] = pd.to_numeric(
        df[amount_col], errors="coerce"
    )
elif price_col:
    unit_price = pd.to_numeric(df[price_col], errors="coerce")
    df["Sales_Analysis"] = unit_price * df["Quantity_Analysis"]
elif price_alt and qty_col:
    unit_price = pd.to_numeric(df[price_alt], errors="coerce")
    df["Sales_Analysis"] = unit_price * df["Quantity_Analysis"]
elif price_alt:
    df["Sales_Analysis"] = pd.to_numeric(
        df[price_alt], errors="coerce"
    )
else:
    df["Sales_Analysis"] = 0

df["Sales_Analysis"] = df["Sales_Analysis"].fillna(0)

# Prepare rating data
if rating_col:
    df["Rating_Analysis"] = pd.to_numeric(
        df[rating_col], errors="coerce"
    )
else:
    df["Rating_Analysis"] = np.nan

# Prepare date data
if date_col:
    df["Date_Analysis"] = pd.to_datetime(
        df[date_col], errors="coerce", dayfirst=True
    )
else:
    df["Date_Analysis"] = pd.NaT

# Prepare meal/time categories
if meal_col:
    df["Meal_Analysis"] = df[meal_col].fillna("Unknown").astype(str)
elif time_col:
    df["Meal_Analysis"] = df[time_col].fillna("Unknown").astype(str)
else:
    df["Meal_Analysis"] = "Not Available"

# =====================================================
# 2. ANALYTICS
# =====================================================

def total_sales():
    return df["Sales_Analysis"].sum()

def total_orders():
    if order_col:
        return df[order_col].nunique()
    return len(df)

def total_quantity():
    return df["Quantity_Analysis"].sum()

def average_rating():
    ratings = df["Rating_Analysis"].dropna()
    return ratings.mean() if not ratings.empty else None

def unique_customers():
    if student_col:
        return df[student_col].nunique()
    return None

def top_item():
    result = df.groupby("Food_Item")["Quantity_Analysis"].sum()
    return result.idxmax() if not result.empty else "N/A"

def top_revenue_item():
    result = df.groupby("Food_Item")["Sales_Analysis"].sum()
    return result.idxmax() if not result.empty else "N/A"

def average_order_value():
    count = total_orders()
    return total_sales() / count if count else 0

# =====================================================
# 3. MAIN WINDOW
# =====================================================

root = tk.Tk()
root.title("Smart Canteen Analytics System")
root.geometry("1250x780")
root.minsize(950, 600)
root.configure(bg="#F2F5FA")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
style.configure(
    "Treeview.Heading",
    background="#24476B",
    foreground="white",
    font=("Segoe UI", 9, "bold")
)

# Header
header = tk.Frame(root, bg="#17365D", height=85)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header, text="SMART CANTEEN ANALYTICS",
    font=("Segoe UI", 22, "bold"),
    bg="#17365D", fg="white"
).pack(anchor="w", padx=22, pady=(12, 0))

tk.Label(
    header, text="Food demand • Customer satisfaction • Business insights",
    font=("Segoe UI", 10),
    bg="#17365D", fg="#DCE8F5"
).pack(anchor="w", padx=25)

# Main layout
sidebar = tk.Frame(root, bg="#202D3D", width=215)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar, text="ANALYTICS MENU",
    font=("Segoe UI", 10, "bold"),
    bg="#202D3D", fg="#B9C7D6"
).pack(anchor="w", padx=17, pady=(22, 12))

content = tk.Frame(root, bg="#F2F5FA")
content.pack(side="left", fill="both", expand=True)

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

def menu_button(text, command):
    tk.Button(
        sidebar, text=text, command=command,
        anchor="w", padx=15, pady=11,
        bg="#202D3D", fg="white",
        activebackground="#315B84",
        activeforeground="white",
        relief="flat", bd=0,
        font=("Segoe UI", 10), cursor="hand2"
    ).pack(fill="x", padx=6, pady=2)

def heading(title, subtitle):
    tk.Label(
        content, text=title,
        font=("Segoe UI", 21, "bold"),
        bg="#F2F5FA", fg="#172B4D"
    ).pack(anchor="w", padx=22, pady=(18, 2))

    tk.Label(
        content, text=subtitle,
        font=("Segoe UI", 10),
        bg="#F2F5FA", fg="#667085"
    ).pack(anchor="w", padx=24, pady=(0, 10))

# =====================================================
# 4. DASHBOARD CARDS
# =====================================================

def create_card(parent, title, value, row, col):
    card = tk.Frame(
        parent, bg="white",
        highlightbackground="#DCE3EC",
        highlightthickness=1
    )
    card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    tk.Label(
        card, text=title,
        font=("Segoe UI", 9, "bold"),
        bg="white", fg="#667085"
    ).pack(anchor="w", padx=12, pady=(12, 4))

    tk.Label(
        card, text=value,
        font=("Segoe UI", 17, "bold"),
        bg="white", fg="#17365D",
        wraplength=190
    ).pack(anchor="w", padx=12, pady=(0, 12))

# =====================================================
# 5. DASHBOARD
# =====================================================

def show_dashboard():
    clear_content()
    heading("Dashboard", "A complete overview of canteen performance")

    cards = tk.Frame(content, bg="#F2F5FA")
    cards.pack(fill="x", padx=14, pady=5)

    for col in range(3):
        cards.columnconfigure(col, weight=1)

    rating = average_rating()
    customers = unique_customers()

    metrics = [
        ("TOTAL REVENUE", f"₹{total_sales():,.2f}"),
        ("TOTAL ORDERS", f"{total_orders():,}"),
        ("UNITS SOLD", f"{total_quantity():,.0f}"),
        ("AVERAGE RATING",
         f"{rating:.2f} / 5" if rating is not None else "Not available"),
        ("UNIQUE CUSTOMERS",
         f"{customers:,}" if customers is not None else "Not available"),
        ("AVG. ORDER VALUE", f"₹{average_order_value():,.2f}")
    ]

    for i, (title, value) in enumerate(metrics):
        create_card(cards, title, value, i // 3, i % 3)

    panel = tk.Frame(
        content, bg="white",
        highlightbackground="#DCE3EC",
        highlightthickness=1
    )
    panel.pack(fill="both", expand=True, padx=20, pady=12)

    tk.Label(
        panel, text="Canteen Insights",
        font=("Segoe UI", 15, "bold"),
        bg="white", fg="#17365D"
    ).pack(anchor="w", padx=18, pady=(14, 8))

    tk.Label(
        panel,
        text=f"Most demanded food: {top_item()}",
        font=("Segoe UI", 11, "bold"),
        bg="white", fg="#2563A6"
    ).pack(anchor="w", padx=20, pady=5)

    tk.Label(
        panel,
        text=f"Highest revenue item: {top_revenue_item()}",
        font=("Segoe UI", 10),
        bg="white", fg="#344054"
    ).pack(anchor="w", padx=20, pady=5)

    popular = (
        df.groupby("Food_Item")["Quantity_Analysis"]
        .sum().sort_values(ascending=False).head(5)
    )

    tk.Label(
        panel, text="Top 5 food items by quantity",
        font=("Segoe UI", 11, "bold"),
        bg="white", fg="#344054"
    ).pack(anchor="w", padx=20, pady=(12, 5))

    for item, quantity in popular.items():
        tk.Label(
            panel, text=f"• {item}: {quantity:,.0f} units",
            font=("Segoe UI", 10),
            bg="white", fg="#475467"
        ).pack(anchor="w", padx=25, pady=2)

    if rating is None:
        note = "Customer rating information is not available in this dataset."
    else:
        note = f"Average customer rating: {rating:.2f} out of 5"

    tk.Label(
        panel, text=note,
        font=("Segoe UI", 10),
        bg="white", fg="#667085"
    ).pack(anchor="w", padx=20, pady=(10, 12))

# =====================================================
# 6. DATASET EXPLORER
# =====================================================

def show_dataset():
    clear_content()
    heading("Dataset Explorer", "Search and inspect canteen records")

    search_var = tk.StringVar()

    search_frame = tk.Frame(content, bg="#F2F5FA")
    search_frame.pack(fill="x", padx=20, pady=8)

    tk.Label(
        search_frame, text="Search:",
        bg="#F2F5FA", font=("Segoe UI", 10, "bold")
    ).pack(side="left")

    ttk.Entry(
        search_frame, textvariable=search_var, width=35
    ).pack(side="left", padx=10)

    table_frame = tk.Frame(content, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))

    columns = list(df.columns)
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    vertical = ttk.Scrollbar(
        table_frame, orient="vertical", command=tree.yview
    )
    horizontal = ttk.Scrollbar(
        table_frame, orient="horizontal", command=tree.xview
    )

    tree.configure(yscrollcommand=vertical.set,
                   xscrollcommand=horizontal.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")

    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    def populate(data):
        tree.delete(*tree.get_children())

        for row in data.itertuples(index=False, name=None):
            values = []
            for value in row:
                if pd.isna(value):
                    values.append("")
                elif isinstance(value, (pd.Timestamp,)):
                    values.append(value.strftime("%d-%m-%Y"))
                else:
                    values.append(str(value))
            tree.insert("", "end", values=values)

    def search(*args):
        term = search_var.get().strip().lower()

        if not term:
            populate(df)
            return

        matches = df.astype(str).apply(
            lambda col: col.str.lower().str.contains(
                term, regex=False, na=False
            )
        ).any(axis=1)

        populate(df[matches])

    populate(df)
    search_var.trace_add("write", search)

# =====================================================
# 7. CHART WINDOW
# =====================================================

def chart_page(title, subtitle="Explore your canteen data visually"):
    clear_content()
    heading(title, subtitle)

    frame = tk.Frame(content, bg="white")
    frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))
    return frame

def display_chart(fig, frame):
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)

def show_message(frame, text):
    tk.Label(
        frame, text=text, font=("Segoe UI", 12),
        bg="white", fg="#667085",
        wraplength=650
    ).pack(expand=True, padx=20, pady=20)

# =====================================================
# 8. FOOD DEMAND CHART
# =====================================================

def show_demand_chart():
    frame = chart_page(
        "Food Demand Analysis",
        "Find which food items are ordered most often"
    )

    data = (
        df.groupby("Food_Item")["Quantity_Analysis"]
        .sum().sort_values(ascending=False).head(10).sort_values()
    )

    if data.empty:
        show_message(frame, "No food demand data is available.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(data.index, data.values)
    ax.set_title("Top 10 Food Items by Quantity")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("Food Item")
    ax.grid(axis="x", alpha=0.25)
    display_chart(fig, frame)

# =====================================================
# 9. REVENUE CHART
# =====================================================

def show_revenue_chart():
    frame = chart_page(
        "Revenue Analysis",
        "Compare revenue generated by food items"
    )

    data = (
        df.groupby("Food_Item")["Sales_Analysis"]
        .sum().sort_values(ascending=False).head(10).sort_values()
    )

    if data.empty:
        show_message(frame, "No revenue data is available.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(data.index, data.values)
    ax.set_title("Top 10 Food Items by Revenue")
    ax.set_xlabel("Revenue (₹)")
    ax.set_ylabel("Food Item")
    ax.grid(axis="x", alpha=0.25)
    display_chart(fig, frame)

# =====================================================
# 10. MEAL / TIME SLOT ANALYSIS
# =====================================================

def show_meal_chart():
    frame = chart_page(
        "Ordering Time Analysis",
        "Compare activity across meal times or time slots"
    )

    if meal_col is None and time_col is None:
        show_message(frame, "No meal-time or time column is available.")
        return

    data = df.groupby("Meal_Analysis")["Sales_Analysis"].sum()

    if data.empty:
        show_message(frame, "No time-based data is available.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(data.values, labels=data.index, autopct="%1.1f%%",
           startangle=90)
    ax.set_title("Revenue Distribution by Meal / Time Slot")
    display_chart(fig, frame)

# =====================================================
# 11. DAILY SALES TREND
# =====================================================

def show_daily_chart():
    frame = chart_page(
        "Daily Sales Trend",
        "Observe how revenue changes over time"
    )

    data = (
        df.dropna(subset=["Date_Analysis"])
        .groupby("Date_Analysis")["Sales_Analysis"]
        .sum().sort_index()
    )

    if data.empty:
        show_message(frame, "No valid date information is available.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(data.index, data.values, marker="o", linewidth=2)
    ax.set_title("Daily Revenue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue (₹)")
    ax.grid(alpha=0.25)
    fig.autofmt_xdate()
    display_chart(fig, frame)

# =====================================================
# 12. CUSTOMER SATISFACTION
# =====================================================

def show_rating_chart():
    frame = chart_page(
        "Customer Satisfaction",
        "Explore ratings given to different food items"
    )

    if rating_col is None or df["Rating_Analysis"].dropna().empty:
        show_message(frame, "Customer rating data is not available.")
        return

    data = (
        df.groupby("Food_Item")["Rating_Analysis"]
        .mean().dropna().sort_values(ascending=False).head(10)
        .sort_values()
    )

    if data.empty:
        show_message(frame, "No valid ratings are available.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(data.index, data.values)
    ax.set_title("Highest-Rated Food Items")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Food Item")
    ax.set_xlim(0, 5)
    ax.grid(axis="x", alpha=0.25)
    display_chart(fig, frame)

# =====================================================
# 13. PAYMENT ANALYSIS
# =====================================================

def show_payment_chart():
    frame = chart_page(
        "Payment Preferences",
        "Understand how customers pay for their orders"
    )

    if payment_col is None:
        show_message(frame, "Payment mode data is not available.")
        return

    data = df[payment_col].fillna("Unknown").value_counts()

    if data.empty:
        show_message(frame, "No payment records are available.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(data.values, labels=data.index, autopct="%1.1f%%",
           startangle=90)
    ax.set_title("Orders by Payment Method")
    display_chart(fig, frame)

# =====================================================
# 14. DAY-OF-WEEK ANALYSIS
# =====================================================

def show_weekday_chart():
    frame = chart_page(
        "Day-wise Performance",
        "Compare canteen activity across days of the week"
    )

    if day_col:
        day_values = df[day_col].fillna("Unknown").astype(str)
    elif df["Date_Analysis"].notna().any():
        day_values = df["Date_Analysis"].dt.day_name()
    else:
        show_message(frame, "Day or date information is not available.")
        return

    temp = df.copy()
    temp["Day_Analysis"] = day_values

    data = temp.groupby("Day_Analysis")["Sales_Analysis"].sum()

    if data.empty:
        show_message(frame, "No day-wise sales data is available.")
        return

    # Arrange standard weekdays in calendar order
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]

    ordered = [day for day in weekdays if day in data.index]
    ordered += [day for day in data.index if day not in ordered]
    data = data.reindex(ordered)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(data.index, data.values)
    ax.set_title("Revenue by Day of the Week")
    ax.set_xlabel("Day")
    ax.set_ylabel("Revenue (₹)")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.25)
    display_chart(fig, frame)

# =====================================================
# 15. SIDEBAR MENU
# =====================================================

menu_button("▣  Dashboard", show_dashboard)
menu_button("▤  Dataset Explorer", show_dataset)
menu_button("🍽  Food Demand", show_demand_chart)
menu_button("₹  Revenue Analysis", show_revenue_chart)
menu_button("◉  Meal / Time Analysis", show_meal_chart)
menu_button("↗  Daily Sales Trend", show_daily_chart)
menu_button("★  Customer Satisfaction", show_rating_chart)
menu_button("▤  Payment Preferences", show_payment_chart)
menu_button("▦  Day-wise Analysis", show_weekday_chart)

tk.Button(
    sidebar, text="✕  Exit",
    command=root.destroy,
    anchor="w", padx=15, pady=11,
    bg="#8F2929", fg="white",
    activebackground="#702020",
    activeforeground="white",
    relief="flat", bd=0,
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
).pack(side="bottom", fill="x", padx=8, pady=12)

# =====================================================
# 16. START APPLICATION
# ==================================
show_dashboard()
root.mainloop()