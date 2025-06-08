# Battle Party Recognition with Arena Log

## About
アリーナのリザルト画像から編成生徒を認識するツールです  
discordのbotトークンと、画像認識用のテンプレート画像を用意できれば動作します

## Requirement
- opencv-python
- Pillow
- numpy
- discord.py

## 実行手順
1. 依存ライブラリのインストール
2. テンプレート画像を準備: `templates/` に A.jpg, B.jpg など配置
    - この時のファイル名が出力されます
3. `config.py`を編集し、Botトークンを設定する
    - トークンの直書きは非推奨です
    - 環境変数から読み込むなどの工夫をしてください
4. botを起動
```bash
cd [main.pyのあるディレクトリ]
python main.py
```