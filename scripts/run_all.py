
import subprocess
steps = [
    ["python", "extract_schema.py"],
    ["python", "generate_mini_xsd.py"],
    ["python", "generate_xml.py"],
    ["python", "transform.py"],
    ["python", "transform.py", "--candidate"],
    ["python", "compare.py"]
]
for s in steps:
    print("Running:", " ".join(s))
    subprocess.run(s, cwd=".")
