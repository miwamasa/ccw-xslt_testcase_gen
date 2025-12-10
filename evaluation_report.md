# XSLT Generator Evaluation Report

## 概要

外部XSLTジェネレータサービスのシミュレーションを行い、生成されたXSLTをテストハーネスで評価しました。

## テスト構成

### 入力（XSDスキーマ）

**ソースXSD** (`xsd/source_mini.xsd`):
- ルート要素: `Order`
- 要素数: 15個
- 構造: フラット
- 要素例: `city`, `country`, `customerEmail`, `customerName`, `itemCode`, etc.

**ターゲットXSD** (`xsd/target_mini.xsd`):
- ルート要素: `Invoice`
- 要素数: 19個（属性含む）
- 構造: 入れ子（フラットに展開されている）
- 要素例: `Address`, `City`, `CustomerInfo`, `Items`, `Name`, `Email`, etc.

### XSLTジェネレータ

**シミュレーター**: `scripts/xslt_generator_simulator.py`

**アルゴリズム**:
1. 名前の完全一致（大文字小文字を区別しない）
2. 部分一致（一方が他方を含む）
3. 共通プレフィックスマッチング（customer*, item*など）

**生成結果**:
- マッピング数: 14個（15要素中）
- 生成XSLT: フラット変換のみ
- 失敗: `orderNumber`（マッピング不可）

## テスト結果

### 実行結果

```
Running: python extract_schema.py
Running: python generate_mini_xsd.py
Running: python generate_target_xsd.py
Running: python generate_xml.py
Running: python transform.py
Running: python transform.py --candidate
Running: python compare.py
input_0.xml DIFF
input_1.xml DIFF
input_2.xml DIFF
input_3.xml DIFF
input_4.xml DIFF
```

**結果**: 5/5 テストケースで DIFF（不一致）

### 差分分析

#### 構造の違い

**正解XSLT（T0_correct.xslt）:**
```xml
<Invoice id="">
  <CustomerInfo>
    <Name/>
    <Email/>
  </CustomerInfo>
  <Items>
    <Item code="test_itemCode_2_0">
      <Description>test_itemName_2_0</Description>
      <Quantity/>
      <Price currency="USD"/>
    </Item>
  </Items>
  <ShippingDetails>
    <Address>
      <Street>test_street_2_0</Street>
      <City/>
    </Address>
    <RequestedDelivery>test_deliveryDate_2_0</RequestedDelivery>
  </ShippingDetails>
</Invoice>
```

**生成XSLT（候補）:**
```xml
<Invoice>
  <City/>
  <Country/>
  <Email/>
  <Name/>
  <Phone/>
  <RequestedDelivery>test_deliveryDate_2_0</RequestedDelivery>
  <Item>test_item_2_0</Item>
  <Item>test_itemCode_2_0</Item>
  <Item>test_itemName_2_0</Item>
  <Price/>
  <Quantity/>
  <State/>
  <Street>test_street_2_0</Street>
  <code/>
</Invoice>
```

#### 主な差異

| 項目 | 正解XSLT | 生成XSLT | 評価 |
|------|---------|---------|------|
| **構造** | 入れ子（3階層） | フラット（2階層） | ❌ 不一致 |
| **グループ化** | CustomerInfo, Items, ShippingDetails | なし | ❌ 不一致 |
| **繰り返し処理** | for-each で複数Item生成 | 単純マッピングのみ | ❌ 不一致 |
| **属性** | id, code, currency | なし（codeが要素に） | ❌ 不一致 |
| **条件分岐** | xsl:if で存在チェック | なし | ❌ 不一致 |
| **要素マッピング** | ビジネスロジックベース | 名前類似性ベース | △ 部分的 |

## 問題点の分析

### 1. XSDの限界

**問題**: 生成されたターゲットXSDはフラット構造

ターゲットXSDが以下のようにフラットな要素リストとして抽出されています：

```xml
<xs:element name="Address" minOccurs="0" maxOccurs="unbounded" type="xs:string"/>
<xs:element name="City" minOccurs="0" maxOccurs="unbounded" type="xs:string"/>
<xs:element name="CustomerInfo" minOccurs="0" maxOccurs="unbounded" type="xs:string"/>
```

実際の正解XSLTでは、これらは以下のような入れ子構造です：

```xml
<Invoice>
  <CustomerInfo>
    <Name/>
    <Email/>
  </CustomerInfo>
  <ShippingDetails>
    <Address>
      <City/>
      <Street/>
    </Address>
  </ShippingDetails>
</Invoice>
```

**原因**: `extract_output_elements()`がすべての要素を平坦に抽出

**影響**: ジェネレータが正しい階層構造を推測できない

### 2. 属性と要素の区別不可

**問題**: XSDで`id`と`code`が要素として定義されている

正解XSLTでは：
- `id` → `<Invoice>`の属性
- `code` → `<Item>`の属性

