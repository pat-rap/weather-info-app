# src/rss_parser.py

import xml.etree.ElementTree as ET
from datetime import datetime

NAMESPACE = {'atom': 'http://www.w3.org/2005/Atom'}

def parse_rss(xml_data: str):
    """
    RSS (Atom形式) の XML を解析して、フィード情報とエントリのリストを返します。
    """
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        raise ValueError(f"XMLの解析に失敗しました: {e}") from e
    
    # Atom名前空間を考慮してタグを取得
    feed_title = root.findtext(f"{{{NAMESPACE['atom']}}}title", default="")
    feed_subtitle = root.findtext(f"{{{NAMESPACE['atom']}}}subtitle", default="")
    updated_text = root.findtext(f"{{{NAMESPACE['atom']}}}updated")
    
    if updated_text:
        try:
            # Python 3.7以上であれば、"+09:00"等のタイムゾーン付きISO8601をパース可能
            feed_updated = datetime.fromisoformat(updated_text)
        except ValueError:
            feed_updated = None
    else:
        feed_updated = None

    feed_info = {
        "feed_title": feed_title,
        "feed_subtitle": feed_subtitle,
        "feed_updated": feed_updated,  # datetime型または None
    }
    
    # エントリの解析
    entries = []
    entry_elements = root.findall(f"{{{NAMESPACE['atom']}}}entry")
    
    for entry in entry_elements:
        author_element = entry.find(f"{{{NAMESPACE['atom']}}}author")
        entry_author = ""
        if author_element is not None:
            entry_author = author_element.findtext(f"{{{NAMESPACE['atom']}}}name", default="")

        link_element = entry.find(f"{{{NAMESPACE['atom']}}}link")
        entry_link = link_element.attrib.get("href") if link_element is not None else None

        updated_entry_text = entry.findtext(f"{{{NAMESPACE['atom']}}}updated", default="")
        if updated_entry_text:
            try:
                entry_updated = datetime.fromisoformat(updated_entry_text)
            except ValueError:
                entry_updated = None
        else:
            entry_updated = None

        entry_data = {
            "entry_id_in_atom": entry.findtext(f"{{{NAMESPACE['atom']}}}id", default=""),
            "entry_title": entry.findtext(f"{{{NAMESPACE['atom']}}}title", default=""),
            "entry_updated": entry_updated,  # datetime型または None
            "entry_author": entry_author,
            "entry_link": entry_link,
            "entry_content": entry.findtext(f"{{{NAMESPACE['atom']}}}content", default=""),
            "inserted_at": datetime.utcnow(),  # データを格納したタイミングなどを付加する場合
        }
        entries.append(entry_data)

    return feed_info, entries
