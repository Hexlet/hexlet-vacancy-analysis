import re


class LineParser:
    @staticmethod
    def extract_value(line):
        parts = re.split(r"[:\-\u2014]", line, maxsplit=1)
        return parts[1].strip() if len(parts) > 1 else line.strip()

    @staticmethod
    def extract_salary(line, keywords):
        cleaned_line = line
        for kw in keywords:
            cleaned_line = re.sub(kw, "", cleaned_line, flags=re.IGNORECASE)
        match = re.search(r"(от\s*)?\d[\d\s.,]{3,}", cleaned_line.lower())
        return match.group().strip() if match else None

    @staticmethod
    def extract_phone(line):
        match_username = re.search(r"@\w+", line)
        if match_username:
            return match_username.group()
        match_phone = re.search(
            r"""(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]
?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}""",
            line,
        )
        return match_phone.group() if match_phone else None

    @staticmethod
    def extract_link(line):
        match = re.search(r"https?://[^\s]+|t\.me/[^\s]+", line)
        return match.group() if match else None
