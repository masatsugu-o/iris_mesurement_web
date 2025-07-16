from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_and_plot():
    graph = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file, header=None, encoding="shift_jis")

            fig, axes = plt.subplots(1, 2, figsize=(10,4), sharey=True)
            fig.subplots_adjust(top=0.75, bottom=0.1)  # グラフ上部の余白を広げる

            # 左側のグラフ（E1, F1, G1）
            values = df.iloc[0, 4:7]
            labels = ['R', 'G', 'B']
            colors1 = ['blue', 'green', 'red']

            axes[0].bar(labels, values, color=colors1)
            axes[0].set_ylim(0, 100)
            axes[0].set_title('Brightness characteristic')
            #axes[0].set_ylabel('値')
            axes[0].set_yticks(range(0, 101, 10))
            for y in range(0, 101, 10):
                axes[0].axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5)

            # 右側のグラフ（新しく計算された値）
            b1 = df.iloc[0, 1]
            i2 = df.iloc[1, 8]
            h3 = df.iloc[2, 7]

            # 低下率
            val_i2 = (b1-i2) / b1 * 100
            val_h3 = (b1-h3) / b1 * 100

            # 感度
            val_1type = -1
            val_2type = -1
            if val_i2 != 0 and val_h3 != 0:
                val_1type=1/val_h3/(1/val_i2)
                val_2type=1/val_i2/(1/val_h3)

            val_g=0
            val_r=0

            if val_i2 >= val_h3:
                val_r=(h3-i2)/h3 * 100
            else:
                val_g=(i2-h3)/i2 * 100

            labels2 = ['G cut', 'R cut']
            values2 = [val_g, val_r]
            colors2 = ['green', 'red']  

            axes[1].bar(labels2, values2, color=colors2)
            axes[1].set_ylim(0, 100)
            axes[1].set_title('Color balance')
            axes[1].set_yticks(range(0, 101, 10))
            axes[1].tick_params(labelleft=True) 
            for y in range(0, 101, 10):
                axes[1].axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5)


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

            # # 表の描画（axes[1] の右側に配置）
            # fig.text(0.75, 0.5, '\n'.join(f'{row[0]}: {row[1]}' for row in table_data),
            #         fontsize=10, verticalalignment='center', bbox=dict(facecolor='white', edgecolor='black'))


            ###################################################
            # 以下はぐらふひとつのとき上記ではサブプロットに変えた
            ###################################################
            # # E1, F1, G1はそれぞれ4,5,6番目のインデックス
            # values = df.iloc[0, 4:7]  # E1=4, F1=5, G1=6（0始まり）
            # colors = ['red', 'green', 'blue']
            # labels = ['R', 'G', 'B']           

            # # グラフを作成
            # plt.figure(figsize=(6,4))
            # bars = plt.bar(labels, values, color=colors)
            # plt.ylim(0, 100)  # 最小0, 最大100
            # plt.yticks(range(0, 101, 10))
            # plt.title('Brightness characteristic')
            # #plt.ylabel('値')
            # # 各yticksに合わせて破線を描画
            # for y in range(0, 101, 10):
            #     plt.axhline(y=y, color='lightgray', linestyle='--', linewidth=0.5)
            #
            # #######グラフに波線など模様をいれるときに使えるかも。興味で残した########
            # # # 波線の描画：各Y軸目盛りに挿入
            # # x_min, x_max = plt.xlim()
            # # x_vals = np.linspace(x_min, x_max, 100)  # 横方向に滑らかに波を描く
            # # for y in range(0, 101, 10):
            # #     wave = 1.5 * np.sin(10 * np.pi * (x_vals - x_min) / (x_max - x_min))
            # #     plt.plot(x_vals, y + wave, color='lightgray', linewidth=0.5, alpha=0.6)

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            graph = base64.b64encode(img.getvalue()).decode()
            plt.close()
    return render_template('index.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
