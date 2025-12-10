#!/usr/bin/env python3
"""
Simple XSLT Generator - Simulates an external XSLT generation service

This script reads source and target XSD files and generates an XSLT
transformation based on simple heuristic rules.
"""

from lxml import etree
import re

def parse_xsd(xsd_path):
    """Parse XSD and extract element information"""
    tree = etree.parse(xsd_path)
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}

    # Get root element name
    root_elem = tree.xpath("//xs:element[@name]", namespaces=ns)[0]
    root_name = root_elem.get("name")

    # Get child elements
    elements = tree.xpath("//xs:element[@name]/xs:complexType//xs:element[@name]/@name", namespaces=ns)

    return root_name, list(elements)

def find_mapping(source_elements, target_elements):
    """
    Simple heuristic mapping based on name similarity

    Rules:
    1. Exact match (case-insensitive)
    2. Partial match (one name contains the other)
    3. Common prefixes (customer*, item*, etc.)
    """
    mappings = []

    # Create lowercase mapping for comparison
    target_lower = {t.lower(): t for t in target_elements}

    for src in source_elements:
        src_lower = src.lower()
        matched = False

        # Rule 1: Exact match (case-insensitive)
        if src_lower in target_lower:
            mappings.append((src, target_lower[src_lower]))
            matched = True
            continue

        # Rule 2: Partial match
        if not matched:
            for tgt_lower, tgt in target_lower.items():
                if src_lower in tgt_lower or tgt_lower in src_lower:
                    mappings.append((src, tgt))
                    matched = True
                    break

        # Rule 3: Common prefix matching (customer*, item*, etc.)
        if not matched:
            for prefix in ['customer', 'item', 'order', 'delivery', 'ship']:
                if src_lower.startswith(prefix):
                    for tgt_lower, tgt in target_lower.items():
                        if prefix in tgt_lower:
                            mappings.append((src, tgt))
                            matched = True
                            break
                if matched:
                    break

        # If no match found, skip this element
        if not matched:
            print(f"  Warning: No mapping found for source element '{src}'")

    return mappings

def generate_xslt(source_root, target_root, mappings):
    """Generate XSLT based on mappings"""

    xslt_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>

  <!-- Auto-generated XSLT by simple mapping generator -->
  <xsl:template match="{source_root}">
    <{target_root}>'''

    for src, tgt in mappings:
        # Simple direct mapping
        xslt_template += f'''
      <{tgt}><xsl:value-of select="{src}"/></{tgt}>'''

    xslt_template += f'''
    </{target_root}>
  </xsl:template>

</xsl:stylesheet>
'''

    return xslt_template

def main():
    print("=" * 60)
    print("XSLT Generator - External Service Simulator")
    print("=" * 60)

    source_xsd = "../xsd/source_mini.xsd"
    target_xsd = "../xsd/target_mini.xsd"
    output_xslt = "../xslt/T1_candidate_generated.xslt"

    print(f"\n1. Reading source XSD: {source_xsd}")
    source_root, source_elements = parse_xsd(source_xsd)
    print(f"   Root: {source_root}")
    print(f"   Elements: {len(source_elements)} ({', '.join(source_elements[:5])}...)")

    print(f"\n2. Reading target XSD: {target_xsd}")
    target_root, target_elements = parse_xsd(target_xsd)
    print(f"   Root: {target_root}")
    print(f"   Elements: {len(target_elements)} ({', '.join(target_elements[:5])}...)")

    print(f"\n3. Finding element mappings...")
    mappings = find_mapping(source_elements, target_elements)
    print(f"   Found {len(mappings)} mappings:")
    for src, tgt in mappings[:10]:
        print(f"     {src:20s} -> {tgt}")
    if len(mappings) > 10:
        print(f"     ... and {len(mappings) - 10} more")

    print(f"\n4. Generating XSLT...")
    xslt_content = generate_xslt(source_root, target_root, mappings)

    with open(output_xslt, "w") as f:
        f.write(xslt_content)

    print(f"   Generated XSLT saved to: {output_xslt}")
    print(f"   Total lines: {len(xslt_content.splitlines())}")

    print("\n5. XSLT Preview:")
    print("-" * 60)
    lines = xslt_content.splitlines()
    for i, line in enumerate(lines[:20], 1):
        print(f"{i:3d}: {line}")
    if len(lines) > 20:
        print(f"     ... and {len(lines) - 20} more lines")
    print("-" * 60)

    print("\n" + "=" * 60)
    print("XSLT Generation Complete!")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"1. Copy generated XSLT to test location:")
    print(f"   cp {output_xslt} ../xslt/T1_candidate.xslt")
    print(f"2. Run test harness:")
    print(f"   cd ../scripts && python3 run_all.py")

if __name__ == "__main__":
    main()
