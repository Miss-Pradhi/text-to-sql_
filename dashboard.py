import pandas as pd
import matplotlib.pyplot as plt

def show_dashboard(data):
    if not data:
        return None
    try:
        if len(data[0]) == 2:
            df = pd.DataFrame(data, columns=["Category", "Value"])
        else:
            return None
        fig, ax = plt.subplots()
        df.plot(kind="bar", x="Category", y="Value", ax=ax)
        return df, fig
    except Exception as e:
        print("Dashboard Error:", e)
        return None