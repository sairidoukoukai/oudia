# OuDia/OuDiaSecond File Specification

This file is an unofficial specification of the OuDia/OuDiaSecond file format, which is used by their respective programs to create transportation system diagrams. This document has been compiled by analyzing files, existing implementations, and available documentation.

## BNF defintion

```bnf
<file> ::= <bom> <root_node> | <root_node>
<bom> ::= "\ufeff"

<root_node> ::= <entry_list>

<entry_list> ::= <entry> | <entry> <entry_list>

<entry> ::= <property> | <node>

<property> ::= <key> "=" <value> <newline>

<node> ::= <node_header> <entry_list> <node_footer>

<node_header> ::= <node_type> "." <newline>
<node_type> ::= "Rosen" | "Eki" | "Ressyasyubetsu" | "Dia" | "Kudari" | "EkiTrack2" | "DispProp" | ...

<node_footer> ::= "." <newline>

<key> ::= <camel_case_text>
<value> ::= <any_text>

<camel_case_text> ::= <capital_letter> <alphanumeric_text> | <capital_letter> <alphanumeric_text> <camel_case_text>

<capital_letter> ::= "A" | "B" | "C" | ... | "Z"
<alphanumeric_text> ::= <letter> | <letter> <alphanumeric_text> | <digit> | <digit> <alphanumeric_text>

<letter> ::= "a" | "b" | "c" | ... | "z" | <capital_letter>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

<any_text> ::= ε | <any_character> | <any_character>  <any_text>

<any_character> ::= ? Any Unicode Character ?

<newline> ::= <lf> | <crlf>
<crlf> ::= <cr> <lf>
<lf> ::= "\n"
<cr> ::= "\r"
```

## Structure Overview

An OuDia file (`.oud`) or OuDiaSecond file (`.oud2`) is a plain text file typically encoded in `UTF-8 BOM`. These files consist of multiple lines, typically separated by CRLF (`\r\n`). Each line represents part of a node, and all lines belong to one node or another. A specific set of lines are grouped into a node, with each node having a defined type.

The file itself (`<file>`) is represented as a root node (`<root_node>`), and all other nodes are child nodes of this root. Each child node begins with a header (`<node_header>`) in the format `Type.`, where `Type` represents the node type (<`node_type`>), and ends with a footer (`<node_footer>`), which is always `.`. The root node does not contain a header or footer but directly consists of entries.

### Node Structure

Each node (`<node>`) is a list of entries composed of one or more entries (`<entry>`). The list of entries is typically ordered in a specific way, depending on the node type. The entries allowed in each node are predefined, depending on the node type. Some nodes only have properties, while others only have node lists, or a combination of both. Some entries are optional, meaning they can be omitted. Each entry can be either of the following:

1. **Property** (`<property>`): A property is defined as a `Key=Value` pair, where `Key` is represented in CamelCase (`<key>`) and `Value` is the text representation of the attribute's value (`<value>`). Usually, the key is unique, meaning a node has only one entry with the same key. However, certain keys in specific node types (e.g., `JikokuhyouFont` in the `DispProp` node) may appear multiple times with the same or different values. In this case, it is treated as a list of values associated with the same key. The value can also be an empty string.
2. **Node List** (`<node_list>`): A node list is a sequence of nodes of the same type. It can have one or more items, and each item is a node with its own header, entries and footer. The node list has no special marking or identifier; it is represented by the concentration of nodes of the same type appearing sequentially. Sometimes there will be a container type (such as `EkiTrack2Cont`) that only holds children in a node list with no properties. Nodes can be nested through node lists.

### File Structure Example

