import csv

def parse_sb_publication_pmc(csv_file_path):
    publications = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            publications.append(row)
    return publications

# Example usage:
if __name__ == "__main__":
    csv_path = "SB_Publication_PMC.csv"
    data = parse_sb_publication_pmc(csv_path)
    print(f"Parsed {len(data)} records.")
    # Print first record as a sample
    if data:
        print(data[0]["Link"])




