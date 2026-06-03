import os

vars_path = "../sovi-20-questions-demo/.dev.vars"
if os.path.exists(vars_path):
    print("Found .dev.vars")
    with open(vars_path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                v = v.strip()
                if len(v) > 15:
                    v_masked = v[:5] + "..." + v[-4:]
                else:
                    v_masked = v
                print(f"{k} = {v_masked}")
else:
    print(".dev.vars not found")
