# OuDia/OuDiaSecond File Specification

This file is an unofficial specification of the OuDia/OuDiaSecond file format, which is used by their respective programs to create transportation system diagrams. This document has been compiled by analyzing files, existing implementations, and available documentation.

## BNF defintion

```bnf
<file> ::= <root_node>

<root_node> ::= <attribute_list> <children_list> <trailing_attributes>

<attribute_list> ::= <attribute> | <attribute> <attribute_list>
<attribute> ::= <key> "=" <value> <newline>

<children_list> ::= <child_node> | <child_node> <children_list>

<child_node> ::= <node_header> <attribute_list> <children_list> <trailing_attributes> <node_footer>

<node_header> ::= <node_type> "." <newline>
<node_type> ::= "Rosen" | "Eki" | "Ressyasyubetsu" | "Dia" | "Kudari" | ...

<node_footer> ::= "." <newline>

<trailing_attributes> ::= <attribute_list> | ε

<key> ::= <camel_case_Text>
<value> ::= <alphanumeric_Text>

<camel_case_Text> ::= <capital_letter> <alphanumeric_Text> | <capital_letter> <alphanumeric_Text> <camel_case_Text>

<capital_letter> ::= "A" | "B" | "C" | ... | "Z"
<alphanumeric_Text> ::= <letter> | <letter> <alphanumeric_Text> | <digit> | <digit> <alphanumeric_Text>

<letter> ::= "a" | "b" | "c" | ... | "z" | <capital_letter>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

<newline> ::= "\n"
```

## Structure

An OuDia file (`.oud`) or OuDiaSecond file (`.oud2`) is a plain text file typically encoded in `UTF-8 BOM`. These files consist of multiple lines, typically separated by CRLF (`\r\n`). A number of lines are grouped into a node, and each node has a type.

The file itself (`<file>`) is a node called the root node (`<root_node>`). Non-root nodes (`<child_node>`) must begin with a header (`<node_header>`) that follows the format `Type.` where `Type` represents the node type, and end with a footer (`<node_footer>`), which is always `.`. The root node does not contain a header or footer.

Each node has attributes (`<attribute_list>`), children, and trailing attributes, in this order.

Each node can have one or more attributes, which are either required or optional, depending on the node's type. A required attribute may have an empty value. Each attributes is defined using the format `Key=Value`, where the `Key` is written in CamelCase, and `Value` is the Text representation of the attribute’s value. Usually a key is unique for a node, however sometimes some specific key (such as `JikokuhyouFont` in `DispProp`) can be set multiple times with different value.

A node can also contain zero or more child nodes, allowing for hierarchical structures. The types of child nodes a node can have are determined by its own type. Not all nodes support children, and the specific types of allowed child nodes vary based on the parent node's type.

In addition to the primary attributes and child nodes, some nodes may include **trailing attributes**, which are a secondary list of attributes. These trailing attributes are placed after the list of child nodes and often serve as supplementary data that follows the main content of the node.

### Root Node

The **root node** represents the entire file. It contains various attributes that define metadata about the file and serves as the top-level container for all the other nodes. This node does not have a header (`Type.`) or footer (`.`), unlike the other nodes.

#### Attributes

