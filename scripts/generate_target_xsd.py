
def generate_xsd(element_names, root="Root"):
    xsd_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="{root}">
    <xs:complexType>
      <xs:sequence>
"""
    xsd_body = ""
    for e in element_names:
        xsd_body += f'        <xs:element name="{e}" minOccurs="0" maxOccurs="unbounded" type="xs:string"/>\n'
    xsd_footer = """      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""
    return xsd_header + xsd_body + xsd_footer

if __name__ == "__main__":
    # Read extracted target element names
    with open("../xsd/_target_names.txt") as f:
        names = [n.strip() for n in f.readlines() if n.strip()]

    # Read target root element name
    try:
        with open("../xsd/_target_root_element.txt") as f:
            root_name = f.read().strip()
    except FileNotFoundError:
        root_name = "Target"  # default fallback

    # Remove root element from the list of child elements
    if root_name in names:
        names.remove(root_name)

    xsd = generate_xsd(names, root=root_name)
    with open("../xsd/target_mini.xsd", "w") as f:
        f.write(xsd)
