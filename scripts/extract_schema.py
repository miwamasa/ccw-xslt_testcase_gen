
import re
from lxml import etree

def extract_root_element(xslt_path):
    """Extract the source root element name from template match patterns"""
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

def extract_target_root_element(xslt_path):
    """Extract the target root element name from literal result elements"""
    tree = etree.parse(xslt_path)
    ns = {"x": "http://www.w3.org/1999/XSL/Transform"}

    # Find all templates
    templates = tree.xpath("//x:template", namespaces=ns)

    for template in templates:
        # Look for the first non-XSLT element (literal result element)
        for child in template:
            # Check if tag is a string
            if isinstance(child.tag, str):
                # Skip XSLT elements
                if child.tag.startswith("{http://www.w3.org/1999/XSL/Transform}"):
                    continue
                # Found a literal result element
                local_name = etree.QName(child).localname
                if local_name:
                    return local_name

    # Fallback: look for xsl:element at root level
    elements = tree.xpath("//x:template/x:element[@name]/@name", namespaces=ns)
    if elements:
        return elements[0]

    return "Target"  # default fallback

def extract_xpaths(xslt_path):
    """Extract source element names from XPath expressions"""
    tree = etree.parse(xslt_path)
    ns = {"x": "http://www.w3.org/1999/XSL/Transform"}
    selects = tree.xpath("//x:*[@select]/@select", namespaces=ns)
    matches = []
    for sel in selects:
        tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_\-]*", sel)
        matches.extend(tokens)
    return sorted(set(matches))

def extract_output_elements(xslt_path):
    """Extract target element names from output (literal result elements and xsl:element)"""
    tree = etree.parse(xslt_path)
    ns = {"x": "http://www.w3.org/1999/XSL/Transform"}

    elements = set()

    # Extract literal result elements (non-XSLT namespace elements)
    for elem in tree.iter():
        # Check if tag is a string (not a function or comment)
        if isinstance(elem.tag, str):
            if not elem.tag.startswith("{http://www.w3.org/1999/XSL/Transform}"):
                local_name = etree.QName(elem).localname
                if local_name:
                    elements.add(local_name)

    # Extract xsl:element/@name
    xsl_elements = tree.xpath("//x:element/@name", namespaces=ns)
    elements.update(xsl_elements)

    # Extract xsl:attribute/@name (attributes are also part of the schema)
    xsl_attrs = tree.xpath("//x:attribute/@name", namespaces=ns)
    elements.update(xsl_attrs)

    return sorted(elements)

if __name__ == "__main__":
    xslt = "../xslt/T0_correct.xslt"

    # Extract source root element
    source_root_elem = extract_root_element(xslt)

    # Extract target root element
    target_root_elem = extract_target_root_element(xslt)

    # Extract source element names (from XPath)
    source_elems = extract_xpaths(xslt)

    # Extract target element names (from output)
    target_elems = extract_output_elements(xslt)

    # Save source information
    with open("../xsd/_extracted_names.txt", "w") as f:
        f.write("\n".join(source_elems))

    with open("../xsd/_root_element.txt", "w") as f:
        f.write(source_root_elem)

    # Save target information
    with open("../xsd/_target_names.txt", "w") as f:
        f.write("\n".join(target_elems))

    with open("../xsd/_target_root_element.txt", "w") as f:
        f.write(target_root_elem)
