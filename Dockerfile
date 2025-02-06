# ベースイメージとしてPython 3.9 slim を利用
FROM python:3.13-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存パッケージのコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY . .

# コンテナ起動時に実行するコマンド
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
