
from lxml import etree
import os
def normalize(xml_path):
    tree = etree.parse(xml_path)
    return etree.tostring(tree, method="c14n")
def compare(f_correct, f_candidate):
    return normalize(f_correct) == normalize(f_candidate)

if __name__ == "__main__":
    correct = "../xml/correct_outputs/"
    candidate = "../xml/candidate_outputs/"
    for f in os.listdir(correct):
        print(f, "OK" if compare(correct+f, candidate+f) else "DIFF")
