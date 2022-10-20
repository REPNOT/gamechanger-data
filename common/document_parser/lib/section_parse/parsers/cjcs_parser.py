from re import compile, finditer, sub, search, IGNORECASE, VERBOSE, Pattern
from os.path import splitext
from typing import List, Union
from .parser_definition import ParserDefinition
from .utils import (
    next_letter,
    CAPITAL_ENCLOSURE,
    DD_MONTHNAME_YYYY,
)


class CJCSParser(ParserDefinition):
    """Section parser for CJCS document types.

    Child of ParserDefinition.
    """

    SUPPORTED_DOC_TYPES = ["cjcsi", "cjcsm", "cjcsn", "cjcs gde"]

    # Pattern to identify the start of a responsibilities section that is an
    # enclosure.
    ENCLOSURE_RESPONSIBILITIES_START_PATTERN = compile(
        r"""
        \b
        E(?:nclosure|NCLOSURE)
        [ ]
        ([A-Z])
        [ \n]*
        [a-zA-Z0-9,:'/";\(\)]*?
        R(?:esponsibilities|ESPONSIBILITIES)
        \b
        """,
        flags=VERBOSE,
    )

    # Pattern to identify the start of a responsibilities section that is part
    # of a numbered list.
    NUMBERED_RESPONSIBILITIES_START_PATTERN = compile(
        r"""
            [\n]\s*
            ([0-9]+)                                # First capture group: 1 or more digits.
                                                    # The number that this item is in the list.
            \.\s*
            .*?                                     # Non-greedy match for any characters. 
                                                    # Note: we don't need to specify the maximum
                                                    # number of characters b/c the DOTALL flag
                                                    # is not being used, and therefore the 
                                                    # maximum number of characters is limited 
                                                    # by the length of the line of text.
            R(?:esponsibilities|ESPONSIBILITIES) 
            \b
        """,
        flags=VERBOSE,
    )

    # Pattern to identify the start of a purpose section that is part of a
    # numbered list.
    NUMBERED_PURPOSE_START_PATTERN = compile(
        rf"""
            [\n][\s]*([0-9])+[ ]?\.[ ]+             # Numbered list formatting
            P(?:urpose|URPOSE)
            [ ]?
            \.?
            [ ]+
            (?!of)                                  # Don't match "of" after "Purpose" b/c
                                                    # there are sections like 
                                                    # "Purpose of [organization]" which are
                                                    # not the document's main purpose section.
        """,
        flags=VERBOSE,
    )

    def __init__(self, doc_dict: dict, test_mode: bool = False):
        super().__init__(doc_dict, test_mode)
        self._text = self.get_raw_text()
        self._filename_without_extension = splitext(self._filename)[0]

        # Keys are (str) enclosure letter, values are (Tuple[int|None, int|None])
        # start and end indices of the corresponding enclosures.
        self._enclosure_spans = {}

    @property
    def responsibilities(self):
        return (
            self._get_responsibilities_from_enclosures()
            + self._get_numbered_section(
                self.NUMBERED_RESPONSIBILITIES_START_PATTERN
            )
        )

    @property
    def purpose(self):
        return self._get_numbered_section(self.NUMBERED_PURPOSE_START_PATTERN)

    def _get_responsibilities_from_enclosures(self) -> List[str]:
        """Get all responsibilities enclosures from the document.

        Returns:
            List[str]: Each item in the list is a responsibilities enclosure.
        """
        result = []

        for match_ in finditer(
            self.ENCLOSURE_RESPONSIBILITIES_START_PATTERN, self._text
        ):
            letter = match_.groups()[0]
            start = match_.start()
            end = self._find_enclosure_end(letter, start)
            if end is None:
                self._logger.warning(
                    f"Could not find end point of `Enclosure {letter}` within "
                    f"`{self._filename_without_extension}. Cannot extract "
                    f"responsibilities section from that enclosure.`"
                )
                continue
            result.append(self._text[start:end])

        return [self._remove_pagebreaks_and_noise(x) for x in result]

    def _get_numbered_section(
        self, section_name: Union[str, Pattern], first_only: bool = False
    ) -> List[str]:
        """

        Args:
            section_name (Union[str, Pattern]): The name of the section to
                extract as a string (case sensitive), or a pre-compiled regex
                pattern.
            first_only (bool, optional): True to only extract the first
                instance of the section, False to extract all instances.
                Defaults to False.

        Returns:
            List[str]: Each item in the list is a section of the document.
        """
        number_pattern = rf"\n\s*([0-9])+[ ]?\.[ ]+"
        if isinstance(section_name, str):
            section_start_pattern = compile(
                rf"{number_pattern}{section_name}\b"
            )
        else:
            section_start_pattern = section_name

        enclosure_title_pattern = compile(
            self._make_enclosure_title_pattern(r"[A-Z]+")
        )

        if first_only:
            matches = [search(section_start_pattern, self._text)]
        else:
            matches = finditer(section_start_pattern, self._text)

        result = []
        patterns = [
            number_pattern,
            r"\n\s*G(?:lossary|LOSSARY)\s*\n",
            r"\n\s*[0-9]+\s*\n",
            r"\s*E(?:nclosures|NCLOSURES)\s*\n",
        ]


        for match_ in matches:
            start = match_.start()
            search_start = match_.end()
            next_match = None
            end = None

            for pattern in patterns:
                m = search(pattern, self._text[search_start:])
                if m:
                    if end is None or m.start() < end:
                        end = m.start()
                        next_match = m

            if next_match:
                text = self._text[start : search_start + end]
                # If the next list item is number 1, it could be part of the next
                # enclosure. If it is, then cut off the text before the next
                # enclosure title.
                if next_match.groups() and next_match.groups()[0] == "1":
                    enclosure_titles = list(
                        finditer(enclosure_title_pattern, text)
                    )
                    if len(enclosure_titles) >= 2:
                        first_enclosure = enclosure_titles[0].groups()[0]
                        for title in enclosure_titles[1:]:
                            if title.groups()[0] != first_enclosure:
                                text = text[: title.start()]
                                break
                result.append(text)
            else:
                self._logger.warning(
                    "Could not find next numbered section. Current num: "
                    f"{match_.groups()[0]}. Start index: {start}."
                )

        return [self._remove_pagebreaks_and_noise(x) for x in result]

    def _find_enclosure_end(
        self, enclosure_letter: str, start: int
    ) -> Union[int, None]:
        """Find the end index of an enclosure within `_text`.

        Adds the span to object's `_enclosure_spans` if it does not exist yet.

        Args:
            enclosure_letter (str): Letter of the enclosure (e.g., "A" for
                Enclosure A).
            start (int): Start index of the enclosure within `_text`.

        Returns:
            Union[int, None]: If the end index is found, returns it as an int.
                Otherwise, returns None.
        """
        enclosure_letter = enclosure_letter.upper()

        if enclosure_letter in self._enclosure_spans:
            return self._enclosure_spans[enclosure_letter][1]

        try:
            end_letter = next_letter(enclosure_letter)
        except ValueError as e:
            self._logger.exception(
                f"Exception occurred within _get_enclosure_span(): {e}"
            )
            return None

        end = search(
            self._make_enclosure_title_pattern(end_letter), self._text[start:]
        )
        if not end:
            end = search(r"\n\s*G(?:lossary|LOSSARY)\s*\n", self._text[start:])

        if end:
            end = end.end() + start
            if enclosure_letter.isalpha():
                self._enclosure_spans[enclosure_letter] = (start, end)

        return end

    def _remove_pagebreaks_and_noise(self, text: str) -> str:
        """Remove page break text and noise from the given text.

        Example page break text that comes from document headers/ footers:
            CJCS Guide 3501
            5 May 2015
            UNCLASSIFIED
            A-1
            ENCLOSURE 1

        Args:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        start_pattern = r"\s*?\n"
        end_pattern = r"(?:\s*?(?=\n)|[ ]?$)"  # ?=\n allows matches to overlap on newline

        if "GDE" in self._filename_without_extension:
            filename_pattern = rf"(?:{self._filename_without_extension}|{self._filename_without_extension.replace('GDE', r'G(?:uide|UIDE)')})"
        else:
            filename_pattern = self._filename_without_extension

        for pattern in [
            filename_pattern,
            rf"{CAPITAL_ENCLOSURE} [A-Z]",
            r"[A-Z]{1,2}-[0-9]+",
            "UNCLASSIFIED",
            r"\(?INTENTIONALLY BLANK\)?",
        ]:
            text = sub(rf"{start_pattern}{pattern}{end_pattern}", "", text)

        text = sub(
            rf"{start_pattern}{DD_MONTHNAME_YYYY}{end_pattern}",
            "",
            text,
            flags=IGNORECASE | VERBOSE,
        )
        text = sub(r"\s+[0-9]+\.\s*$", "", text)

        return text.strip()

    def _make_enclosure_title_pattern(self, enclosure_letter: str):
        return rf"\n\s*{CAPITAL_ENCLOSURE} ({enclosure_letter})\.?\s*\n"