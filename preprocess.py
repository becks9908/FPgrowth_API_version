import re
from collections import Counter

class Preprocess:
    def __init__(self, file_name, min_times):
        self.file_name = file_name
        self.test_status_dict = {}
        self.min_times = min_times
        
    def process_file(self):
        test_status_pattern = r'\d+\s+\d+\s+(.*?)\s+Digital_Contact\s+(passed|failed)'
        
        self.test_name_counts = Counter()

        with open(self.file_name, 'r',encoding='utf-8', errors='ignore') as log_file:
            lines = log_file.readlines()

        for line in lines:
            match = re.search(test_status_pattern, line)
            if match:
                current_test_name, status = match.groups()
                self.test_name_counts[current_test_name] += 1
                if current_test_name not in self.test_status_dict:
                    self.test_status_dict[current_test_name] = {'passed': 0, 'failed': 0}
                self.test_status_dict[current_test_name][status] += 1

        failure_rates = {}
        for test_name, status_counts in self.test_status_dict.items():
            total_count = self.test_name_counts.get(test_name, 0)
            if total_count > 0 and status_counts['failed']>0:
                failure_rate = status_counts['failed'] / total_count
                failure_rates[test_name] = round(failure_rate * 100, 2)

        return failure_rates
