了解です！
では **実際に動くテストハーネスの雛形** を、すぐ実装できる形で提示します。
構成要素は以下の 6 つです：

1. **XSLT の静的解析（XPath 抽出）**
2. **抽出した要素名からのミニ XSD 生成**
3. **ミニ XSD からのテスト用 XML インスタンス生成**
4. **正解 XSLT（T₀）での変換 → ゴール XML 生成**
5. **候補 XSLT（T₁）での変換**
6. **正規化して XML 同値比較（差分取得）**

ここでは Python ベースで Saxon/C を利用した形にします。
ファイル構成は以下のようになる想定です：

```
project/
  xslt/
    T0_correct.xslt
    T1_candidate.xslt
  xsd/
    source_mini.xsd
    target_mini.xsd
  xml/
    generated_inputs/
    correct_outputs/
    candidate_outputs/
  scripts/
    extract_schema.py
    generate_xml.py
    transform.py
    compare.py
    run_all.py
```

---

# 🔧 **1. XSLT の静的解析（XPath 抽出）スクリプト**

`extract_schema.py`

```python
import re
from lxml import etree

def extract_xpaths(xslt_path):
    tree = etree.parse(xslt_path)
    ns = {"x": "http://www.w3.org/1999/XSL/Transform"}

    # xsl:value-of/@select などを抽出
    selects = tree.xpath("//x:*[@select]/@select", namespaces=ns)
    matches = []

    for sel in selects:
        # ".//a/b/text()" などから要素名をざっくり抽出
        tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_\-]*", sel)
        matches.extend(tokens)

    return sorted(set(matches))


if __name__ == "__main__":
    xslt = "../xslt/T0_correct.xslt"
    elems = extract_xpaths(xslt)

    print("Extracted element/attr names:")
    for e in elems:
        print(" -", e)

    # ミニ XSD の材料としてファイル出力
    with open("../xsd/_extracted_names.txt", "w") as f:
        f.write("\n".join(elems))
```

**ポイント**

* 完全解析ではなく “T₀ が使っている名前要素セット” を抽出する。
* あくまで「ミニ XSD」を作る材料。

---

# 📘 **2. ミニ XSD 生成（テスト用）**

`generate_mini_xsd.py`

```python
def generate_xsd(element_names, root="Root"):
    xsd_header = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="%s">
    <xs:complexType>
      <xs:sequence>
""" % root

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
```

**ポイント**

* minOccurs=0 や maxOccurs=2 にしてテストの幅を出す。
* 生成 XSD は “入力の構造をざっくりカバー” すれば十分。

---

# 🧪 **3. XSD から XML インスタンスを生成する**

`generate_xml.py`

```python
import random
import xml.etree.ElementTree as ET

def generate_xml(xsd_names, case_id):
    root = ET.Element("Source")

    for name in xsd_names:
        # ランダムに出現有無を決める
        if random.choice([True, False]):
            for i in range(random.randint(1,2)):
                elem = ET.SubElement(root, name)
                elem.text = f"test_{name}_{case_id}_{i}"

    return ET.tostring(root, encoding="utf-8")

if __name__ == "__main__":
    cases = 20

    with open("../xsd/_extracted_names.txt") as f:
        names = [n.strip() for n in f]

    for cid in range(cases):
        xml = generate_xml(names, cid)
        with open(f"../xml/generated_inputs/input_{cid}.xml", "wb") as f:
            f.write(xml)
```

**ポイント**

* ランダム生成で十分（正確性より「多様性」を重視）。
* 20〜100 ケースぐらい生成してカバレッジを確保。

---

# 🔄 **4. Saxon を使って変換（正解 T₀）**

`transform.py`

```python
import subprocess
import os

SAXON = "saxon"   # Saxon-HE が PATH にある前提

def transform(xslt, src, out):
    subprocess.run([SAXON, f"-xsl:{xslt}", f"-s:{src}", f"-o:{out}"])

if __name__ == "__main__":
    T0 = "../xslt/T0_correct.xslt"
    input_dir = "../xml/generated_inputs/"
    out_dir = "../xml/correct_outputs/"

    os.makedirs(out_dir, exist_ok=True)

    for f in os.listdir(input_dir):
        transform(T0, input_dir + f, out_dir + f.replace("input", "out"))
```

---

# 🆚 **5. 候補 XSLT（T₁）でも同じ入力を変換**

（T₁ の path を変えるだけなので transform.py を共用）

---

# 🔍 **6. XML 正規化して比較**

`compare.py`

```python
from lxml import etree
import os

def normalize(xml_path):
    tree = etree.parse(xml_path)
    return etree.tostring(tree, method="c14n")

def compare(f_correct, f_candidate):
    c1 = normalize(f_correct)
    c2 = normalize(f_candidate)
    return c1 == c2

if __name__ == "__main__":
    correct = "../xml/correct_outputs/"
    candidate = "../xml/candidate_outputs/"

    for f in os.listdir(correct):
        ok = compare(correct + f, candidate + f)
        print(f, "OK" if ok else "DIFF")
```

**ポイント**

* C14N（XML Canonicalization）で比較 → 空白や属性順の差異を吸収できる。
* NG の場合は xmldiff を追加して差分内容を取得可能。

---

# 🚀 **7. 全体を実行するワンショットスクリプト**

`run_all.py`

```python
import subprocess

print("1. Extract schema from T0...")
subprocess.run(["python", "extract_schema.py"])

print("2. Generate mini XSD...")
subprocess.run(["python", "generate_mini_xsd.py"])

print("3. Generate XML instances...")
subprocess.run(["python", "generate_xml.py"])

print("4. Transform using T0...")
subprocess.run(["python", "transform.py"])

print("5. Transform using T1...")
subprocess.run(["python", "transform.py", "--candidate"])

print("6. Compare outputs...")
subprocess.run(["python", "compare.py"])
```

---

# 🧩 **このテストハーネスの到達点**

あなたが望んでいた、

> 「正解の XSLT→スキーマ推定→XSLT 自動生成→比較」

のうち、

* **正解 XSLT → （テスト用）スキーマ断片抽出**
* **そのスキーマによる入力生成**
* **正解 XSLT でゴール生成**
* **候補 XSLT で比較**

まで自動化しました。

XSLT 自動生成部分（T₁生成）も、必要なら続けて作れます。

* ルールベース生成
* XPath マッピング推論
* 対応ノードの類似度マッチング
  など、何段階かレベルがあります。

---

必要なら、**XSLT 自動合成器（T₁生成器）**も作りますか？
あるいは、テストハーネスを **Saxon-JS ベース** にする／**Java プロジェクト化**するなどもできます。
