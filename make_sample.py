import pandas as pd

SOURCE = "data/2019-Oct.csv"
OUTPUT = "data/sample.csv"

chunks = []
for chunk in pd.read_csv(SOURCE, chunksize=500_000):
    # keep every user whose ID ends in 0 → ~10% of users, full journeys intact
    chunks.append(chunk[chunk["user_id"] % 10 == 0])

sample = pd.concat(chunks)
sample.to_csv(OUTPUT, index=False)

print(f"Rows: {len(sample):,}")
print(f"Users: {sample['user_id'].nunique():,}")
print(sample["event_type"].value_counts())