```oud
FileType=OuDia.1.02
Rosen.                         # Rosen node begins
Rosenmei=Main Line             # Attribute for Rosen node
Eki.                           # Eki node begins
Ekimei=First Station           # Attribute for Eki node
Ekijikokukeisiki=Jikokukeisiki_Hatsu
Ekikibo=Ekikibo_Ippan
DownMain=0
UpMain=1
EkiTrack2Cont.                 # EkiTrack2Cont node begins
EkiTrack2.                     # EkiTrack2 child node begins
TrackName=1番線                # Attribute for EkiTrack2 node
TrackRyakusyou=1
.                              # EkiTrack2 child node ends
EkiTrack2.                     # Another EkiTrack2 child node begins
TrackName=2番線
TrackRyakusyou=2
.                              # EkiTrack2 child node ends
.                              # EkiTrack2Cont node ends
JikokuhyouJikokuDisplayKudari=0,1
JikokuhyouJikokuDisplayNobori=1,0
JikokuhyouSyubetsuChangeDisplayKudari=0,0,0,0,1
JikokuhyouSyubetsuChangeDisplayNobori=0,0,0,0,1
DiagramColorNextEki=0
JikokuhyouOuterDisplayKudari=0,0
JikokuhyouOuterDisplayNobori=0,0
.                              # Eki node ends
Ressyasyubetsu.                # Another child node of Rosen node begins
Syubetsumei=普通
JikokuhyouMojiColor=00000000
JikokuhyouFontIndex=0
.                              # Ressyasyubetsu node ends
.
```

### Fixed Order of Entries

The order of properties and node lists within each node is fixed and defined by the node type. For example:

