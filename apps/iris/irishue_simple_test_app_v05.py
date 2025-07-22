# tkinterのインポート
import tkinter as tk
import tkinter.ttk as ttk

# numpyのインポート
import numpy as np

# sysのインポート
import sys

# exe化時のエラー回避のための追加
from sys import exit

# timeのインポート
import time

# datetimeのインポート
import datetime

# osのインポート
import os
from os import path


#########################
# RGB値を16進数に変換
#########################
def from_rgb_to_colorcode(rgb):
    return '#%02x%02x%02x' % rgb


#########################
# 測定画像を描画
#########################
def drawing_test_image(big_r, big_g, big_b, target_r, target_g ,target_b):

    # 大円の半径を設定
    big_circle_radius = 540

    # 輝度を変化させる小円の半径を設定
    target_radius = viewing_angle.get()

    # 円の中央からの横位置
    distance = 0

    global my_canvas

    # 描画前に表示していた内容を消す
    my_canvas.delete('all')

    # 大円を描画
    my_canvas.create_oval(960 + distance - big_circle_radius, 540 - big_circle_radius, 960 + distance + big_circle_radius, 540 + big_circle_radius, width=0, fill=from_rgb_to_colorcode((big_r, big_g, big_b)))

    # 小円を描画
    my_canvas.create_oval(960 + distance - target_radius, 540 - target_radius, 960 + distance + target_radius, 540 + target_radius, width=0, fill=from_rgb_to_colorcode((target_r, target_g ,target_b)))


    # 動作確認用
    # current_data_text = '大円RGB: R ' + str(big_r) + ' G ' + str(big_g) + ' B ' + str(big_b) + '  小円RGB: R ' + str(target_r) + ' G ' + str(target_g) + ' B ' + str(target_b) 
    # my_canvas.create_text(10, 1080-30, text=current_data_text, anchor="nw", font=("MSゴシック", 20), fill="white")


    # キャンパスを描画
    my_canvas.pack()



#########################
# 経過時間を測定
#########################
def get_elapsed_time():
    global time_start
    global time_end
    time_end = time.perf_counter()
    elapsed_time = time_end - time_start
    time_start = time.perf_counter()
    return round(elapsed_time, 2)


################
# 測定結果をファイルに保存
################
def save_result_file():
    global result

    # ファイル名に付加する日付と時間の文字列を準備
    date_and_time = str(datetime.datetime.now())
    date_and_time = date_and_time.replace(':', '-')
    date_and_time = date_and_time.replace(' ', '_')
    date_and_time = date_and_time[:-7]

    # 視野角1度の場合
    if viewing_angle.get() == 13:
        viewing_angle_str ='1'
    # 視野角2度の場合
    elif viewing_angle.get() == 26:
        viewing_angle_str ='2'
    # 視野角4度の場合
    elif viewing_angle.get() == 52:
        viewing_angle_str ='4'

    # resultをファイルに保存
    result_file=open(name_entry_input_frame.get() + '_' + path.splitext(path.basename(__file__))[0] + '_result_' + date_and_time + '_angle=' + viewing_angle_str + '.csv','w')
    np.savetxt(result_file, result, delimiter=',', fmt="%s")
    result_file.close()


#########################
# ボタン押下で測定前画面へ移動時に実行
#########################
def to_pre_test_frame(frame):

    # 全画面表示に切り替え
    root.attributes('-fullscreen', True)
    
    result_dtype = [('test_name', 'U100'),  ('big_r', 'u1'), ('big_g', 'u1'), ('big_b', 'u1'), ('big_r_per', 'f2'), ('big_g_per', 'f2'), ('big_b_per', 'f2'),\
         ('target_r', 'u1'), ('target_g', 'u1'), ('target_b', 'u1'), ('target_r_per', 'f2'), ('target_g_per', 'f2'), ('target_b_per', 'f2'),\
            ('time', 'f8')]

    # result配列を用意
    global result
    result = np.empty(1, dtype = result_dtype)

    global tmp_result
    tmp_result = np.empty(1, dtype = result_dtype)


    #測定前画面へ移動
    pre_test_frame.tkraise()
    pre_test_frame.focus_set()
 

