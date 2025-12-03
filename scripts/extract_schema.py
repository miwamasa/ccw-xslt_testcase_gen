
import re
from lxml import etree
def extract_xpaths(xslt_path):
    tree = etree.parse(xslt_path)
    ns = {"x": "http://www.w3.org/1999/XSL/Transform"}
    selects = tree.xpath("//x:*[@select]/@select", namespaces=ns)
    matches = []
    for sel in selects:
        tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_\-]*", sel)
        matches.extend(tokens)
    return sorted(set(matches))
if __name__ == "__main__":
    xslt = "../xslt/T0_correct.xslt"
    elems = extract_xpaths(xslt)
    with open("../xsd/_extracted_names.txt", "w") as f:
        f.write("\n".join(elems))
