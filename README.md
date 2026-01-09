# SampleSQLModelApp
PythonのORMライブラリである(SQLModel)[https://sqlmodel.tiangolo.com/]を技術検証するリポジトリである。  
※後々にフォルダ構成は見直す予定です。

## 環境構築 (Environment Setup)

### Docker Compose (推奨)
Docker と Docker Compose がインストールされていることが前提です。

1. コンテナのビルドと起動:
   ```bash
   docker-compose up -d --build
   ```

2. ログの確認 (任意):
   ```bash
   docker-compose logs -f
   ```

3. コンテナの停止:
   ```bash
   docker-compose down
   ```

### ローカル開発 (Local Development)
ローカルで直接 Python アプリケーションを実行する場合の手順です。

#### 前提条件
- Python 3.10 以上
- PostgreSQL 15 (または Docker で DB のみ起動)

#### セットアップ手順

1. 仮想環境の作成と有効化:
   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```

2. 依存関係のインストール:
   ```bash
   pip install -r requirements.txt
   ```

3. データベースの起動:
   Docker を使用して DB のみ起動する場合:
   ```bash
   docker-compose up --build
   ```