#########################
# ホワイト決定(B)画面へ移動時に実行
#########################
def to_white_b_test_frame(event):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas
    my_canvas = tk.Canvas(white_b_test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # テスト画像を描画
    drawing_test_image(tmp_r, tmp_g, tmp_b,\
        tmp_r, tmp_g, tmp_b)

    white_b_test_frame.tkraise()
    white_b_test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# ホワイト決定(B)画面で8キー押下時に実行：大円（小円も含む）の輝度アップ
#########################
def white_b_test_increase_circle_brightness(event):
    global tmp_r, tmp_g, tmp_b

    if tmp_r + 1 <= 255:
        tmp_r += 1
        tmp_g += 1
        tmp_b += 1
        drawing_test_image(tmp_r, tmp_g, tmp_b,\
            tmp_r, tmp_g, tmp_b)


#########################
# ホワイト決定(B)画面で2キー押下時に実行：大円（小円も含む）の輝度ダウン
#########################
def white_b_test_decrease_circle_brightness(event):
    global tmp_r, tmp_g, tmp_b

    if tmp_r - 1 >= 0:
        tmp_r -= 1
        tmp_g -= 1
        tmp_b -= 1
        drawing_test_image(tmp_r, tmp_g, tmp_b,\
            tmp_r, tmp_g, tmp_b)


#########################
# ホワイト決定(B)画面でEnterキー押下時に実行：まぶしくない明るさまで明るくして押下
#########################
def white_b_test_too_bright_now(event):
    global max_b, result, tmp_result

    # ホワイト決定結果を配列に格納
    tmp_result[0]['test_name'] = 'ホワイト(B)決定結果'
    tmp_result[0]['big_r'] = tmp_r
    tmp_result[0]['big_g'] = tmp_g
    tmp_result[0]['big_b'] = tmp_b
    tmp_result[0]['big_r_per'] = (tmp_r/255) ** 2.2 * 100
    tmp_result[0]['big_g_per'] = (tmp_g/255) ** 2.2 * 100
    tmp_result[0]['big_b_per'] = (tmp_b/255) ** 2.2 * 100
    tmp_result[0]['target_r'] = tmp_r
    tmp_result[0]['target_g'] = tmp_g
    tmp_result[0]['target_b'] = tmp_b
    tmp_result[0]['target_r_per'] =  (tmp_r/255) ** 2.2 * 100
    tmp_result[0]['target_g_per'] =  (tmp_g/255) ** 2.2 * 100
    tmp_result[0]['target_b_per'] =  (tmp_b/255) ** 2.2 * 100
    tmp_result[0]['time'] = get_elapsed_time()

    # tmp_result配列を、result配列に追加
    result = np.concatenate((result, tmp_result), axis = 0)

    #ダミーであるresultの最初の行を削除
    result = np.delete(result, 0, axis=0) 

    # Bの値をホワイトの決定値として格納
    max_b = tmp_b

    # 測定前画面へ移動
    pre_white_rg_test_frame.tkraise()
    pre_white_rg_test_frame.focus_set()
 

#########################
# ホワイト決定(RG)画面へ移動時に実行
#########################
def to_white_rg_test_frame(event):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas
    my_canvas = tk.Canvas(white_rg_test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # テスト画像を描画
    drawing_test_image(tmp_r, tmp_g, max_b,\
        tmp_r, tmp_g, max_b)

    white_rg_test_frame.tkraise()
    white_rg_test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# ホワイト決定(RG)画面で8キー押下時に実行：大円（小円も含む）の輝度アップ
#########################
def white_rg_test_increase_small_circle_brightness(event):
    global tmp_r, tmp_g

    if tmp_r + 1 and tmp_g + 1 <= 255:
        tmp_r += 1
        tmp_g += 1
        drawing_test_image(tmp_r, tmp_g, max_b,\
            tmp_r, tmp_g, max_b)


#########################
# ホワイト決定(RG)画面で2キー押下時に実行：大円（小円も含む）の輝度ダウン
#########################
def white_rg_test_decrease_small_circle_brightness(event):
    global tmp_r, tmp_g

    if tmp_r - 1 >= max_b and tmp_g - 1 >= max_b :
        tmp_r -= 1
        tmp_g -= 1
        drawing_test_image(tmp_r, tmp_g, max_b,\
            tmp_r, tmp_g, max_b)


#########################
# ホワイト決定(RG)画面でEnterキー押下時に実行：自分にとっての「白」であるとき押下
#########################
def white_rg_test_too_bright_now(event):
    global max_r, max_g, result, tmp_result

    # ホワイト決定結果を配列に格納
    tmp_result[0]['test_name'] = 'ホワイト(RG)決定結果'
    tmp_result[0]['big_r'] = tmp_r
    tmp_result[0]['big_g'] = tmp_g
    tmp_result[0]['big_b'] = max_b
    tmp_result[0]['big_r_per'] = (tmp_r/255) ** 2.2 * 100
    tmp_result[0]['big_g_per'] = (tmp_g/255) ** 2.2 * 100
    tmp_result[0]['big_b_per'] = (max_b/255) ** 2.2 * 100
    tmp_result[0]['target_r'] = tmp_r
    tmp_result[0]['target_g'] = tmp_g
    tmp_result[0]['target_b'] = max_b
    tmp_result[0]['target_r_per'] =  (tmp_r/255) ** 2.2 * 100
    tmp_result[0]['target_g_per'] =  (tmp_g/255) ** 2.2 * 100
    tmp_result[0]['target_b_per'] =  (max_b/255) ** 2.2 * 100
    tmp_result[0]['time'] = get_elapsed_time()

    # tmp_result配列を、result配列に追加
    result = np.concatenate((result, tmp_result), axis = 0)

    # RGの値をホワイトの決定値として格納
    max_r = tmp_r
    max_g = tmp_g

    # 測定前画面へ移動
    pre_g_test_frame.tkraise()
    pre_g_test_frame.focus_set()


#########################
# G画面へ移動時に実行
#########################
def to_g_test_frame(event):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas
    my_canvas = tk.Canvas(g_test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # テスト画像を描画
    drawing_test_image(max_r, max_g, max_b,\
        max_r, tmp_g, max_b)

    g_test_frame.tkraise()
    g_test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# G画面で8キー押下時に実行：小円Gの輝度アップ
#########################
def g_test_increase_small_circle_brightness(event):
    global tmp_g

    if tmp_g + 1 <= max_g:
        tmp_g += 1
        drawing_test_image(max_r, max_g, max_b,\
            max_r, tmp_g, max_b)


#########################
# G画面で2キー押下時に実行：小円Gの輝度ダウン
#########################
def g_test_decrease_small_circle_brightness(event):
    global tmp_g

    if tmp_g - 1 >= 0:
        tmp_g -= 1
        drawing_test_image(max_r, max_g, max_b,\
            max_r, tmp_g, max_b)


#########################
# G画面でEnterキー押下時に実行：小円が見えた場合
#########################
def g_test_i_can_see_now(event):
    global result, tmp_result

    # ホワイト決定結果を配列に格納
    tmp_result[0]['test_name'] = '緑色視感度測定結果'
    tmp_result[0]['big_r'] = max_r
    tmp_result[0]['big_g'] = max_g
    tmp_result[0]['big_b'] = max_b
    tmp_result[0]['big_r_per'] = (max_r/255) ** 2.2 * 100
    tmp_result[0]['big_g_per'] = (max_g/255) ** 2.2 * 100
    tmp_result[0]['big_b_per'] = (max_b/255) ** 2.2 * 100
    tmp_result[0]['target_r'] = max_r
    tmp_result[0]['target_g'] = tmp_g
    tmp_result[0]['target_b'] = max_b
    tmp_result[0]['target_r_per'] =  (max_r/255) ** 2.2 * 100
    tmp_result[0]['target_g_per'] =  (tmp_g/255) ** 2.2 * 100
    tmp_result[0]['target_b_per'] =  (max_b/255) ** 2.2 * 100
    tmp_result[0]['time'] = get_elapsed_time()

    # tmp_result配列を、result配列に追加
    result = np.concatenate((result, tmp_result), axis = 0)

    # 測定前画面2へ移動
    pre_r_test_frame.tkraise()
    pre_r_test_frame.focus_set()


#########################
# R画面へ移動時に実行
#########################
def to_r_test_frame(event):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas
    my_canvas = tk.Canvas(r_test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # テスト画像を描画
    drawing_test_image(max_r, max_g, max_b,\
        tmp_r, max_g, max_b)

    r_test_frame.tkraise()
    r_test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# R画面で8キー押下時に実行：小円Rの輝度アップ
#########################
def r_test_increase_small_circle_brightness(event):
    global tmp_r

    if tmp_r + 1 <= max_r:
        tmp_r += 1
        drawing_test_image(max_r, max_g, max_b,\
            tmp_r, max_g, max_b)



#########################
# R画面で2キー押下時に実行：小円Rの輝度ダウン
#########################
def r_test_decrease_small_circle_brightness(event):
    global tmp_r

    if tmp_r - 1 >= 0:
        tmp_r -= 1
        drawing_test_image(max_r, max_g, max_b,\
            tmp_r, max_g, max_b)


#########################
# R画面でEnterキー押下時に実行：小円が見えた場合
#########################
def r_test_i_can_see_now(event):
    global result, tmp_result

    # ホワイト決定結果を配列に格納
    tmp_result[0]['test_name'] = '赤色視感度測定結果'
    tmp_result[0]['big_r'] = max_r
    tmp_result[0]['big_g'] = max_g
    tmp_result[0]['big_b'] = max_b
    tmp_result[0]['big_r_per'] = (max_r/255) ** 2.2 * 100
    tmp_result[0]['big_g_per'] = (max_g/255) ** 2.2 * 100
    tmp_result[0]['big_b_per'] = (max_b/255) ** 2.2 * 100
    tmp_result[0]['target_r'] = tmp_r
    tmp_result[0]['target_g'] = max_g
    tmp_result[0]['target_b'] = max_b
    tmp_result[0]['target_r_per'] =  (tmp_r/255) ** 2.2 * 100
    tmp_result[0]['target_g_per'] =  (max_g/255) ** 2.2 * 100
    tmp_result[0]['target_b_per'] =  (max_b/255) ** 2.2 * 100
    tmp_result[0]['time'] = get_elapsed_time()

    # tmp_result配列を、result配列に追加
    result = np.concatenate((result, tmp_result), axis = 0)

    # 測定前画面2へ移動
    pre_b_test_frame.tkraise()
    pre_b_test_frame.focus_set()


#########################
# B画面へ移動時に実行
#########################
def to_b_test_frame(event):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas
    my_canvas = tk.Canvas(b_test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # テスト画像を描画
    drawing_test_image(max_r, max_g, max_b,\
        max_r, max_g, tmp_b)

    b_test_frame.tkraise()
    b_test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# B画面で8キー押下時に実行：小円Rの輝度アップ
#########################
def b_test_increase_small_circle_brightness(event):
    global tmp_b

    if tmp_b + 1 <= max_b:
        tmp_b += 1
        drawing_test_image(max_r, max_g, max_b,\
            max_r, max_g, tmp_b)



#########################
# B画面で2キー押下時に実行：小円Rの輝度ダウン
#########################
def b_test_decrease_small_circle_brightness(event):
    global tmp_b

    if tmp_b - 1 >= 0:
        tmp_b -= 1
        drawing_test_image(max_r, max_g, max_b,\
            max_r, max_g, tmp_b)


#########################
# B画面でEnterキー押下時に実行：小円が見えた場合
#########################
def b_test_i_can_see_now(event):
    global result, tmp_result, tmp_r, tmp_g

    # ホワイト決定結果を配列に格納
    tmp_result[0]['test_name'] = '青色視感度測定結果'
    tmp_result[0]['big_r'] = max_r
    tmp_result[0]['big_g'] = max_g
    tmp_result[0]['big_b'] = max_b
    tmp_result[0]['big_r_per'] = (max_r/255) ** 2.2 * 100
    tmp_result[0]['big_g_per'] = (max_g/255) ** 2.2 * 100
    tmp_result[0]['big_b_per'] = (max_b/255) ** 2.2 * 100
    tmp_result[0]['target_r'] = max_r
    tmp_result[0]['target_g'] = max_g
    tmp_result[0]['target_b'] = tmp_b
    tmp_result[0]['target_r_per'] =  (max_r/255) ** 2.2 * 100
    tmp_result[0]['target_g_per'] =  (max_g/255) ** 2.2 * 100
    tmp_result[0]['target_b_per'] =  (tmp_b/255) ** 2.2 * 100
    tmp_result[0]['time'] = get_elapsed_time()

    # tmp_result配列を、result配列に追加
    result = np.concatenate((result, tmp_result), axis = 0)

    # tmp_r、tmp_gをmax_r、max_gにリセット
    tmp_r = max_r
    tmp_g = max_g

    # 測定前画面2へ移動
    pre_rg_test_frame.tkraise()
    pre_rg_test_frame.focus_set()


#########################
# RG画面へ移動時に実行
#########################
def to_rg_test_frame(event):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas
    my_canvas = tk.Canvas(rg_test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # テスト画像を描画
    drawing_test_image(max_r, max_g, max_b,\
        tmp_r, tmp_g, max_b)

    rg_test_frame.tkraise()
    rg_test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# RG画面で8キー押下時に実行：小円Rの輝度アップ
#########################
def rg_test_increase_small_circle_brightness(event):
    global tmp_r, tmp_g

    if tmp_r + 1 <= max_r and tmp_g + 1 <= max_g:
        tmp_r += 1
        tmp_g += 1
        drawing_test_image(max_r, max_g, max_b,\
            tmp_r, tmp_g, max_b)



#########################
# RG画面で2キー押下時に実行：小円Rの輝度ダウン
#########################
def rg_test_decrease_small_circle_brightness(event):
    global tmp_r, tmp_g

    if tmp_r - 1 >= 0 and tmp_g - 1 >= 0:
        tmp_r -= 1
        tmp_g -= 1
        drawing_test_image(max_r, max_g, max_b,\
            tmp_r, tmp_g, max_b)


#########################
# RG画面でEnterキー押下時に実行：小円が見えた場合
#########################
def rg_test_i_can_see_now(event):
    global result, tmp_result

    # ホワイト決定結果を配列に格納
    tmp_result[0]['test_name'] = '赤・緑色視感度測定結果'
    tmp_result[0]['big_r'] = max_r
    tmp_result[0]['big_g'] = max_g
    tmp_result[0]['big_b'] = max_b
    tmp_result[0]['big_r_per'] = (max_r/255) ** 2.2 * 100
    tmp_result[0]['big_g_per'] = (max_g/255) ** 2.2 * 100
    tmp_result[0]['big_b_per'] = (max_b/255) ** 2.2 * 100
    tmp_result[0]['target_r'] = tmp_r
    tmp_result[0]['target_g'] = tmp_g
    tmp_result[0]['target_b'] = max_b
    tmp_result[0]['target_r_per'] =  (tmp_r/255) ** 2.2 * 100
    tmp_result[0]['target_g_per'] =  (tmp_g/255) ** 2.2 * 100
    tmp_result[0]['target_b_per'] =  (max_b/255) ** 2.2 * 100
    tmp_result[0]['time'] = get_elapsed_time()

    # tmp_result配列を、result配列に追加
    result = np.concatenate((result, tmp_result), axis = 0)

    # 結果をCSVファイルに保存
    save_result_file()

    #測定終了画面へ移動
    end_frame.tkraise()
    end_frame.focus_set()


#########################
# プログラム終了時に実行
#########################
def program_end(event):
    # プログラム終了
    sys.exit()


#########################
# メインプログラム
#########################
# or以降は、exe化時のエラー回避のための追加。ファイル名を変更してexe化する場合、修正が必要
if __name__ == '__main__' or __name__ == '__irishue_simple_test_app_v05__':

    ################
    # 時刻を格納するグローバル変数を用意
    ################
    time_start = time.perf_counter()
    time_end = time.perf_counter()

    ################
    # 提示円のRGBのグローバル変数を準備（初期表示を0.5%とする）
    ################
    tmp_r = 23
    tmp_g = 23
    tmp_b = 23
    max_r = 0
    max_g = 0
    max_b = 0

    ################
    # インターバル画面の表示時間を設定
    ################
    interval_msec = 500

    ################
    # rootメインウィンドウの設定
    ################
    root = tk.Tk()

    # 全画面表示に切り替え
    # root.attributes('-fullscreen', True)

    # 700x500で画面を表示
    root.geometry('700x500')

    # rootメインウィンドウのグリッドを 1x1 にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    ################
    # スタイル設定
    ################
    style = ttk.Style()
    # 背景色を黒にするためのスタイルを設定
    style.configure('My.TFrame', background='black')
    # ボタンのフォントサイズを変更にするためのスタイルを設定
    style.configure('My.TButton', font=15)


    ################
    # 名前入力画面
    ################
    # input_frameの作成と設置
    input_frame = ttk.Frame(root, style='My.TFrame')
    input_frame.grid(row=0, column=0, sticky='nsew')

    # 名前入力ウィジェットの作成
    name_label_input_frame = ttk.Label(input_frame, text='お名前または測定番号を入力してください。\n入力内容が測定結果ファイル名の先頭になります。\n\n\
注意：日本語入力で入力した場合は、「測定開始」ボタンを押す前に日本語入力をOFFにしてください。', foreground='white', background='black', font=('MSゴシック', '10'))
    name_entry_input_frame = ttk.Entry(input_frame, font=('MSゴシック', '10'))

    # 名前入力ウィジェットの設置
    name_label_input_frame.place(x = 100, y = 240)
    name_entry_input_frame.place(x = 100, y = 320)

    # 測定開始ボタンの作成
    button_input_frame = ttk.Button(input_frame, text='測定開始', command=lambda: to_pre_test_frame(pre_test_frame), style='My.TButton')
    # 測定開始ボタンを設置
    button_input_frame.place(x = 300, y = 400)

    # 小円の視野角を選択するラジオボタンを設置
    # チェック有無変数
    viewing_angle = tk.IntVar()
    # value=26（小円視野角：2度）のラジオボタンにチェックを入れる
    viewing_angle.set(26)
    # ラジオボタン作成
    rdo2_1 = tk.Radiobutton(input_frame, value=13, variable=viewing_angle, text='小円視野角：1度')
    rdo2_1.place(x=10, y=80)
    rdo2_2 = tk.Radiobutton(input_frame, value=26, variable=viewing_angle, text='小円視野角：2度')
    rdo2_2.place(x=10, y=100)
    rdo2_3 = tk.Radiobutton(input_frame, value=52, variable=viewing_angle, text='小円視野角：4度')
    rdo2_3.place(x=10, y=120)

    # Escapeキーによる強制終了 #
    input_frame.bind('<Escape>', exit)


    ################
    # 測定開始前画面
    ################
    # pre_test_frameの作成と設置
    pre_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_test_frame.grid(row=0, column=0, sticky='nsew')

    # 各種ウィジェットの作成
    '''
    label_pre_test_frame_1 = ttk.Label(pre_test_frame_1, text='■キー操作\n「8」キー：明るさアップ\n「2」キー：明るさダウン\n「Enter」キー：まぶしいと感じたところで押す\n',\
     foreground='gray', background='black', font=('MSゴシック', '20'))

    # ウィジェットの設置
    label_pre_test_frame_1.place(x = 100, y = 100)
    '''

    # Nキーによる測定開始 #
    pre_test_frame.bind('<Key-N>', to_white_b_test_frame)
    pre_test_frame.bind('<Key-n>', to_white_b_test_frame)

    # Escapeキーによる強制終了 #
    pre_test_frame.bind('<Escape>', exit)


    ################
    # ホワイト(B)決定画面
    ################
    # 測定画面1の作成と設置
    white_b_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    white_b_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    white_b_test_frame.bind('<Key-8>', white_b_test_increase_circle_brightness)
    white_b_test_frame.bind('<Key-2>', white_b_test_decrease_circle_brightness)
    white_b_test_frame.bind('<Return>', white_b_test_too_bright_now)

    # Escapeキーによる強制終了 #
    white_b_test_frame.bind('<Escape>', exit)


    ################
    # ホワイト(RG)決定前画面
    ################
    # pre_white_rg_test_frameの作成と設置
    pre_white_rg_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_white_rg_test_frame.grid(row=0, column=0, sticky='nsew')

    # Nキーによる測定開始 #
    pre_white_rg_test_frame.bind('<Key-N>', to_white_rg_test_frame)
    pre_white_rg_test_frame.bind('<Key-n>', to_white_rg_test_frame)

    # Escapeキーによる強制終了 #
    pre_white_rg_test_frame.bind('<Escape>', exit)


    ################
    # ホワイト(RG)決定画面
    ################
    # 測定画の作成と設置
    white_rg_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    white_rg_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    white_rg_test_frame.bind('<Key-8>', white_rg_test_increase_small_circle_brightness)
    white_rg_test_frame.bind('<Key-2>', white_rg_test_decrease_small_circle_brightness)
    white_rg_test_frame.bind('<Return>', white_rg_test_too_bright_now)

    # Escapeキーによる強制終了 #
    white_rg_test_frame.bind('<Escape>', exit)


    ################
    # G決定前画面
    ################
    # pre_g_test_frameの作成と設置
    pre_g_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_g_test_frame.grid(row=0, column=0, sticky='nsew')

    # Nキーによる測定開始 #
    pre_g_test_frame.bind('<Key-N>', to_g_test_frame)
    pre_g_test_frame.bind('<Key-n>', to_g_test_frame)

    # Escapeキーによる強制終了 #
    pre_g_test_frame.bind('<Escape>', exit)


    ################
    # G決定画面
    ################
    # 測定画の作成と設置
    g_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    g_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    g_test_frame.bind('<Key-2>', g_test_increase_small_circle_brightness)
    g_test_frame.bind('<Key-8>', g_test_decrease_small_circle_brightness)
    g_test_frame.bind('<Return>', g_test_i_can_see_now)

    # Escapeキーによる強制終了 #
    g_test_frame.bind('<Escape>', exit)


    ################
    # R決定前画面
    ################
    # pre_r_test_frameの作成と設置
    pre_r_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_r_test_frame.grid(row=0, column=0, sticky='nsew')

    # Nキーによる測定開始 #
    pre_r_test_frame.bind('<Key-N>', to_r_test_frame)
    pre_r_test_frame.bind('<Key-n>', to_r_test_frame)

    # Escapeキーによる強制終了 #
    pre_r_test_frame.bind('<Escape>', exit)


    ################
    # R決定画面
    ################
    # 測定画面の作成と設置
    r_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    r_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    r_test_frame.bind('<Key-2>', r_test_increase_small_circle_brightness)
    r_test_frame.bind('<Key-8>', r_test_decrease_small_circle_brightness)
    r_test_frame.bind('<Return>', r_test_i_can_see_now)

    # Escapeキーによる強制終了 #
    r_test_frame.bind('<Escape>', exit)


    ################
    # B決定前画面
    ################
    # pre_b_test_frameの作成と設置
    pre_b_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_b_test_frame.grid(row=0, column=0, sticky='nsew')

    # Nキーによる測定開始 #
    pre_b_test_frame.bind('<Key-N>', to_b_test_frame)
    pre_b_test_frame.bind('<Key-n>', to_b_test_frame)

    # Escapeキーによる強制終了 #
    pre_b_test_frame.bind('<Escape>', exit)


    ################
    # B決定画面
    ################
    # 測定画面の作成と設置
    b_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    b_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    b_test_frame.bind('<Key-2>', b_test_increase_small_circle_brightness)
    b_test_frame.bind('<Key-8>', b_test_decrease_small_circle_brightness)
    b_test_frame.bind('<Return>', b_test_i_can_see_now)

    # Escapeキーによる強制終了 #
    b_test_frame.bind('<Escape>', exit)


    ################
    # RG決定前画面
    ################
    # pre_rg_test_frameの作成と設置
    pre_rg_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_rg_test_frame.grid(row=0, column=0, sticky='nsew')

    # Nキーによる測定開始 #
    pre_rg_test_frame.bind('<Key-N>', to_rg_test_frame)
    pre_rg_test_frame.bind('<Key-n>', to_rg_test_frame)

    # Escapeキーによる強制終了 #
    pre_rg_test_frame.bind('<Escape>', exit)


    ################
    # RG決定画面
    ################
    # 測定画面の作成と設置
    rg_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    rg_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    rg_test_frame.bind('<Key-2>', rg_test_increase_small_circle_brightness)
    rg_test_frame.bind('<Key-8>', rg_test_decrease_small_circle_brightness)
    rg_test_frame.bind('<Return>', rg_test_i_can_see_now)

    # Escapeキーによる強制終了 #
    rg_test_frame.bind('<Escape>', exit)


    ################
    # 測定終了画面
    ################
    # end_frameの作成と設置
    end_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    end_frame.grid(row=0, column=0, sticky='nsew')

    '''
    # 各種ウィジェットの作成
    label_end_frame = ttk.Label(end_frame, text='測定が終了しました。\nお疲れ様でした。', foreground='gray', background='black', font=('MSゴシック', '20'))

    # 各種ウィジェットの設置
    label_end_frame.place(x = 100, y = 100)
    '''

    # 「Esc」キーで終了
    end_frame.bind('<Escape>', program_end)


    ################
    # プログラムの開始処理
    ################
    # input_frameを前面にする
    input_frame.tkraise()
    input_frame.focus_set()

    root.mainloop()