- A [`Rosen` node](#rosen-node) will always begin with `Rosenmei` and other properties, followed by a list of [`Eki` nodes](#eki-node), then a list of [`Ressyasyubetsu` nodes](#ressyasyubetsu-node), a list of [`Dia` nodes](#dia) followed by any remaining properties.

To ensure best compatibility with OuDia/OuDiaSecond and other editor, parser or converter software, it is recommended to strictly maintain the order of entries. This hierarchical structure, combined with the fixed order of attributes and node lists, allows for the efficient representation of complex timetable data in a structured and easily readable format.

## Node Types

### Root Node

The **root node** represents the entire file. It contains various attributes that define metadata about the file and serves as the top-level container for all the other nodes. This node does not have a header (`Type.`) or footer (`.`), unlike the other nodes.

#### Entries

- `FileType` ([Text](#data-types), [required](#field-tags)): Specifies the version of the file format, for example, "OuDia.1.02". This may not necessarily be the same as the version of the program that generated the file.
- ([NodeList](#data-types)\[[Rosen](#rosen-node); 1\]): Represents a route or line.
- ([NodeList](#data-types)\[[DispProp](#dispprop-node); 1\]): Contains display properties like font styles and colors used in diagrams.
- ([NodeList](#data-types)\[[WindowPlacement](#windowplacement-node)\]): Contains window view positions.
- `FileTypeAppComment` ([Text](#data-types), [optional](#field-tags)): Additional comments related to the file type or application, possibly detailing the version of the application or any specific information.

### Rosen Node

The **Rosen Node** represents a single route or line in the transportation system (路線). This node contains attributes describing the route and can have child nodes that describe the stations (Eki), train types (Ressyasyubetsu), and timetables (Dia).

#### Entries

- `Rosenmei` ([Text](#data-types), [required](#field-tags)): The name of the route (路線名), e.g., "東急東横線".
- `KudariDiaAlias` ([Text](#data-types), [optional](#field-tags)): Alias for the "Kudari" (下り) direction (downward route). [OuDiaSecond.1.04+](http://oudiasecond.seesaa.net/article/459366976.html)
- `NoboriDiaAlias` ([Text](#data-types), [optional](#field-tags)): Alias for the "Nobori" (上り) direction (upward route). [OuDiaSecond.1.04+](http://oudiasecond.seesaa.net/article/459366976.html)
- ([NodeList](#data-types)\[[Eki Node](#eki-node)\]): Represents individual stations on the route. Multiple Eki nodes can be listed.
- ([NodeList](#data-types)\[[Ressyasyubetsu Node](#ressyasyubetsu-node)\]): Describes the types of trains that run on the route.
- ([NodeList](#data-types)\[[Dia Node](#dia-node)\]): Contains timetable data for different days or schedules (e.g., weekdays, weekends).
- `KitenJikoku` ([Text](#data-types), [optional](#field-tags)): The starting time of the route's operation, e.g., "400" for 4:00 AM.
- `DiagramDgrYZahyouKyoriDefault` ([Number](#data-types), [optional](#field-tags)): Default Y-coordinate distance between stations in diagrams.
- `EnableOperation` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether operational functionality is enabled. [OuDiaSecond.1.03+](http://oudiasecond.seesaa.net/article/457223251.html)
- `OperationCrossKitenJikoku` ([Number](#data-types), [optional](#field-tags)): Indicates whether connecting operations across the diagram start time is enabled. [OuDiaSecond.1.10+](http://oudiasecond.seesaa.net/article/481081211.html)
- `KijunDiaIndex` ([Number](#data-types), [optional](#field-tags)): Reference diagram index.
- `Comment` ([Text](#data-types), [optional](#field-tags)): Any comments regarding the route, such as service notes or special instructions.

### Eki Node

The **Eki Node** represents a station (駅) on the route. It provides information about the station’s name, its timetable style, and its operational role.

#### Entries

- `Ekimei` ([Text](#data-types), [required](#field-tags)): The name of the station, e.g., "四日市". Previously, empty station name was invalid, but will not throw errors now.
- `EkimeiJikokuRyaku` ([Text](#data-types), [optional](#field-tags)): The abbreviation for the station name used in the timetable view, specifically for start and terminal stations. If empty, the full station name is used. [OuDiaSecond.1.07+](http://oudiasecond.seesaa.net/article/467843165.html)
- `EkimeiDiaRyaku` ([Text](#data-types), [optional](#field-tags)): The abbreviation for the station name used in operational diagrams. If empty, the first character of the station name is used.
- `Ekijikokukeisiki` ([Enumeration](#data-types), [required](#field-tags)): The type of timetable associated with the station. Possible values include:
  - `"Jikokukeisiki_Hatsu"` (departure only)
  - `"Jikokukeisiki_Hatsuchaku"` (both arrival and departure)
  - `"Jikokukeisiki_KudariChaku"` (arrival for downward trains)
  - `"Jikokukeisiki_NoboriChaku"` (arrival for upward trains)
- `Ekikibo` ([Enumeration](#data-types), [required](#field-tags)): The station's classification based on its importance. Possible values include:
  - `"Ekikibo_Syuyou"` (major station)
  - `"Ekikibo_Ippan"` (general station)
- <s>`Kyoukaisen`</s> ([Boolean](#data-types), [optional](#field-tags), [deprecated](#field-tags)): Specifies if the station is part of a boundary line between two jurisdictions. Removed since [OuDiaSecond Ver1.02](http://oudiasecond.seesaa.net/article/454143826.html).
- `DiagramRessyajouhouHyoujiKudari` ([Enumeration](#data-types), [optional](#field-tags)): Controls the display of timetable information for downward-bound trains. Possible values include:
  - `DiagramRessyajouhouHyouji_Origin` (only show starting stations, default)
  - `"DiagramRessyajouhouHyouji_Anytime"` (always displayed)
  - `"DiagramRessyajouhouHyouji_Not"` (not displayed)
- `DiagramRessyajouhouHyoujiNobori` ([Enumeration](#data-types), [optional](#field-tags)): Controls the display of timetable information for upward-bound trains. Possible values include:
  - `DiagramRessyajouhouHyouji_Origin` (only show starting stations, default)
  - `"DiagramRessyajouhouHyouji_Anytime"` (always displayed)
  - `"DiagramRessyajouhouHyouji_Not"` (not displayed)
- `DownMain` ([Number](#data-types), [optional](#field-tags)): The main platform for downward trains.
- `UpMain` ([Number](#data-types), [optional](#field-tags)): The main platform for upward trains.
- `BrunchCoreEkiIndex` ([Number](#data-types), [optional](#field-tags)): Index of the core station in branching station settings. `-1` if not applicable.
- `BrunchOpposite` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether the branch is opposite the core station.
- `LoopOriginEkiIndex` ([Number](#data-types), [optional](#field-tags)): Index of the origin station for loop settings. `-1` if not applicable.
- `LoopOpposite` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether the loop is in the opposite direction.
- `JikokuhyouTrackDisplayKudari` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether the departure track is displayed for downward trains.
- `JikokuhyouTrackDisplayNobori` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether the departure track is displayed for upward trains.
- `NextEkiDistance` ([Number](#data-types), [optional](#field-tags)): Specifies the distance to the next station in seconds. Defaults to 0, meaning the default distance is used.
- `JikokuhyouTrackOmit` ([Boolean](#data-types), [optional](#field-tags)): Indicates whether the track display is omitted for the station.
- `JikokuhyouTrackDisplayKudari` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether track display is enabled for downward trains in the timetable.
- `JikokuhyouTrackDisplayNobori` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether track display is enabled for upward trains in the timetable.
- `DiagramTrackDisplay` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether track display is enabled in the diagram.
- ([NodeList](#data-types)\[[EkiTrack2 Node](#eki-track2-node)\]): (optional, [repeatable](#field-tags)) Represents the track layout of the station, including the track names, abbreviations, and configurations for upward and downward directions.
- ([NodeList](#data-types)\[[OuterTerminal Node](#outer-terminal-node)\]): (optional, [repeatable](#field-tags)) Represents outer terminals that are connected to the station but belong to another line.
- `OuterTerminalEkimei` ([Text](#data-types), [optional](#field-tags)): Represents outer terminals connected to the station.
- `NextEkiDistance` ([Number](#data-types), [optional](#field-tags)): The distance to the next station in seconds.
- `JikokuhyouTrackOmit` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to omit track display in the timetable.
- `JikokuhyouOperationOrigin` ([Number](#data-types), [optional](#field-tags)): Specifies the number of operation columns at the origin side of the station in the timetable.
- `JikokuhyouOperationTerminal` ([Number](#data-types), [optional](#field-tags)): Specifies the number of operation columns at the terminal side of the station in the timetable.
- `JikokuhyouOperationOriginDownBeforeUpAfter` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display coupling and decoupling operations at the origin side for downward trains.
- `JikokuhyouOperationOriginDownAfterUpBefore` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display coupling and decoupling operations at the origin side for upward trains.
- `JikokuhyouOperationTerminalDownBeforeUpAfter` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display coupling and decoupling operations at the terminal side for downward trains.
- `JikokuhyouOperationTerminalDownAfterUpBefore` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display coupling and decoupling operations at the terminal side for upward trains.
- `JikokuhyouJikokuDisplayKudari` ([Tuple](#data-types)\[[Boolean](#data-types), [Boolean](#data-types)\], [optional](#field-tags)): Specifies whether to display arrival and departure times for downward trains in the customized timetable view. The first value corresponds to arrival time, and the second corresponds to departure time.
- `JikokuhyouJikokuDisplayNobori` ([Tuple](#data-types)\[[Boolean](#data-types), [Boolean](#data-types)\], [optional](#field-tags)): Specifies whether to display arrival and departure times for upward trains in the customized timetable view. The first value corresponds to arrival time (`JikokuhyouChakuJikokuDisplayKudari`), and the second corresponds to departure time (`JikokuhyouHatsuJikokuDisplayKudari`).
- `JikokuhyouSyubetsuChangeDisplayKudari` ([Tuple](#data-types)\[[Integer](#data-types), [Integer](#data-types)\, [Integer](#data-types)\, [Integer](#data-types)\, [Integer](#data-types)\], [optional](#field-tags)): Specifies how to display train type changes for downward trains in the timetable. The values correspond to the following:
  - `JikokuhyouRessyabangouDisplayKudari`: Specifies how train numbers are displayed.
  - `JikokuhyouOperationNumberDisplayKudari`: Specifies how operation numbers are displayed.
  - `JikokuhyouRessyaSyubetsuDisplayKudari`: Specifies how train categories are displayed.
  - `JikokuhyouRessyameiDisplayKudari`: Specifies how train names and numbers are displayed.
  - `JikokuhyouOperationNumberDisplayRowsKudari`: Specifies how many rows are used for operation numbers.
- `JikokuhyouSyubetsuChangeDisplayNobori` ([Tuple](#data-types)\[[Integer](#data-types), [Integer](#data-types)\, [Integer](#data-types)\, [Integer](#data-types)\, [Integer](#data-types)\], [optional](#field-tags)): Specifies how to display train type changes for upward trains in the timetable. The values correspond to the following:
  - `JikokuhyouRessyabangouDisplayNobori`: Specifies how train numbers are displayed.
  - `JikokuhyouOperationNumberDisplayNobori`: Specifies how operation numbers are displayed.
  - `JikokuhyouRessyaSyubetsuDisplayNobori`: Specifies how train categories are displayed.
  - `JikokuhyouRessyameiDisplayNobori`: Specifies how train names and numbers are displayed.
  - `JikokuhyouOperationNumberDisplayRowsNobori`: Specifies how many rows are used for operation numbers.
- `JikokuhyouOuterDisplayKudari` ([Tuple](#data-types)\[[Boolean](#data-types), [Boolean](#data-types)\], [optional](#field-tags)): Specifies whether to display outer-terminal information for downward trains. The first value corresponds to the first departure (`JikokuhyouOuterSihatsuDisplayKudari`), and the second corresponds to the last arrival (`JikokuhyouOuterShuchakuDisplayKudari`).
- `JikokuhyouOuterDisplayNobori` ([Tuple](#data-types)\[[Boolean](#data-types), [Boolean](#data-types)\]): Specifies whether to display outer-terminal information for upward trains. The first value corresponds to the first departure (`JikokuhyouOuterSihatsuDisplayNobori`), and the second corresponds to the last arrival (`JikokuhyouOuterShuchakuDisplayNobori`).
- `JikokuhyouOuterDisplayKudari` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display outer-terminal information for downward trains.
- `JikokuhyouOuterDisplayNobori` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display outer-terminal information for upward trains.
- `DiagramColorNextEki` ([Number](#data-types), [optional](#field-tags)): Specifies the color for the next station in the diagram.
- `OperationTableDisplayJikoku` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display times in the operation table.
- `CrossingCheckRule` ([Custom](#data-types), [optional](#field-tags)): Specifies the rules for crossing checks

#### References

- OuDiaSecond Ver2.06.14
  - `DiagramEdit/DiagramEdit/entDed/CconvCentDedOud.cpp`
  - `DiagramEdit/DiagramEdit/entDed/CentDedEki.h`

### Ressyasyubetsu Node

The **Ressyasyubetsu Node** describes the types of trains that operate on the route (列車種別). Each train type has attributes for its display color and style on both diagrams and timetables.

#### Entries

- `Syubetsumei` ([Text](#data-types), [required](#field-tags)): The name of the train type, e.g., "通勤特急" (commuter express).
- `Ryakusyou` ([Text](#data-types), [optional](#field-tags)): The abbreviation used for the train type.
- `JikokuhyouMojiColor` ([Color](#data-types), [required](#field-tags)): The color used for displaying the train type on timetables, represented as a hexadecimal color code (e.g., `"000000FF"` for blue).
- `JikokuhyouFontIndex` ([Number](#data-types), [required](#field-tags)): The font index used for displaying the train type on timetables.
- `JikokuhyouBackColor` ([Color](#data-types), [optional](#field-tags)): Specifies the background color of the timetable, using a hexadecimal code (e.g., `"00FFFFFF"`).
- `DiagramSenColor` ([Color](#data-types), [required](#field-tags)): The color of the line in diagrams, defined as a hexadecimal code.
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

#### Entries

- `DiaName` ([Text](#data-types), [required](#field-tags)): The name of the timetable, e.g., `"平日"` (weekday).
- `MainBackColorIndex` ([Number](#data-types), [optional](#field-tags)): Background color index for the main timetable, values between 0-3.
- `SubBackColorIndex` ([Number](#data-types), [optional](#field-tags)): Background color index for sub-timetables, values between 0-3.
- `BackPatternIndex` ([Number](#data-types), [optional](#field-tags)): Background pattern for the timetable. Possible values include:
  - `0` (solid color)
  - `1` (train type color)
  - `2` (vertical stripes)
  - `3` (horizontal stripes)
  - `4` (checkered pattern)
- ([NodeList](#data-types)\[[Kudari Node](#kudari-node)\]): Represents downward-bound trains on the route.
- ([NodeList](#data-types)\[[Nobori Node](#nobori-node))\]): Represents upward-bound trains on the route.

### Ressya Node

The **Ressya Node** represents an individual train (列車) and contains attributes for its schedule and classification.

#### Entries

- `Houkou` ([Enumeration](#data-types), [required](#field-tags)): The direction of the train, values are:
  - `"Kudari"` (downward)
  - `"Nobori"` (upward)
- `Syubetsu` ([Number](#data-types), [required](#field-tags)): The number corresponding to the train type defined in the **Ressyasyubetsu Node**.
- `Ressyabangou` ([Text](#data-types), [optional](#field-tags)): The train number.
- `Ressyamei` ([Text](#data-types), [optional](#field-tags)): The name of the train.
- `Gousuu` ([Text](#data-types), [optional](#field-tags)): The number of train cars.
- `EkiJikoku` ([Text](#data-types), [optional](#field-tags)): The schedule of the train at various stations. This can follow several formats:
  - `""` (no service)
  - `"1"` (stops at the station)
  - `"2"` (does not pass through the station)
  - `"3"` (passes through the station without stopping)
  - `"1;HHMM/HHMM"` (departure and arrival times).

### DispProp Node

The **DispProp Node** defines the display properties for various elements of the timetable, including fonts and colors.

#### Entries

- `JikokuhyouFont` ([Font](#data-types), [repeatable](#field-tags)): Specifies the font used for the timetable text. This attribute should be repeated 8 times(`CentDedRessyasyubetsu::JIKOKUHYOUFONT_COUNT`). If fewer than 8 values are provided, the remaining fonts will not be set. Example: `PointTextHeight=9;Facename=Meiryo UI;Bold=1;Itaric=1`.
- `JikokuhyouVFont` ([Font](#data-types), [optional](#field-tags)): Specifies the vertical font used for the timetable text. Example: `JikokuhyouVFont=PointTextHeight=9;Facename=@メイリオ`.
- `DiaEkimeiFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used for station names in the diagram.
- `DiaJikokuFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used for displaying time in the diagram.
- `DiaRessyaFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used for the train text in the diagram.
- `OperationTableFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used in the operation table.
- `AllOperationTableJikokuFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used for displaying time in the operation table.
- `CommentFont` ([Font](#data-types), [optional](#field-tags)): Specifies the font used for comments.
- `DiaMojiColor` ([Color](#data-types), [optional](#field-tags)): Specifies the color of the text on the timetable using a hexadecimal color code. Example: `000000` (for black).
- `DiaHaikeiColor` ([Color](#data-types), [optional](#field-tags)): Specifies the background color of the timetable using a hexadecimal color code.
- `DiaRessyaColor` ([Color](#data-types), [optional](#field-tags)): Specifies the color of the train lines in the diagram using a hexadecimal color code.
- `DiaJikuColor` ([Color](#data-types), [optional](#field-tags)): Specifies the color of the axis in the using a hexadecimal color code.
- `JikokuhyouBackColor` ([Color](#data-types), [optional](#field-tags), [repeatable](#field-tags)): Specifies the background color for the timetable's outer area. This attribute is repeatable 4 times for different layers.
- `StdOpeTimeLowerColor` ([Color](#data-types), [optional](#field-tags)): Specifies the background color for operation times that are below the standard.
- `StdOpeTimeHigherColor` ([Color](#data-types), [optional](#field-tags)): Specifies the background color for operation times that exceed the standard.
- `StdOpeTimeUndefColor` ([Color](#data-types), [optional](#field-tags)): Specifies the background color for undefined operation times.
- `StdOpeTimeIllegalColor` ([Color](#data-types), [optional](#field-tags)): Specifies the background color for illegal operation times.
- `OperationStringColor` ([Color](#data-types), [optional](#field-tags)): Specifies the color of the text in the operation table.
- `OperationGridColor` ([Color](#data-types), [optional](#field-tags)): Specifies the color of the grid in the operation table.
- `EkimeiLength` ([Number](#data-types), [optional](#field-tags)): Specifies the width of the station name column, in terms of full-width characters. Default is 6, with a range of 1 to 29.
- `JikokuhyouRessyaWidth` ([Number](#data-types), [optional](#field-tags)): Specifies the width of the train column in the timetable. Default is 5, with a range of 4 to 255.
- `AnySecondIncDec1` ([Number](#data-types), [optional](#field-tags)): Specifies the increment/decrement value in seconds for the first custom time adjustment. Default is 5, with a range of 1 to 60.
- `AnySecondIncDec2` ([Number](#data-types), [optional](#field-tags)): Specifies the increment/decrement value in seconds for the second custom time adjustment. Default is 15, with a range of 1 to 60.
- `DisplayRessyamei` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display the train name and number in the timetable view. Default is true.
- `DisplayOuterTerminalEkimeiOriginSide` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display the outer terminal station name on the origin side. Default is true.
- `DisplayOuterTerminalEkimeiTerminalSide` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display the outer terminal station name on the terminal side. Default is true.
- `DiagramDisplayOuterTerminal` ([Number](#data-types), [optional](#field-tags)): Specifies how outer terminal station names and operation numbers are displayed in the diagram. Possible values:
  - `0`: Station name + operation number (default)
  - `1`: Station name only
  - `2`: Operation number only
  - `3`: None
- `SecondRoundChaku` ([Number](#data-types), [optional](#field-tags)): Specifies how to handle arrival times when seconds are hidden. Possible values:
  - `0`: Truncate (default)
  - `1`: Round (round up if 30 seconds or more)
  - `2`: Always round up
- `SecondRoundHatsu` ([Number](#data-types), [optional](#field-tags)): Specifies how to handle departure times when seconds are hidden. Possible values:
  - `0`: Truncate (default)
  - `1`: Round (round up if 30 seconds or more)
  - `2`: Always round up
- `Display2400` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display 2400 for midnight in the timetable. Default is false.
- `OperationNumberRows` ([Number](#data-types), [optional](#field-tags)): Specifies the number of rows for operation numbers in the timetable. Default is 1, with a range of 1 to 5.
- `DisplayInOutLinkCode` ([Boolean](#data-types), [optional](#field-tags)): Specifies whether to display the in/out link code column in the timetable. Default is true.

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
- `deprecated`: Indicates that the value may be or has already abandonded by later versions.

#### Data Types

The following data types are for reference only and are not explicitly required. In practice, all values are treated as strings, with differentiation occurring during the parsing process.

The parenthesized types correspond to those used in the original OuDiaSecond C++ implementation and the current OuDia.Py Python implementation.

- Primitive Types
- `Text` (`tstring`, `str`): A string of characters, often representing a name, description, or identifier.
- `Number` (`int`, `int`): A numerical value, usually an integer, that can represent quantities, indices, or values like time.
- `Enumeration`: A predefined set of values from which only one can be chosen. These are typically used for fixed categories, like train types or station roles.
- `Boolean` (`bool`, `bool`): A binary value, represented by `0` (false) or `1` (true), used for toggle-type fields such as enabling or disabling certain behaviors or features. If omitted, it usually defaults to `0` (false).
- `Tuple` (multiple variables, `str`): A series of values with fixed amount of elements separated by `,` as a string.
- `Dictionary` (? , `str`): A series of key value pairs separated by `;` <!-- TODO: Check how is it implemented in CPP -->
- `NodeList` (`CDirectory`, `Children`): A list of child nodes.
- `Color` (`CdFontColor`, `str`): A hexadecimal string representing an RGB color.
- `Font` (`CdFontProp`, `str`): A list of font properties, separated by `;`. Includes sub-attributes such as:
  - `PointTextHeight` ([Number](#data-types)): The size of the text.
  - `Facename` ([Text](#data-types)): The name of the font, e.g., `"ＭＳ ゴシック"`.
  - `Bold` ([Boolean](#data-types), [optional](#field-tags)): Indicates if the text is bold.
  - `Itaric` ([Boolean](#data-types), [optional](#field-tags)): Indicates if the text is italicized. `Itaric` (sic) is a misspelling of "Italic".

## References

### Bibliography

- [01397/clouddia/OuDiaFileMemo.rtf](https://github.com/01397/clouddia/blob/5325411cdccfd0d5c3c131a59adfe0e64a599c9e/OuDiaFileMemo.rtf)

### Links

- [OuDia](http://take-okm.a.la9.jp/oudia/)
- [OuDiaSecond](http://oudiasecond.seesaa.net/)
- [AOudia](https://kamelong.com/aodia/)
- [CloudDia](http://onemu.starfree.jp/clouddia/)