- `FileType` ([Text](#data-types), [required](#field-tags)): Specifies the version of the file format, for example, "OuDia.1.02". This may not necessarily be the same as the version of the program that generated the file.

#### Children

The root node can contain the following children nodes:

- [Rosen](#Rosen_Node): Represents a route or line.
- [DispProp](#DispProp_Node): Contains display properties like font styles and colors used in diagrams.
- [WindowPlacement](#WindowPlacement_Node): Contains window view positions.

#### Trailing Attributes

- `FileTypeAppComment` ([Text](#data-types), [optional](#field-tags)): Additional comments related to the file type or application, possibly detailing the version of the application or any specific information.

### Rosen Node

The **Rosen Node** represents a single route or line in the transportation system (路線). This node contains attributes describing the route and can have child nodes that describe the stations (Eki), train types (Ressyasyubetsu), and timetables (Dia).

#### Attributes

- `Rosenmei` ([Text](#data-types), [required](#field-tags)): The name of the route (路線名), e.g., "東急東横線".
- `KudariDiaAlias` ([Text](#data-types), [optional](#field-tags)): Alias for the "Kudari" (下り) direction (downward route). [OuDiaSecond.1.04+](http://oudiasecond.seesaa.net/article/459366976.html)
- `NoboriDiaAlias` ([Text](#data-types), [optional](#field-tags)): Alias for the "Nobori" (上り) direction (upward route). [OuDiaSecond.1.04+](http://oudiasecond.seesaa.net/article/459366976.html)

### Children

The Rosen Node can contain the following children nodes:

- [Eki Node](#Eki_Node): Represents individual stations on the route. Multiple Eki nodes can be listed.
- [Ressyasyubetsu Node](#Ressyasyubetsu_Node): Describes the types of trains that run on the route.
- [Dia Node](#Dia_Node): Contains timetable data for different days or schedules (e.g., weekdays, weekends).

#### Trailing Attributes

- `KitenJikoku` ([Text](#data-types), [optional](#field-tags)): The starting time of the route's operation, e.g., "400" for 4:00 AM.
- `DiagramDgrYZahyouKyoriDefault` ([Number](#data-types), [optional](#field-tags)): Default Y-coordinate distance between stations in diagrams.
- `EnableOperation` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether operational functionality is enabled. [OuDiaSecond.1.03+](http://oudiasecond.seesaa.net/article/457223251.html)
- `OperationCrossKitenJikoku` ([Number](#data-types), [optional](#field-tags)): Indicates whether connecting operations across the diagram start time is enabled. [OuDiaSecond.1.10+](http://oudiasecond.seesaa.net/article/481081211.html)
- `KijunDiaIndex` ([Number](#data-types), [optional](#field-tags)): Reference diagram index.
- `Comment` ([Text](#data-types), [optional](#field-tags)): Any comments regarding the route, such as service notes or special instructions.

### Eki Node

The **Eki Node** represents a station (駅) on the route. It provides information about the station’s name, its timetable style, and its operational role.

#### Attributes

- `Ekimei` ([Text](#data-types), [required](#field-tags)): The name of the station, e.g., "和光市".
- `Ekijikokukeisiki` ([Enumeration](#data-types), [required](#field-tags)): The type of timetable associated with the station. Possible values include:
  - `"Jikokukeisiki_Hatsu"` (departure only)
  - `"Jikokukeisiki_Hatsuchaku"` (both arrival and departure)
  - `"Jikokukeisiki_KudariChaku"` (arrival for downward trains)
  - `"Jikokukeisiki_NoboriChaku"` (arrival for upward trains)
- `Ekikibo` ([Enumeration](#data-types), [required](#field-tags)): The station's classification based on its importance. Possible values include:
  - `"Ekikibo_Syuyou"` (major station)
  - `"Ekikibo_Ippan"` (general station)

#### Children

The **Eki Node** can contain the following child nodes:

- **EkiTrack2 Node**: (optional, [repeatable](#field-tags)) Describes the track layout of the station, including the track names, abbreviations, and configurations for upward and downward directions.
- **OuterTerminal Node**: (optional, [repeatable](#field-tags)) Represents outer terminals that are connected to the station but belong to another line.

#### Trailing Attributes

- `Kyoukaisen` ([Number](#data-types), [optional](#field-tags)): Specifies if the station is part of a boundary line between two jurisdictions.
- `DiagramRessyajouhouHyoujiKudari` ([Enumeration](#data-types), [optional](#field-tags)): Controls the display of timetable information for downward-bound trains. Possible values include:
  - `"DiagramRessyajouhouHyouji_Anytime"` (always displayed)
  - `"DiagramRessyajouhouHyouji_Not"` (not displayed)
- `DiagramRessyajouhouHyoujiNobori` ([Enumeration](#data-types), [optional](#field-tags)): Same as `DiagramRessyajouhouHyoujiKudari`, but for upward-bound trains.

### Ressyasyubetsu Node

The **Ressyasyubetsu Node** describes the types of trains that operate on the route (列車種別). Each train type has attributes for its display color and style on both diagrams and timetables.

#### Attributes

- `Syubetsumei` ([Text](#data-types), [required](#field-tags)): The name of the train type, e.g., "通勤特急" (commuter express).
- `Ryakusyou` ([Text](#data-types), [optional](#field-tags)): The abbreviation used for the train type.
- `JikokuhyouMojiColor` ([Text](#data-types), [required](#field-tags)): The color used for displaying the train type on timetables, represented as a hexadecimal color code (e.g., `"000000FF"` for blue).
- `JikokuhyouFontIndex` ([Number](#data-types), [required](#field-tags)): The font index used for displaying the train type on timetables.
- `JikokuhyouBackColor` ([Text](#data-types), [optional](#field-tags)): Specifies the background color of the timetable, using a hexadecimal code (e.g., `"00FFFFFF"`).
- `DiagramSenColor` ([Text](#data-types), [required](#field-tags)): The color of the line in diagrams, defined as a hexadecimal code.
- `DiagramSenStyle` ([Enumeration](#data-types), [required](#field-tags)): The style of the line in diagrams. Possible values include:
  - `"SenStyle_Jissen"` (solid line)
  - `"SenStyle_Tensen"` (dashed line)
- `DiagramSenIsBold` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether the line should be displayed in bold.
- `StopMarkDrawType` ([Enumeration](#data-types), [optional](#field-tags)): Defines how stop marks are displayed. Possible values include:
  - `"EStopMarkDrawType_DrawOnStop"` (draw stop mark at station stops)
  - `"EStopMarkDrawType_DrawOnPass"` (draw stop mark at pass)
  - `"EStopMarkDrawType_Nothing"` (no stop mark).
- `ParentSyubetsuIndex` ([Number](#data-types), [optional](#field-tags)): Refers to the index of the parent train type. If this value is set, it means this train type is a variation of the parent. For example, `"ParentSyubetsuIndex=0"` means this train type is a variant of the train type with index 0.

#### Example

```oudia
Ressyasyubetsu.
Syubetsumei=各駅停車
Ryakusyou=各停
JikokuhyouMojiColor=00000000
JikokuhyouFontIndex=0
JikokuhyouBackColor=00FFFFFF
DiagramSenColor=00000000
DiagramSenStyle=SenStyle_Jissen
StopMarkDrawType=EStopMarkDrawType_DrawOnStop
.
Ressyasyubetsu.
Syubetsumei=各駅停車(支線)
Ryakusyou=支各停
JikokuhyouMojiColor=00000000
JikokuhyouFontIndex=0
JikokuhyouBackColor=00FFFFFF
DiagramSenColor=00000000
DiagramSenStyle=SenStyle_Ittensasen
StopMarkDrawType=EStopMarkDrawType_DrawOnStop
ParentSyubetsuIndex=0
.
Ressyasyubetsu.
Syubetsumei=急行
Ryakusyou=急行
JikokuhyouMojiColor=00FF0000
JikokuhyouFontIndex=0
JikokuhyouBackColor=00FFFFFF
DiagramSenColor=00FF0000
DiagramSenStyle=SenStyle_Jissen
DiagramSenIsBold=1
StopMarkDrawType=EStopMarkDrawType_DrawOnStop
.
```

### Dia Node

The **Dia Node** represents a timetable (ダイヤ) for the route. It holds scheduling information for different operating days, such as weekdays, weekends, or special holidays.

#### Attributes

- `DiaName` ([Text](#data-types), [required](#field-tags)): The name of the timetable, e.g., `"平日"` (weekday).
- `MainBackColorIndex` ([Number](#data-types), [optional](#field-tags)): Background color index for the main timetable, values between 0-3.
- `SubBackColorIndex` ([Number](#data-types), [optional](#field-tags)): Background color index for sub-timetables, values between 0-3.
- `BackPatternIndex` ([Number](#data-types), [optional](#field-tags)): Background pattern for the timetable. Possible values include:
  - `0` (solid color)
  - `1` (train type color)
  - `2` (vertical stripes)
  - `3` (horizontal stripes)
  - `4` (checkered pattern)

#### Children

The **Dia Node** can contain two types of child nodes:

- **Kudari Node**: Describes downward-bound trains.
- **Nobori Node**: Describes upward-bound trains.

Both the **Kudari** and **Nobori** nodes contain multiple **Ressya Nodes**, each of which holds detailed information about individual trains on the route.

### Ressya Node

The **Ressya Node** represents an individual train (列車) and contains attributes for its schedule and classification.

#### Attributes

- `Houkou` ([Enumeration](#data-types), [required](#field-tags)): The direction of the train, values are:
  - `"Kudari"` (downward)
  - `"Nobori"` (upward)
- `Syubetsu` ([Number](#data-types), [required](#field-tags)): The number corresponding to the train type defined in the **Ressyasyubetsu Node**.
- `Ressyabangou` ([Text](#data-types), [optional](#field-tags)): The train number.
- `Ressyamei` ([Text](#data-types), [optional](#field-tags)): The name of the train.
- `Gousuu` ([Text](#data-types), [optional](#field-tags)): The number of train cars.

#### Trailing Attributes

- `EkiJikoku` ([Text](#data-types), [optional](#field-tags)): The schedule of the train at various stations. This can follow several formats:
  - `""` (no service)
  - `"1"` (stops at the station)
  - `"2"` (does not pass through the station)
  - `"3"` (passes through the station without stopping)
  - `"1;HHMM/HHMM"` (departure and arrival times).

### DispProp Node

The **DispProp Node** defines the display properties for various elements of the timetable, including fonts and colors.

#### Attributes

- `JikokuhyouFont` ([Font](#data-types), [repeatable](#field-tags)): Specifies the font used for the timetable text. It should be repeated 8 (`CentDedRessyasyubetsu::JIKOKUHYOUFONT_COUNT`) times. If fewer than 8 are provided, the unspecified font properties will not be set, e.g., `PointTextHeight=9;Facename=Meiryo UI;Bold=1;Itaric=1`.
- `JikokuhyouVFont` ([Font](#data-types), [optional](#field-tags)): Specifies the vertical font used for the timetable text, e.g. `JikokuhyouVFont=PointTextHeight=9;Facename=@メイリオ`
- `DiaEkimeiFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used for station names in the diagram.
- `DiaMojiColor` ([Text](#data-types), [optional](#field-tags)): Specifies the color of the text on the timetable using a hexadecimal color code.
- `DiaHaikeiColor` ([Text](#data-types), [optional](#field-tags)): Specifies the background color of the timetable using a hexadecimal color code.
- `DiaRessyaColor` ([Text](#data-types), [optional](#field-tags)): Specifies the color of the train text in the diagram using a hexadecimal color code.
- `DiaJikuColor` ([Text](#data-types), [optional](#field-tags)): Specifies the color of the diagram axis using a hexadecimal color code.

#### References

- OuDiaSecond Ver2.06.14
  - `DiagramEdit/DiagramEdit/DedRosenFileData/CdDedDispProp.h`
  - `DiagramEdit/DiagramEdit/DedRosenFileData/CconvCdDedDispProp.cpp`

### WindowPlacement Node

#### Version

[OuDiaSecond Ver2.06.02+ (FileType=OuDiaSecond.1.12+)](http://oudiasecond.seesaa.net/article/483445182.html)

#### Attributes

- `RosenViewWidth` ([Number](#data-types), [required](#field-tags)): The width of the Route view.

### Attribute Field Properties

#### Field Tags

- `required`: Indicates that the field must be present in the node. Missing required fields will likely cause the file to be invalid or fail parsing.
- `optional`: Optional value that can be omitted if not applicable. If omitted, the parser will likely apply a default value or handle it gracefully.
- `repeatable`: Indicates that the field or node can appear multiple times within the same parent node. These fields can store multiple values or instances of the same data type.

#### Data Types

The following data types are for reference only and are not explicitly required. In practice, all values are treated as strings, with differentiation occurring during the parsing process.

The parenthesized types correspond to those used in the original OuDiaSecond C++ implementation and the current OuDia.Py Python implementation.

- Primitive Types
- `Text` (`tstring`, `str`): A string of characters, often representing a name, description, or identifier.
- `Number` (`int`, `int`): A numerical value, usually an integer, that can represent quantities, indices, or values like time.
- `Enumeration`: A predefined set of values from which only one can be chosen. These are typically used for fixed categories, like train types or station roles.
- `Boolean` (`bool`, `bool`): A binary value, represented by `0` (false) or `1` (true), used for toggle-type fields such as enabling or disabling certain behaviors or features. If omitted, it usually defaults to `0` (false).
- `Font` (`CdFontProp`, `str`): A list of font properties, separated by `;`. Includes sub-attributes such as:
  - `PointTextHeight` ([Number](#data-types)): The size of the text.
  - `Facename` ([Text](#data-types)): The name of the font, e.g., `"ＭＳ ゴシック"`.
  - `Bold` ([Boolean](#data-types), [optional](#field-tags)): Indicates if the text is bold.
  - `Italic` ([Boolean](#data-types), [optional](#field-tags)): Indicates if the text is italicized.

## References

### Bibliography

- [01397/clouddia/OuDiaFileMemo.rtf](https://github.com/01397/clouddia/blob/5325411cdccfd0d5c3c131a59adfe0e64a599c9e/OuDiaFileMemo.rtf)

### Links

- [OuDia](http://take-okm.a.la9.jp/oudia/)
- [OuDiaSecond](http://oudiasecond.seesaa.net/)
- [AOudia](https://kamelong.com/aodia/)
- [CloudDia](http://onemu.starfree.jp/clouddia/)
