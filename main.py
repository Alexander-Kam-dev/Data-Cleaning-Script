import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Sample script that simulates the full project structure for a CSV data cleaner and summarizer

# Step 1: Load CSV file

def load_file(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.tsv'):
            df = pd.read_csv(file_path, sep='\t')
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            raise ValueError("❌ Unsupported file format. Supported: .csv, .xlsx, .tsv, .json")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None



# def load_file(file_path):
#     try:
#         df = pd.read_csv(file_path)
#         return df
#     except Exception as e:
#         print(f"Error loading CSV: {e}")
#         return None

# Step 2: Clean data
def clean_data(df):
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.drop_duplicates()

    # Preserve numeric data for plotting
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype == 'object':
            df_cleaned[col] = df_cleaned[col].fillna("n/a")
        else:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
            # Leave NaN as-is for now to avoid breaking plotting

    return df_cleaned


# def clean_data(df):
#     df_cleaned = df.copy()
#     df_cleaned = df_cleaned.drop_duplicates()

#     for col in df_cleaned.columns:
#         if df_cleaned[col].dtype == 'object':
#             df_cleaned[col] = df_cleaned[col].fillna("n/a")
#         else:
#             # Keep column as numeric and fill missing with column mean
#             df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
#             df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mean())

#     return df_cleaned




# def clean_data(df):
#     df_cleaned = df.copy()
#     df_cleaned = df_cleaned.drop_duplicates()
#     df_cleaned = df_cleaned.fillna("n/a")
#     return df_cleaned



# Step 3: Generate summary
def generate_summary(df, output_path):
    with open(os.path.join(output_path, "summary_report.txt"), "w") as f:
        f.write("Summary Report\n")
        f.write("=====================\n\n")
        f.write(f"Total rows: {df.shape[0]}\n")
        f.write(f"Total columns: {df.shape[1]}\n\n")
        f.write("Missing Values Per Column:\n")
        f.write(df.isnull().sum().to_string())
        f.write("\n\nNumeric Column Statistics:\n")
        f.write(df.describe().to_string())

# Step 4: Generate visualization
def generate_visual(df, output_path):
    numeric_cols = df.select_dtypes(include='number').columns
    if not numeric_cols.empty:
        df[numeric_cols[0]].plot(kind='hist', bins=10, title=f"{numeric_cols[0]} Distribution")
        plt.xlabel(numeric_cols[0])
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, "visual_summary.png"))
        plt.close()

# Step 5: Save cleaned data
def save_cleaned_data(df, output_path):
    df.to_csv(os.path.join(output_path, "cleaned_data.csv"), index=False)

# Main driver
def main():
    # Use a sample test file (user can replace this with their own path)
    sample_file = "raw_data.tsv"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    df = load_file(sample_file)

    if df is not None:
        df_cleaned = clean_data(df)
        
        save_cleaned_data(df_cleaned, output_dir)
        generate_summary(df_cleaned, output_dir)
        generate_visual(df_cleaned, output_dir)

        # Final cleanup: convert any remaining NaN to "n/a" before saving final output
        df_cleaned = df_cleaned.fillna("n/a")
        save_cleaned_data(df_cleaned, output_dir)

        print("✅ Project completed. Check the 'output/' folder for results.")


    # if df is not None:
    #     df_cleaned = clean_data(df)
    #     save_cleaned_data(df_cleaned, output_dir)
    #     generate_summary(df_cleaned, output_dir)
    #     generate_visual(df_cleaned, output_dir)

    #     print("✅ Project completed. Check the 'output/' folder for results.")

main()
