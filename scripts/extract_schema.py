
import re
from lxml import etree

def extract_root_element(xslt_path):
    """Extract the root element name from template match patterns"""
    tree = etree.parse(xslt_path)
    ns = {"x": "http://www.w3.org/1999/XSL/Transform"}
    # Look for template match patterns
    matches = tree.xpath("//x:template[@match]/@match", namespaces=ns)
    for match in matches:
        # Simple extraction: first word that's not "/" or "*"
        if match and match not in ["/", "*", "/"]:
            # Remove leading slashes and special characters
            clean_match = match.lstrip("/").split("/")[0].split("[")[0].strip()
            if clean_match and clean_match != "*" and not clean_match.startswith("@"):
                return clean_match
    return "Source"  # default fallback

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

    # Extract root element
    root_elem = extract_root_element(xslt)

    # Extract element names
    elems = extract_xpaths(xslt)

    # Save both to files
    with open("../xsd/_extracted_names.txt", "w") as f:
        f.write("\n".join(elems))

    with open("../xsd/_root_element.txt", "w") as f:
        f.write(root_elem)
