import pandas as pd

# Example DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
df = pd.DataFrame(data)

# Define a function to apply to the element
def multiply_by_2(x):
    return x * 2

# Apply the function to the element in the 3rd column (index 2) of the 1st row (index 0)
df.iloc[0, 1:] = multiply_by_2(df.iloc[0, 1:])

print(df)
