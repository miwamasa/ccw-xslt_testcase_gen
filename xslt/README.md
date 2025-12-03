# XSLTサンプル集

このディレクトリには、テストハーネス用のXSLTサンプルが含まれています。

## 必須ファイル

テストハーネスを実行するには、以下の2つのファイルが必須です：

- **T0_correct.xslt** - 正解XSLT（テスト基準）
- **T1_candidate.xslt** - 候補XSLT（テスト対象）

これらのファイルは`scripts/run_all.py`で自動的に使用されます。

## 提供されているサンプル

### シンプルな変換サンプル

**ファイル:**
- `simple_T0_correct.xslt`
- `simple_T1_candidate.xslt`

**変換内容:**
- フラットなソース構造からフラットなターゲット構造へ
- 要素名の変更のみ（name → fullName、age → years、city → location）
- ルート要素: `Source` → `Target`

**使用例:**
```xml
<!-- 入力 -->
<Source>
  <name>John Doe</name>
  <age>30</age>
  <city>Tokyo</city>
</Source>

<!-- 出力 -->
<Target>
  <fullName>John Doe</fullName>
  <years>30</years>
  <location>Tokyo</location>
</Target>
```

### 複雑な変換サンプル（デフォルト）

**ファイル:**
- `complex_T0_correct.xslt`
- `complex_T1_candidate.xslt`

**変換内容:**
- フラットなソース構造から深く入れ子のターゲット構造へ
- 要素のグループ化（CustomerInfo、Items、ShippingDetails）
- 繰り返し処理（`xsl:for-each`）
- 条件分岐（`xsl:if`）
- 属性の生成
- ルート要素: `Order` → `Invoice`

**使用例:**
```xml
<!-- 入力 -->
<Order>
  <orderNumber>12345</orderNumber>
  <customerName>John Doe</customerName>
  <customerEmail>john@example.com</customerEmail>
  <item>Widget</item>
  <itemCode>W001</itemCode>
  <itemName>Super Widget</itemName>
  <quantity>5</quantity>
  <price>100.00</price>
  <street>123 Main St</street>
  <city>Tokyo</city>
  <country>Japan</country>
</Order>

<!-- 出力 -->
<Invoice id="12345">
  <CustomerInfo>
    <Name>John Doe</Name>
    <Email>john@example.com</Email>
  </CustomerInfo>
  <Items>
    <Item code="W001">
      <Description>Super Widget</Description>
      <Quantity>5</Quantity>
      <Price currency="USD">100.00</Price>
    </Item>
  </Items>
  <ShippingDetails>
    <Address>
      <Street>123 Main St</Street>
      <City>Tokyo</City>
      <Country>Japan</Country>
    </Address>
  </ShippingDetails>
</Invoice>
```

## サンプルの切り替え方法

### 方法1: ファイルをコピー

使いたいサンプルをT0/T1ファイルにコピーします：

```bash
# シンプルな変換を使う場合
cd xslt
cp simple_T0_correct.xslt T0_correct.xslt
cp simple_T1_candidate.xslt T1_candidate.xslt

# 複雑な変換を使う場合
cd xslt
cp complex_T0_correct.xslt T0_correct.xslt
cp complex_T1_candidate.xslt T1_candidate.xslt
```

### 方法2: extract_schema.pyを修正

`scripts/extract_schema.py`の以下の行を変更：

```python
# デフォルト
xslt = "../xslt/T0_correct.xslt"

# シンプルなサンプルを直接使う場合
xslt = "../xslt/simple_T0_correct.xslt"

# 複雑なサンプルを直接使う場合
xslt = "../xslt/complex_T0_correct.xslt"
```

また、`scripts/transform.py`も同様に修正が必要です。

## 独自のXSLTを追加

独自のXSLTをテストする場合：

1. 正解XSLTを`T0_correct.xslt`として保存
2. 候補XSLTを`T1_candidate.xslt`として保存
3. `cd scripts && python3 run_all.py`を実行

## サンプルの特徴比較

| 特徴 | シンプル | 複雑 |
|------|---------|------|
| 構造の変更 | なし（フラット→フラット） | あり（フラット→入れ子） |
| 要素のグループ化 | なし | あり |
| 繰り返し処理 | なし | あり（for-each） |
| 条件分岐 | なし | あり（if） |
| 属性の生成 | なし | あり |
| テストケース生成 | 3要素（name, age, city） | 15要素（顧客、商品、住所情報） |
| 学習難易度 | 初級 | 中級 |

## トラブルシューティング

### 問題: ルート要素がマッチしない

**症状**: 変換結果が空または予期しない出力

**原因**: ソースXMLのルート要素とXSLTの`<xsl:template match="...">`が一致していない

**対処**:
- `simple_*`はルート要素が`Source`である必要があります
- `complex_*`はルート要素が`Order`である必要があります
- 独自のXSLTを使う場合、ルート要素名を確認してください

### 問題: 要素が抽出されない

**原因**: XSLTで使用している要素名が複雑すぎる

**対処**:
- `xsd/_extracted_names.txt`を確認
- 必要に応じて手動で要素名を追加
