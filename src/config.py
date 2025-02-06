# src/config.py

# 高頻度フィード（毎分更新）
HIGH_FREQ_FEEDS = {
    "天気概況": "https://www.data.jma.go.jp/developer/xml/feed/regular.xml",
    "警報・注意報": "https://www.data.jma.go.jp/developer/xml/feed/extra.xml",
    "地震・火山": "https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml",
    "その他": "https://www.data.jma.go.jp/developer/xml/feed/other.xml",
}

# 長期フィード（毎時更新）
LONG_TERM_FEEDS = {
    "天気概況": "https://www.data.jma.go.jp/developer/xml/feed/regular_l.xml",
    "警報・注意報": "https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml",
    "地震・火山": "https://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml",
    "その他": "https://www.data.jma.go.jp/developer/xml/feed/other_l.xml",
}
