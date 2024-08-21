import pandas as pd
import numpy as np

# Example DataFrame
df = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, np.nan, 4]
})

# Flatten the DataFrame to a single Series
flattened = df.stack()

# Reset the index to create a new DataFrame without NaN values
df_cleaned = flattened.reset_index(drop=True)

# If you want to reshape back into a 2D DataFrame with the dropped NaNs removed:
reshaped_df = pd.DataFrame(df_cleaned.values.reshape(-1, len(df.columns)))

print("Flattened and NaNs removed:")
print(df_cleaned)

print("\nReshaped DataFrame:")
print(reshaped_df)
