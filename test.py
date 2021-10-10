import subprocess

a = subprocess.check_output("D:/.temp/.dev/.aztool/atauth/dist/auth.exe --appname atcrawl")

print(eval(a))