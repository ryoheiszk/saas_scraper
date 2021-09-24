# ここからアプリスクレイパー

## 概要

業務でいくらかのSaaSの情報が必要だったため、[ここからアプリ](https://ittools.smrj.go.jp/app/index.php)をスクレピングすることにした。

## 環境構築

`build.sh`を実行すれば必要なDockerコマンドが実行される。

VSCodeユーザーなら、`.devcontainer/devcontainer.json`の通り`ms-vscode-remote.remote-containers`用の設定ができているため利用されたし。

`vnc://localhost:5900`にてブラウザの表示を見ながらデバッグが可能。

## 実行方法

`/app/src/main.py`を実行すると、`/app/src/exported`にいろいろ出力される。

## メモ

Seleniumを利用しているが、この用途ならrequestsが適切ではあった。
過去のコードを活用し、短時間で収集するためにこのようにした。
ないとは思うが、定期的に収集することがあるならば、このプログラムは利用しないことが望まれる。
