import pandas as pd

# Load dataset
df = pd.read_csv("cleaned_ddos.csv")

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Convert labels to binary: BENIGN -> 0, attack -> 1
df['Label'] = df['Label'].apply(lambda x: 0 if x.strip().upper() == 'BENIGN' else 1)

# Move label column to front
cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index('Label')))
df = df[cols]

# Save final version
df.to_csv("binary_cleaned_ddos.csv", index=False)
print("✅ binary_cleaned_ddos.csv saved and ready for SageMaker")

