# Flaskクラスをimportする
from flask import Flask

# Flaskクラスをインスタンス化する
app=Flask(__name__)

# URLと実行する関数をマッピングする
@app.route("/")
def index():
    return "Hello, Fkaskbook!"

@app.route("/hello", 
           methods=["GET"], 
           endpoint="hello-endpoint")
def hello():
    return "Hello World!"


# Debugモードに環境変数でならないので小川が挿入。でも入らないので一旦コメントアウト
# if __name__ == "__main__":
#     app.run(debug=True)