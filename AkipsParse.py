import csv
import re

# Function to check if the interface is valid (Gi1/0/XX)
def is_valid_interface(interface):
    return bool(re.match(r"^Gi1/0/\d+$", interface))

# Function to parse the CSV and generate counts
def parse_csv(input_file, output_file):
    switch_data = {}

    # Read the input CSV file
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if len(row) < 5:
                continue  # Skip malformed rows

            switch_name, interface, _, status, _, *_ = row

            if not is_valid_interface(interface):
                continue  # Ignore invalid interfaces

            if switch_name not in switch_data:
                switch_data[switch_name] = {'total': 0, 'used': 0, 'free': 0}

            switch_data[switch_name]['total'] += 1
            if status == 'free':
                switch_data[switch_name]['free'] += 1
            elif status == 'used':
                switch_data[switch_name]['used'] += 1

    # Write the results to the output CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Switch Name', 'Total Ports', 'Used Ports', 'Free Ports'])
        for switch_name, counts in switch_data.items():
            writer.writerow([switch_name, counts['total'], counts['used'], counts['free']])

# Main function
if __name__ == "__main__":
    input_file = "report.20241206.1200.csv"  # Replace with the path to your input CSV file
    output_file = "switch_summary.csv"  # Replace with the desired output CSV file name

    parse_csv(input_file, output_file)
    print(f"Summary written to {output_file}")
