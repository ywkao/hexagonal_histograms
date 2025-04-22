import pandas as pd
import os

class WaferDataLoader:
    def __init__(self, file_path="./data/input/WaferCellMapTraces.txt"):
        # Load the full dataset once
        self.df = pd.read_csv(file_path, sep=r'\s+', header=0)
        column_names = ["TypeCode", "ROC", "HalfROC", "Seq", "ROCpin", "SiCell",
                       "TrLink", "TrCell", "iu", "iv", "trace", "t"]
        self.df.columns = column_names
        self.type_codes = self.df["TypeCode"].unique()

    def get_data_for_type(self, type_code):
        """Return a DataFrame filtered for a specific type code"""
        if type_code not in self.type_codes:
            raise ValueError(f"Unknown type code: {type_code}")
        return self.df[self.df["TypeCode"] == type_code]

    def get_all_type_codes(self):
        """Return all available type codes"""
        return self.type_codes

    def get_data_as_lines(self, type_code):
        """For backward compatibility - return data as lines of text"""
        filtered_df = self.get_data_for_type(type_code)
        # Convert DataFrame rows back to space-separated strings
        return [' '.join(map(str, row)) for _, row in filtered_df.iterrows()]

    def retrieve_info(self, line):
        info = line.strip().split()
        result = []
        for ele in info:
            if "ML" in ele or "MH" in ele or "CALIB" in ele:
                result.append(str(ele))
            elif "." in ele:
                result.append(float(ele))
            else:
                result.append(int(ele))
        return tuple(result)
