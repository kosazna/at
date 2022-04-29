import random

random.seed(1994)
num1 = input("Give number:\n")
num2 = str(random.randint(1000, 9999))

lnum1 = list(num1)
lnum2 = list(num2)
snum1 = set(num1)
snum2 = set(num2)
occurence_cnt = 0
digit_cnt = 0

for idx, i in enumerate(snum1):
    if i in snum2:
        occurence_cnt += 1

for idx, i in enumerate(lnum1):
    if lnum1[idx] == lnum2[idx]:
        digit_cnt += 1

print(f"\n  User: {num1}")
print(f"Random: {num2}")
print("-" * 12)
print(f"+ : {digit_cnt}")
print(f"? : {occurence_cnt}")