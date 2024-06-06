import re
from typing import List


splits = {
    "，",
    "。",
    "？",
    "！",
    ",",
    ".",
    "?",
    "!",
    "~",
    ":",
    "：",
    "—",
    "…",
}


def cut5(inp: str):
    """Cut one line of text into pieces."""
    items = re.split(f"([{''.join(splits)}])", inp)
    if items[-1] == "":
        items = items[:-1]
    if len(items) % 2 == 1:
        items.append(".")

    mergeitems: List[str] = [items[0]]
    for item in items[1:]:
        if item == "":
            continue
        if item not in splits:
            mergeitems.append(item)
        else:
            mergeitems[-1] += item

    return mergeitems


def merge_short_texts(texts: List[str], threshold: int = 6):
    """Merge short texts to longer ones. Texts are generated by cut5."""
    result: List[str] = []
    text = ""
    for ele in texts:
        text += ele
        if len(text) >= threshold:
            result.append(text)
            text = ""
    if text:
        result.append(text)
    return result


def clean_and_cut_text(text: str) -> List[str]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    texts = [
        merged.strip()
        for line in lines
        for merged in merge_short_texts(cut5(line))
        if not all(char in splits for char in merged.strip())
    ]
    texts = ["." + text if len(text) < 5 else text for text in texts]
    return texts