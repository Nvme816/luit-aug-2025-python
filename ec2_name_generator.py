import random
import string

ALLOWED = {"marketing", "accounting", "finops"}
count = int(input("How many ec2 instance names do you want? "))
dept_raw = input("Department (Marketing/Accounting/FinOps): ")

dept_key = dept_raw.strip().lower()
if dept_key not in ALLOWED: 
    print("Sorry, this generator is only for Marketing, Accounting, and FinOps. ")
else:
    pretty = {"marketing": "Marketing", "accounting": "Accounting", "finops": "FinOps"} [dept_key]
    alphabet = string.ascii_uppercase + string.digits
    names = set()
while len(names) < count:
    token = ''.join(random.choices(alphabet, k=4))
    names.add(f"{pretty}-{token}")
for name in sorted(names):
    print(name)


