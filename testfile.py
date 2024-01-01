import sys
print(sys.path)

import os

with open('/home/asafz/tasks/output_file.txt', 'w') as f:
    for key, value in os.environ.items():
        f.write(f'{key}={value}\n')

with open('/home/asafz/tasks/output_file123.txt', 'w') as f:
    for path in sys.path:
        f.write(f"{path}\n")