
def generate_xsd(element_names, root="Root"):
    xsd_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="{root}">
    <xs:complexType>
      <xs:sequence>
"""
    xsd_body = ""
    for e in element_names:
        xsd_body += f'        <xs:element name="{e}" minOccurs="0" maxOccurs="2" type="xs:string"/>\n'
    xsd_footer = """      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""
    return xsd_header + xsd_body + xsd_footer

if __name__ == "__main__":
    with open("../xsd/_extracted_names.txt") as f:
        names = [n.strip() for n in f.readlines()]
    xsd = generate_xsd(names, root="Source")
    with open("../xsd/source_mini.xsd", "w") as f:
        f.write(xsd)
