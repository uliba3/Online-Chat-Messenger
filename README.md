# Online-Chat-Messenger
ステージ 3 （任意・上級者）
このステージでは、より高度な機能と要件が求められ、その実装にはかなりの労力が必要です。


パスワード
コードベースのリファクタリングを行い、ペイロードが常に JSON 形式でデコードされるようにします。
チャットルームを作成するとき、ホストはパスワードのオプション引数を渡すことができ、パスワードを持つクライアントだけがチャットルームに参加することができます。
クライアントは、チャットルームに参加する際にオプションの引数としてパスワードを渡すことができます。チャットルームがパスワードで保護されている場合、このパスワードが正しく一致する必要があります。
クライアントとしてデスクトップアプリケーションを作成
JavaScript または TypeScript、Electron.js を使用します。Electron.js は Node.js を使用しており、JS コードはブラウザ上ではなく、オペレーティングシステム上で実行されます。

ユーザーが簡単にチャットルームを作成し、参加できるデスクトップアプリケーションを作成します。
アプリには、ユーザーがチャットルームを作成するか参加するかを選択するナビゲーションがあります。
チャットルームを作成する場合、ユーザーはユーザー名とチャットルーム名を入力してチャットルームを作成し、サーバに接続します。
チャットルームに参加する場合、ユーザーは自動的にチャットルーム GUI に参加し、テキストを入力したり、参加以降のすべてのメッセージを上下にスクロールすることができます。
メッセージの暗号化
暗号化方式として、RSA に似た手法を使用して、サーバとクライアント間で送受信されるすべてのメッセージを保護します。クライアントとサーバは、送受信するすべてのメッセージを以下の暗号化方式で処理します。


クライアントの手順：

クライアントはローカル環境で秘密鍵と公開鍵を生成します。
サーバへの接続要求を行う際に、生成した公開鍵をサーバに送信します。
サーバはこの公開鍵を保存し、この鍵を用いてメッセージを暗号化した後でクライアントに送信します。
メッセージに含まれるトークンを復号化する唯一の方法は、正確な秘密鍵を使用することです。クライアントはローカルに保存された秘密鍵で復号化を行います。
逆のプロセス：

すべてのクライアントは、初めにサーバからその公開鍵を取得します。
クライアントがサーバにメッセージを送る際は、このサーバの公開鍵を使用してメッセージを暗号化する必要があります。
これらがメッセージ暗号化における主要な要件と手順です。


拡張性
拡張性について実装する必要はありませんが、以下の非機能要件について考慮してみてください。


チャットメッセージングシステムは、少なくとも毎秒 10,000 パケットの送信に対応できるようにしてください。たとえば、1 秒に平均で 2 メッセージを送る 10 人がいる 500 個のチャットルームをサポートできると考えられます。


もし WhatsApp や LINE のような大規模なサービスになると、どうなるでしょうか。これらのメッセージングアプリには数億から数十億のユーザーがいます。ピーク時には 4 億人がアクティブで、各ユーザーが 10 分に 1 回メッセージを送ると仮定した場合、平均して 20% のユーザーが 4 人グループに参加しているとしましょう。この条件下で、1 秒間に送信されるパケット数を計算してみてください。


ピーク時に多数のユーザーをサポートする場合、1 秒間にどれだけのパケットを送信できるのか考慮が必要です。具体的には以下の点を考えてみましょう。


ロードバランシング

ロードバランサーはネットワークトラフィックを複数のサーバに効率よく振り分けます。もし 1 台のサーバが 1 秒間に 10,000 パケットを処理できるとしたら、その影響は 1 秒間に処理されるソケットの総数にどう出るでしょうか？


並行処理

一つのコアで 1 秒間に 10,000 ソケットを処理できるかもしれませんが、16 コアでプログラムを実行できるとしたら、どうなるでしょうか？


分散プログラミング

特定のタスクが小さなサブタスクに分けられ、それが複数のコアを持ついくつかのマシンに分散される場合、1 秒間に処理できるソケットの総数はどれくらいになるでしょうか？