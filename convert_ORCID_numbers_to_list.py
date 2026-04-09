# save_orcids.py
import pandas as pd
from pathlib import Path


def extract_orcids_from_excel(file_path, column_position=2):
    """Extract ORCIDs from Excel column C"""
    if not Path(file_path).exists():
        print(f"Error: File not found")
        return []

    df = pd.read_excel(file_path, header=None, engine="openpyxl")
    orcids = df[column_position].dropna().astype(str).tolist()

    # Clean up
    cleaned_orcids = []
    for orcid in orcids:
        if orcid and orcid.strip():
            if "orcid.org/" in orcid:
                orcid = orcid.split("orcid.org/")[-1]
            cleaned_orcids.append(orcid.strip())

    return cleaned_orcids


# Extract ORCIDs
file_path = "C:/Users/Simon/MAIN_WORK_FOLDER/coding/litreview_telegram_bot/litreview_bot/ORCIDs.xlsx"
orcids = extract_orcids_from_excel(file_path)

# Save as a Python file
with open("orcids_list.py", "w") as f:
    f.write("# Auto-generated ORCID list\n")
    f.write(f"ORCIDS = {orcids}\n")
    f.write(f"\n# Total count: {len(orcids)} ORCIDs\n")

print(f"Saved {len(orcids)} ORCIDs to orcids_list.py")
