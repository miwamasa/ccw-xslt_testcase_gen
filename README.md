# XSLT テストケース自動生成ハーネス

## 概要

このテストハーネスは、正解XSLT（T0）から自動的にテストケースを生成し、候補XSLT（T1）の出力と比較するツールです。

### 目的

XSLT変換の正しさを検証するために：
1. **正解XSLT**から使用される要素名を抽出
2. 抽出した要素からミニXSDスキーマを自動生成
3. ミニXSDからテスト用XMLを複数生成
4. 正解XSLTと候補XSLTでそれぞれ変換
5. 両者の出力を比較して差分を検出

## ディレクトリ構造

```
ccw-xslt_testcase_gen/
├── README.md                    # このファイル
├── instructions.md              # 研究背景と設計思想
├── doc/                         # 詳細なドキュメント
│   ├── the_method.md           # 手法の詳細説明
│   └── the_harness.md          # ハーネスの実装詳細
├── scripts/                     # テストハーネスの実装
│   ├── run_all.py              # 全ステップを実行するメインスクリプト
│   ├── extract_schema.py       # XSLTから要素名を抽出
│   ├── generate_mini_xsd.py    # ミニXSDスキーマ生成
│   ├── generate_xml.py         # テスト用XML生成
│   ├── transform.py            # XSLT変換実行
│   └── compare.py              # 出力の比較
├── xslt/                        # XSLTファイルを配置
│   ├── T0_correct.xslt         # 正解XSLT（必須）
│   └── T1_candidate.xslt       # 候補XSLT（必須）
├── xsd/                         # 生成されるXSDファイル（自動生成）
│   ├── _extracted_names.txt    # 抽出された要素名リスト
│   └── source_mini.xsd         # 生成されたミニXSD
└── xml/                         # 生成されるXMLファイル（自動生成）
    ├── generated_inputs/        # 生成されたテスト入力XML
    ├── correct_outputs/         # 正解XSLTの出力
    └── candidate_outputs/       # 候補XSLTの出力
```

## 前提条件

### 必須の依存関係

- **Python 3.x**
- **lxml** - XPathパース、XML正規化に使用
- **xsltproc** - XSLT変換エンジン（libxslt1-dev）

### インストール方法

```bash
# Python依存関係
pip3 install lxml

# xsltprocのインストール（Ubuntu/Debian）
sudo apt-get install -y libxslt1-dev xsltproc

# xsltprocのインストール（macOS）
brew install libxslt
```

## 使い方

### 基本的な使用手順

#### ステップ1: XSLTファイルの配置

正解XSLTと候補XSLTを以下のパスに配置します：

```bash
xslt/T0_correct.xslt      # 正解XSLT
xslt/T1_candidate.xslt    # 候補XSLT（テスト対象）
```

**付属のサンプルを使用する場合:**

`xslt/`ディレクトリには以下のサンプルが用意されています：

- **シンプルな変換** (`simple_T0_correct.xslt` / `simple_T1_candidate.xslt`)
  - フラット構造からフラット構造への変換
  - 要素名の変更のみ（初学者向け）

- **複雑な変換** (`complex_T0_correct.xslt` / `complex_T1_candidate.xslt`) **← デフォルト**
  - フラット構造から入れ子構造への変換
  - グループ化、繰り返し、条件分岐を含む（実践的）

詳細は`xslt/README.md`を参照してください。

サンプルを切り替える場合：
```bash
# シンプルな変換を使う
cp xslt/simple_T0_correct.xslt xslt/T0_correct.xslt
cp xslt/simple_T1_candidate.xslt xslt/T1_candidate.xslt

# 複雑な変換を使う（デフォルト）
cp xslt/complex_T0_correct.xslt xslt/T0_correct.xslt
cp xslt/complex_T1_candidate.xslt xslt/T1_candidate.xslt
```

#### ステップ2: テストハーネスの実行

```bash
cd scripts
python3 run_all.py
```

これにより、以下の処理が自動的に実行されます：

1. **スキーマ抽出** - `T0_correct.xslt`から要素名を抽出
2. **XSD生成** - 抽出された要素からミニXSDを生成
3. **テストXML生成** - ランダムなテストケース（デフォルト5個）を生成
4. **正解変換** - 正解XSLTでテストXMLを変換
5. **候補変換** - 候補XSLTでテストXMLを変換
6. **比較** - 両者の出力を正規化して比較

#### ステップ3: 結果の確認

出力例：
```
Running: python extract_schema.py
Running: python generate_mini_xsd.py
Running: python generate_xml.py
Running: python transform.py
Running: python transform.py --candidate
Running: python compare.py
input_0.xml OK
input_1.xml OK
input_2.xml DIFF
input_3.xml OK
input_4.xml OK
```

- **OK** - 正解と候補の出力が一致
- **DIFF** - 正解と候補の出力に差異あり

### 個別ステップの実行

各ステップを個別に実行することも可能です：

```bash
cd scripts

# 1. 要素名抽出
python3 extract_schema.py

# 2. ミニXSD生成
python3 generate_mini_xsd.py

# 3. テストXML生成
python3 generate_xml.py

# 4. 正解XSLTで変換
python3 transform.py

# 5. 候補XSLTで変換
python3 transform.py --candidate

# 6. 結果比較
python3 compare.py
```

