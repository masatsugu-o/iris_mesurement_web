from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from pathlib import Path
from apps.iris.models import Customer
from apps.iris.forms import CustomerForm
import json
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# Blueprintを使ってauthを生成する
iris = Blueprint(
    "iris",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# indexエンドポイントを作成する
@iris.route("/")
def index():
    form = CustomerForm()
    return render_template("iris/index.html", form=form)

# 以下、小川改造分
@iris.route("/run_external", methods=["GET"])
@login_required
def run_external():
    import subprocess

    script_path = Path(current_app.root_path) / "iris" / "irishue_measurement_v01_r3_flask.py"
    try:
        # Python スクリプトをサブプロセスとして実行
        subprocess.run(["python", str(script_path)], check=True)
        flash("スクリプト実行が完了しました。")
    except subprocess.CalledProcessError as e:
        flash("スクリプト実行に失敗しました。")
        current_app.logger.error(f"Script error: {e}")

    customer_data = session.get("customer_data")
    if not customer_data:
        flash("顧客情報が見つかりません")
        return redirect(url_for("iris.index"))

    # # 簡易測定処理（例）
    # #result = perform_measurement()
    # result={
    #     "height": "172cm",
    #     "weight": "64kg",
    #     "bmi": "21.6",
    #     "blood_pressure": "120/80"
    # }

    result_path = Path(current_app.root_path) .parent / "result.json"
    if result_path.exists():
        with open(result_path, "r", encoding="utf-8") as f:
            result = json.load(f)
    else:
        flash("測定結果が見つかりませんでした")
        return redirect(url_for("iris.index"))

    # 顧客データに測定結果を組み込んで保存
    new_customer = Customer(
        user_id=current_user.id,
        customer_id=customer_data["customer_id"],
        name=customer_data["name"],
        gender=customer_data["gender"],
        memo=customer_data["memo"],
        result=json.dumps(result, ensure_ascii=False),
    )
    db.session.add(new_customer)
    db.session.commit()

    session.pop("customer_data", None)  # 一時データ削除
    flash("顧客情報と測定結果を保存しました")

    # # 処理後に index に戻る
    # return redirect(url_for("iris.index")) 
    # 処理後に analyze でグラフ表示
    return redirect(url_for("iris.analyze")) 


# 一時的に顧客データを保存
@iris.route("/save_customer_temp", methods=["POST"])
def save_customer_temp():
    session["customer_data"] = {
        "customer_id": request.form.get("customer_id"),
        "name": request.form.get("name"),
        "gender": request.form.get("gender"),
        "memo": request.form.get("memo"),
    }
    return redirect(url_for("iris.run_external"))

@iris.route('/analyze', methods=['GET'])
def analyze():
    graph = None
    result_path = Path(current_app.root_path).parent / "result.json"
    
    if not result_path.exists():
        flash("測定結果ファイルが存在しません")
        return redirect(url_for("iris.index"))

    try:
        with open(result_path, "r", encoding="utf-8") as f:
            result = json.load(f)
    except Exception as e:
        flash(f"測定結果の読み込みに失敗しました: {e}")
        return redirect(url_for("iris.index"))

    ### グラフ描画処理（元のロジックを活用）
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    fig.subplots_adjust(top=0.75, bottom=0.1)

    # 明るさ（RGB）グラフ
    # 該当テストデータを抽出
    target = next((r for r in result if r["test_name"] == "ホワイト(RG)決定結果"), None)
    if not target:
        flash("グラフ描画用の測定結果が見つかりませんでした")
        return redirect(url_for("iris.index"))
    # グラフ用の数値取得
    values = [target["target_r_per"], target["target_g_per"], target["target_b_per"]]
    #values = [result["R"], result["G"], result["B"]]
    labels = ['R', 'G', 'B']
    colors1 = ['red', 'green', 'blue']
    axes[0].bar(labels, values, color=colors1)
    axes[0].set_ylim(0, 100)
    axes[0].set_title('Brightness characteristic')
    axes[0].set_yticks(range(0, 101, 10))
    for y in range(0, 101, 10):
        axes[0].axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5)

    # 色バランス（例：G cut/R cut） ← result.jsonの構造に応じて調整
    # 対象データを抽出
    green_test = next((r for r in result if r["test_name"] == "緑色視感度測定結果"), None)
    red_test = next((r for r in result if r["test_name"] == "赤色視感度測定結果"), None)
    # 初期化
    val_g = val_r = 0
    # 低下率
    ref_r=red_test["big_r_per"]
    ref_g=green_test["big_g_per"]
    loss_r=red_test["target_r_per"]
    loss_g=green_test["target_g_per"]
    r_loss=(ref_r-loss_r)/ref_r*100
    g_loss=(ref_g-loss_g)/ref_g*100
    if r_loss >= g_loss:
        val_g=(loss_g-loss_r)/loss_g*100
    else:
        val_r=(loss_r-loss_g)/loss_r*100
    values2 = [val_g, val_r]
    #values2 = [result.get("G_cut", 0), result.get("R_cut", 0)]
    labels2 = ['G cut', 'R cut']
    colors2 = ['green', 'red']
    axes[1].bar(labels2, values2, color=colors2)
    axes[1].set_ylim(0, 100)
    axes[1].set_title('Color balance')
    axes[1].set_yticks(range(0, 101, 10))
    for y in range(0, 101, 10):
        axes[1].axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5)
    # 感度
    val_1type = -1
    val_2type = -1
    if r_loss != 0 and g_loss != 0:
        val_1type=1/r_loss/(1/g_loss)
        val_2type=1/g_loss/(1/r_loss)
    # 表形式で感度を表示（グラフの右側）
    table_data = [
        ['Type 1 Sensitivity', f'{val_1type:.2f}'],
        ['Type 2 Sensitivity', f'{val_2type:.2f}']
    ]
    # 表の表示
    fig.text(0.75, 0.92,
            f'Type 1 Sensitivity: {val_1type:.2f}\nType 2 Sensitivity: {val_2type:.2f}',
            fontsize=10, verticalalignment='top',
            bbox=dict(facecolor='white', edgecolor='black'))

    # グラフをBase64化してHTMLに渡す
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('iris/analyze.html', graph=graph)
