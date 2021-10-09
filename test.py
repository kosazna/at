import subprocess

a = subprocess.check_output(["python", "D:/.temp/.dev/.aztool/at/io.py"])

print(type(eval(a)))