## XSLTの制限事項

このテストハーネスは以下の制限があります。ご使用前に必ずご確認ください。

### ✅ サポートされる機能

- `xsl:value-of`、`xsl:apply-templates`、`xsl:template`などの基本的なXSLT要素
- XPath式による要素選択（`@select`属性）
- 要素名、属性名の抽出
- 名前空間の使用

### ⚠️ 制限事項

1. **静的解析の限界**
   - XPath式から要素名を正規表現で抽出するため、完全な解析ではありません
   - `//element[@attr='value']`のような複雑なXPathも単純化されます
   - 動的に生成される要素名は抽出できません

2. **外部依存の非サポート**
   - `document()` 関数による外部ファイル参照は未サポート
   - XSLT拡張関数（extension functions）は使用できません
   - 外部パラメータの渡し方には制限があります

3. **XSDの近似性**
   - 生成されるミニXSDは「テスト用の近似スキーマ」です
   - 元の完全なXSDを復元することはできません
   - `minOccurs="0"`, `maxOccurs="2"`, `type="xs:string"`として簡略化されます

4. **変換エンジンの制約**
   - xsltprocはXSLT 1.0のみサポート（XSLT 2.0/3.0は非対応）
   - XSLT 2.0/3.0を使用する場合はSaxon等に変更が必要です

5. **テストデータの多様性**
   - ランダム生成のため、すべてのエッジケースをカバーする保証はありません
   - 必要に応じて手動でテストXMLを追加してください

### 制限事項への対処方法

複雑なXSLTを使用する場合：
- 外部ファイルは相対パスで配置し、モックデータを用意
- 拡張関数を使う部分は別途手動テストが必要
- XSLT 2.0/3.0を使う場合は`scripts/transform.py`を修正してSaxonを使用

## カスタマイズ

### テストケース数の変更

`scripts/generate_xml.py`の以下の行を編集：

```python
cases = 5  # この数値を変更
```

### XSDスキーマのカスタマイズ

`scripts/generate_mini_xsd.py`で以下をカスタマイズ可能：

```python
# 出現回数の制限
xsd_body += f'<xs:element name="{e}" minOccurs="0" maxOccurs="2" type="xs:string"/>\n'
```

### XSLTエンジンの変更

Saxonなど他のXSLTプロセッサを使用する場合は`scripts/transform.py`を編集：

```python
# xsltprocの代わりにSaxonを使用する例
SAXON = "java -jar /path/to/saxon.jar"
def transform(xslt, src, out):
    subprocess.run([SAXON, f"-xsl:{xslt}", f"-s:{src}", f"-o:{out}"])
```

## トラブルシューティング

### 問題: 要素が抽出されない

**原因**: XPath式が複雑すぎるか、要素が`@select`属性以外で参照されている

**対処**:
- `xsd/_extracted_names.txt`の内容を確認
- 必要に応じて手動で要素名を追加

### 問題: 全テストケースがDIFF

**原因**: 候補XSLTに誤りがあるか、インデントなどの形式差異

**対処**:
- 生成された出力を直接確認：
  ```bash
  diff xml/correct_outputs/input_0.xml xml/candidate_outputs/input_0.xml
  ```
- XML正規化（C14N）を使用しているため、空白やコメントの違いは無視されます

### 問題: xsltprocがインストールされていない

**エラー**: `xsltproc: command not found`

**対処**:
```bash
# Ubuntu/Debian
sudo apt-get install xsltproc

# macOS
brew install libxslt
```

### 問題: lxmlがインストールされていない

**エラー**: `ModuleNotFoundError: No module named 'lxml'`

**対処**:
```bash
pip3 install lxml
```

## 高度な使用方法

### 手動でテストXMLを追加

`xml/generated_inputs/`に直接XMLファイルを配置することで、特定のテストケースを追加できます：

```bash
# 手動テストケースの追加
cp my_custom_test.xml xml/generated_inputs/input_custom.xml

# 変換と比較のみ実行
cd scripts
python3 transform.py
python3 transform.py --candidate
python3 compare.py
```

### 差分の詳細確認

XMLの差分を詳しく見る場合：

```bash
# xmldiffをインストール
pip3 install xmldiff

# 差分の詳細表示
xmldiff xml/correct_outputs/input_2.xml xml/candidate_outputs/input_2.xml
```

## 研究背景

このツールは以下の研究質問に基づいています：

> ソースとターゲットのXSDが与えられたときに、双方のXSDをみて、XML変換のXSLTを作ろうとしている。その際テストデータを作らなければならず、XSLTが与えられたとき、これからソースのXSD、ターゲットのXSDを推定して、それらを使ってテストを生成させて、最初の正解XSLTと比較するようなテストは可能だろうか？

詳細は`doc/the_method.md`と`doc/the_harness.md`を参照してください。

## ライセンス

このプロジェクトは研究目的で作成されています。

## 参考資料

- [XSLT 1.0 Specification](https://www.w3.org/TR/xslt-10/)
- [libxslt (xsltproc) Documentation](http://xmlsoft.org/XSLT/)
- [lxml Documentation](https://lxml.de/)
