
import random
import xml.etree.ElementTree as ET
def generate_xml(xsd_names, case_id):
    root = ET.Element("Source")
    for name in xsd_names:
        if random.choice([True, False]):
            for i in range(random.randint(1,2)):
                elem = ET.SubElement(root, name)
                elem.text = f"test_{name}_{case_id}_{i}"
    return ET.tostring(root, encoding="utf-8")

if __name__ == "__main__":
    import os
    cases = 5
    with open("../xsd/_extracted_names.txt") as f:
        names = [n.strip() for n in f]
    os.makedirs("../xml/generated_inputs", exist_ok=True)
    for cid in range(cases):
        xml = generate_xml(names, cid)
        with open(f"../xml/generated_inputs/input_{cid}.xml", "wb") as f:
            f.write(xml)
