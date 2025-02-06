# src/rss_parser.py

import xml.etree.ElementTree as ET
from datetime import datetime

def parse_rss(xml_data: str):
    """
    RSS (Atom形式) の XML を解析して、フィード情報とエントリのリストを返します。
    ※ 以下はサンプル実装。実際のフィード構造に合わせて調整してください。
    """
    root = ET.fromstring(xml_data)
    
    # フィード情報の取得
    feed_info = {
        "feed_title": root.findtext("title"),
        "feed_subtitle": root.findtext("subtitle"),
        "feed_updated": datetime.fromisoformat(root.findtext("updated")) if root.findtext("updated") else None,
        # 例：feed_id_in_atom や rights なども取得
    }
    
    # 各エントリの解析
    entries = []
    for entry in root.findall("entry"):
        entry_data = {
            "entry_id_in_atom": entry.findtext("id"),
            "entry_title": entry.findtext("title"),
            "entry_updated": datetime.fromisoformat(entry.findtext("updated")) if entry.findtext("updated") else None,
            "entry_author": entry.find("author").findtext("name") if entry.find("author") is not None else None,
            "entry_link": entry.find("link").attrib.get("href") if entry.find("link") is not None else None,
            "entry_content": entry.findtext("content"),
            "inserted_at": datetime.utcnow(),
        }
        entries.append(entry_data)
    
    return feed_info, entries
