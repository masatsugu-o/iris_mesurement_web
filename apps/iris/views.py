from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from pathlib import Path
from apps.iris.models import Customer
from apps.iris.forms import CustomerForm

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

    # 簡易測定処理（例）
    #result = perform_measurement()
    result={
        "height": "172cm",
        "weight": "64kg",
        "bmi": "21.6",
        "blood_pressure": "120/80"
    }

    # 顧客データに測定結果を組み込んで保存
    new_customer = Customer(
        user_id=current_user.id,
        customer_id=customer_data["customer_id"],
        name=customer_data["name"],
        gender=customer_data["gender"],
        memo=customer_data["memo"],
        result=result,
    )
    db.session.add(new_customer)
    db.session.commit()

    session.pop("customer_data", None)  # 一時データ削除
    flash("顧客情報と測定結果を保存しました")

    # 処理後に index に戻る
    return redirect(url_for("iris.index")) 

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

