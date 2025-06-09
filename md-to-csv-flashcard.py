import re
import sys
from enum import Enum


class Notetype(Enum):
    BASIC = 1
    REVERSED = 2


# What card backs could contain
class Linetype(Enum):
    NONE = 1
    NONE_UL = 2
    OL = 3
    P = 4
    UL = 5


class Card:
    def __init__(
        self,
        front: str = "",
        back_lines: list[str] = [],
        notetype: Notetype = Notetype.BASIC,
    ) -> None:
        self.notetype = notetype
        self.front = front
        self.set_back_lines(back_lines)

    def __get_line_type_close(self, line_type: Linetype) -> str:
        if line_type == Linetype.NONE_UL or line_type == Linetype.UL:
            return "</ul>"
        elif line_type == Linetype.OL:
            return "</ol>"
        return ""

    def __get_notetype_str(self) -> str:
        if self.notetype == Notetype.REVERSED:
            return "Basic (and reversed card)"
        return "Basic"

    def __sanitize_str(self, string: str) -> str:
        return (
            string.replace('"', '""')
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("&", "&amp;")
        )

    def __str__(self):
        return f'"{self.front}","{self.back}",{self.__get_notetype_str()}\n'

    def set_back_lines(self, back_lines: list[str]):
        back_list: list[str] = []
        line_type = Linetype.NONE

        for line in back_lines:
            # None-styled unordered list
            none_ul_start = re.search(r"^-\s.*:", line)
            if none_ul_start:
                if line_type != Linetype.NONE_UL:
                    back_list.append(self.__get_line_type_close(line_type))
                    back_list.append('<ul style=""list-style-type:none;"">')
                line_type = Linetype.NONE_UL
                back_list.append(
                    f"<li><strong>{self.__sanitize_str(none_ul_start.group(0)[1:].strip())}</strong>"
                )
                back_list.append(
                    f"{self.__sanitize_str(line[none_ul_start.end():].strip())}</li>"
                )
            # Unordered list
            elif re.search(r"^-\s", line):
                if line_type != Linetype.UL:
                    back_list.append(self.__get_line_type_close(line_type))
                    back_list.append("<ul>")
                line_type = Linetype.UL
                back_list.append(f"<li>{self.__sanitize_str(line[1:].strip())}</li>")
            # Ordered list
            elif re.search(r"^\d\.", line):
                if line_type != Linetype.OL:
                    back_list.append(self.__get_line_type_close(line_type))
                    back_list.append("<ol>")
                line_type = Linetype.OL
                back_list.append(f"<li>{self.__sanitize_str(line[2:].strip())}</li>")
            # Paragraph
            else:
                if line_type != Linetype.P:
                    back_list.append(self.__get_line_type_close(line_type))
                line_type = Linetype.P
                back_list.append(f"<p>{self.__sanitize_str(line.strip())}</p>")

        back_list.append(self.__get_line_type_close(line_type))
        self.back = "".join(back_list)


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print(f"USAGE: {sys.argv[0]} <input file> [output file]")

input_file = sys.argv[1]

if len(sys.argv) == 3:
    output_file = sys.argv[2]
else:
    output_file = "out.csv"

have_front = False
front = ""
back_lines: list[str] = []
cards: list[Card] = []

with open(input_file, "r") as inf:
    for line in inf:
        # Skip blank lines
        if len(line.strip()) == 0:
            continue

        # Front
        if (len(line) > 0 and line[0] == "#") and (len(line) == 1 or line[1] != "#"):
            if have_front:
                cards.append(Card(front, back_lines))
            have_front = True
            front = line[1:].strip()
            back_lines.clear()

        # Back
        elif have_front:
            back_lines.append(line)

    cards.append(Card(front, back_lines))

with open(output_file, "w") as outf:
    card_strings: list[str] = []
    for card in cards:
        card_strings.append(str(card))
    outf.write("#separator:comma\n")
    outf.write("#html:true\n")
    outf.write("#notetype:Basic\n")
    outf.write("#notetype column:3\n")
    outf.writelines(card_strings)
