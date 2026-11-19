import re

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

with open("/tmp/batch1_fin_dump.txt") as f:
    text = f.read()

# 1. 3738.HK
print("=================== 3738.HK ===================")
part = text.split("3738.HK Income")[1].split("=== 6119.HK")[0]
lines = [clean(l) for l in part.split("\n") if l.strip()]
print("\n".join(lines[:60]))

# 2. 6119.HK
print("\n=================== 6119.HK ===================")
part = text.split("6119.HK Income")[1].split("=== 8447.HK")[0]
lines = [clean(l) for l in part.split("\n") if l.strip()]
print("\n".join(lines[:60]))

# 3. 8447.HK
print("\n=================== 8447.HK ===================")
part = text.split("8447.HK Income")[1].split("=== 8516.HK")[0]
lines = [clean(l) for l in part.split("\n") if l.strip()]
print("\n".join(lines[:60]))

# 4. 8516.HK
print("\n=================== 8516.HK ===================")
part = text.split("8516.HK Income")[1].split("=== 8645.HK")[0]
lines = [clean(l) for l in part.split("\n") if l.strip()]
print("\n".join(lines[:60]))

# 5. 8645.HK
print("\n=================== 8645.HK ===================")
part = text.split("8645.HK Income")[1].split("=== 9988.HK")[0]
lines = [clean(l) for l in part.split("\n") if l.strip()]
print("\n".join(lines[:60]))

# 6. 9988.HK
print("\n=================== 9988.HK ===================")
part = text.split("9988.HK Income")[1]
lines = [clean(l) for l in part.split("\n") if l.strip()]
print("\n".join(lines[:60]))

