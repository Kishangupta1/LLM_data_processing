import pandas as pd

# Example DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Value to add to all cells in the new row
value = 9

# Adding a new row with the same value in all columns
df.loc[len(df)] = [value] * len(df.columns)

print(df)
