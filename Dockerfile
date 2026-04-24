# ベースイメージを指定（Python3.11が入った環境を使う）
FROM public.ecr.aws/docker/library/python:3.11
# コンテナ内の作業ディレクトリを /app に設定
WORKDIR /app

# requirements.txtだけを先にコピー
COPY requirements.txt .
# ライブラリをインストール
RUN pip install -r requirements.txt

# 残りのファイルを全部コピー（main.pyなど）
COPY . .

# コンテナ起動時に実行するコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]