生成XSLTでは：
- `id` → マッピングなし（無視）
- `code` → `<code>`要素として出力

**原因**: スキーマ抽出時に属性と要素を区別していない

### 3. 繰り返し処理の推測不可

**問題**: `item`要素が複数あることをXSLTジェネレータが認識できない

正解XSLTでは：
```xml
<xsl:for-each select="item">
  <Item code="{../itemCode}">
    <Description><xsl:value-of select="../itemName"/></Description>
  </Item>
</xsl:for-each>
```

生成XSLTでは：
```xml
<Item><xsl:value-of select="item"/></Item>
<Item><xsl:value-of select="itemCode"/></Item>
<Item><xsl:value-of select="itemName"/></Item>
```

**原因**: 要素間の関連性（item, itemCode, itemNameが関連している）を推測できない

### 4. ビジネスロジックの欠如

**問題**: 名前マッピングのみでは、ビジネスロジックを再現できない

例：
- `customerName` → `Name`（CustomerInfo内）
- `itemName` → `Description`（Item内）

両方とも"Name"を含むが、配置場所とセマンティクスが異なります。

## 提言

### テストハーネスの改善

#### 1. 階層構造を持つXSD生成

現在の`extract_output_elements()`を拡張：

```python
def extract_output_structure(xslt_path):
    """Extract hierarchical structure of output elements"""
    # 親子関係を追跡
    # 戻り値: ツリー構造
```

#### 2. 属性と要素の明示的な区別

XSD生成時に属性を正しく定義：

```xml
<xs:complexType>
  <xs:sequence>
    <xs:element name="CustomerInfo">
      <xs:complexType>
        <xs:sequence>
          <xs:element name="Name" type="xs:string"/>
        </xs:sequence>
      </xs:complexType>
    </xs:element>
  </xs:sequence>
  <xs:attribute name="id" type="xs:string"/>
</xs:complexType>
```

#### 3. 要素間の関連性メタデータ

XSLTから抽出：
- 同じfor-each内の要素 → グループ化のヒント
- 属性参照のパターン → 親子関係のヒント

### XSLTジェネレータの改善

#### 1. セマンティックマッピング

単純な名前マッチングではなく：
- ビジネスドメイン知識の活用
- ML/AIベースの要素マッピング
- ユーザーフィードバックによる学習

#### 2. 階層構造の推論

ターゲットXSDの構造情報を活用：
- グループ化パターンの認識
- 親子関係の推測

#### 3. サンプルベース学習

既存のXSLT変換例から学習：
- パターン認識
- テンプレートライブラリ

## 結論

### 検証結果

テストハーネスは、**外部XSLTジェネレータの品質を正しく評価**できました：

✅ **成功点**:
- 5つのテストケースすべてで差分を検出
- フラット vs 入れ子構造の違いを識別
- 属性の欠落を検出
- グループ化の欠如を検出

❌ **ジェネレータの課題**:
- 階層構造の生成不可
- 属性の正しい配置不可
- 繰り返し処理の生成不可
- ビジネスロジックの推測不可

### 推奨事項

1. **XSD生成の改善が必須**
   - 階層構造の保持
   - 属性と要素の区別
   - 要素間の関連性メタデータ

2. **テストハーネスは機能的**
   - 現状でも基本的な差分検出は可能
   - より詳細な診断情報の追加を推奨

3. **XSLTジェネレータには高度な推論が必要**
   - 単純なヒューリスティックでは不十分
   - 構造情報、ドメイン知識、学習機能が必要

## 付録

### 生成されたファイル

```
xsd/
├── source_mini.xsd              # ソーススキーマ
├── target_mini.xsd              # ターゲットスキーマ
├── _extracted_names.txt         # ソース要素リスト
├── _target_names.txt            # ターゲット要素リスト
├── _root_element.txt            # ソースルート要素
└── _target_root_element.txt     # ターゲットルート要素

xslt/
├── T0_correct.xslt              # 正解XSLT（手動作成）
├── T1_candidate_generated.xslt  # 生成XSLT（ジェネレータ）
└── T1_candidate.xslt            # テスト用コピー

xml/
├── generated_inputs/            # 5個のテストXML
├── correct_outputs/             # 正解XSLTの出力
└── candidate_outputs/           # 生成XSLTの出力
```

### テスト統計

- テストケース総数: 5
- 一致: 0 (0%)
- 不一致: 5 (100%)
- エラー: 0

### 実行時間

- スキーマ抽出: < 1秒
- XSD生成: < 1秒
- XSLT生成: < 1秒
- テストXML生成: < 1秒
- 変換実行: < 1秒
- 比較: < 1秒
- **合計: < 5秒**

---

**作成日**: 2025-12-10
**テストハーネスバージョン**: 1.0
**XSLTジェネレータ**: Simple Heuristic Simulator
