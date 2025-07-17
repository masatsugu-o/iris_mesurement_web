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

# # weber_testをインポート
# import weber_test as wb


#########################
# RGB値を16進数に変換
#########################
def from_rgb_to_colorcode(rgb):
    return '#%02x%02x%02x' % rgb


#########################
# 測定画像を描画
#########################
def drawing_test_image(big_r, big_g, big_b, target_r, target_g ,target_b):

    # 大円の半径を設定(ディスプレイ縦の半分)
    big_circle_radius = 540

    # 中円の半径を設定
    mid_circle_radius = 30

    # 横方向位置（ディスプレイ横の半分）
    offset_x=960

    # 縦方向位置（ディスプレイの縦の半分）
    offset_y=540

    # 輝度を変化させる小円の半径を設定
    target_radius = viewing_angle.get()

    # 円の中央からの横位置
    distance = 0

    global my_canvas, measure_num, measure_num_to_selecter, Title

    # 描画前に表示していた内容を消す
    my_canvas.delete('all')

    # 大円を描画
    my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, fill=from_rgb_to_colorcode((big_r, big_g, big_b)))
    if measure_num_to_selecter[0][measure_num] == 11:
        if measure_num == 1:
            big_r_inner = big_r
            big_g_inner = big_g
            big_b_inner = big_b
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner)))
        elif measure_num == 2:
            big_r_inner = 16
            big_g_inner = big_g
            big_b_inner = big_b
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner))) 
        elif measure_num == 3:
            big_r_inner = big_r
            big_g_inner = 16
            big_b_inner = big_b
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner))) 
        elif measure_num == 4:
            big_r_inner = big_r
            big_g_inner = big_g
            big_b_inner = 16
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner))) 
        elif measure_num == 5:
            big_r_inner = big_r
            big_g_inner = 16
            big_b_inner = 16
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner))) 
        elif measure_num == 6:
            big_r_inner = 16
            big_g_inner = big_g
            big_b_inner = 16
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner)))                                                    
        else:
            big_r_inner = 16
            big_g_inner = 16
            big_b_inner = big_b
            my_canvas.create_oval(offset_x + distance - big_circle_radius, offset_y - big_circle_radius, offset_x + distance + big_circle_radius, offset_y + big_circle_radius, width=0, \
                                  fill=from_rgb_to_colorcode((big_r_inner, big_g_inner, big_b_inner)))      
        
    # # 中円を描画
    # if measure_num_to_selecter[0][measure_num] >= 4:
    #     my_canvas.create_oval(960 + distance - mid_circle_radius, 540 - mid_circle_radius, 960 + distance + mid_circle_radius, 540 + mid_circle_radius, width=0, fill=from_rgb_to_colorcode((0, 0, 0)))
    
    # 小円を描画
    #my_canvas.create_oval(960 + distance - target_radius, 540 - target_radius, 960 + distance + target_radius, 540 + target_radius, width=0, fill=from_rgb_to_colorcode((target_r, target_g ,target_b)))


    # 動作確認用
    # current_data_text = '大円RGB: R ' + str(big_r) + ' G ' + str(big_g) + ' B ' + str(big_b) + '  小円RGB: R ' + str(target_r) + ' G ' + str(target_g) + ' B ' + str(target_b) 
    # my_canvas.create_text(10, 1080-30, text=current_data_text, anchor="nw", font=("MSゴシック", 20), fill="white")


    # キャンパスを描画
    my_canvas.pack()

    # # 文字(テストプログラム)
    # # バックグラウンドはRGBの16進数表示なので、255などの値を16進数変換して文字列にすれば良い
    # hex_r=hex(target_r)
    # hex_g=hex(target_g)
    # hex_b=hex(target_b)
    # hex_r = hex_r[2:]
    # hex_g = hex_g[2:]
    # hex_b = hex_b[2:]
    # title_bg = '#'+str(hex_r)+str(hex_g)+str(hex_b)
    # gain=5
    # title_size = round(5+(60-5)/255*(target_r-16)*gain)
    # print(title_size)
    # if measure_num_to_selecter[0][measure_num] == 0:
    #     tango="こねこ"
    # elif measure_num_to_selecter[0][measure_num] == 1:
    #     tango = "かえる"
    # else:
    #     tango = "さかな"
    # Title = tk.Label(my_canvas, text=tango, font=("MSゴシック", str(title_size), "bold"), background=title_bg)
    # Title.pack()
    # Title.place(x=960, y=540)

    # 文字(本番)
    # バックグラウンドはRGBの16進数表示なので、255などの値を16進数変換して文字列にすれば良い
    if measure_num_to_selecter[0][measure_num] == 11:
        Title.destroy()
        hex_r=hex(big_r_inner)
        hex_g=hex(big_g_inner)
        hex_b=hex(big_b_inner)
        hex_r = hex_r[2:]
        hex_g = hex_g[2:]
        hex_b = hex_b[2:]
        title_bg = '#'+str(hex_r)+str(hex_g)+str(hex_b)
        gain=5
        title_size = round(5+(60-5)/255*(target_r-20)*gain)
        #print(title_bg)
        # if measure_num == 1:
        #     tango="ねずみ"
        # elif measure_num == 2:
        #     tango = "こぐま"
        # elif measure_num == 3:
        #     tango = "ごりら"
        # elif measure_num == 4:
        #     tango = "ぱんだ"
        # elif measure_num == 5:
        #     tango = "きつね"
        # elif measure_num == 6:
        #     tango = "きりん"                                                   
        # else:
        #     tango = "たぬき"
        # if measure_num == 1:
        #     tango="ねずみ"
        # elif measure_num == 5:
        #     tango = "こぐま"
        # elif measure_num == 6:
        #     tango = "ごりら"
        # elif measure_num == 7:
        #     tango = "ぱんだ"
        # elif measure_num == 2:
        #     tango = "きつね"
        # elif measure_num == 3:
        #     tango = "きりん"                                                   
        # else:
        #     tango = "たぬき"
        # if measure_num == 1:
        #     tango="ねずみ"
        # elif measure_num == 2:
        #     tango = "こぐま"
        # elif measure_num == 3:
        #     tango = "つばめ"
        # elif measure_num == 4:
        #     tango = "ぱんだ"
        # elif measure_num == 5:
        #     tango = "こざる"
        # elif measure_num == 6:
        #     tango = "すずめ"                                                   
        # else:
        #     tango = "ごりら"
        #tango = "pppqppp\nuuunuuu"
        tango = "ぎんぎん　ぎらぎら　ゆうひが　しずむ\n\nぎんぎん　ぎらぎら　ひが　しずむ" 
        # Title = tk.Label(my_canvas, text=tango, font=("MSゴシック", str(title_size+10), "bold"), background=title_bg)
        # Title.pack()
        # Title.place(x=960-title_size*2, y=540-title_size)
        # Title.destroy()                              
        Title = tk.Label(my_canvas, text=tango, font=("MSゴシック", str(title_size)), background=title_bg)
        Title.pack()
        Title.place(x=offset_x-title_size*10, y=offset_y-title_size)    


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
# ファイル書き込み
#########################
def file_write(test_name, dai_r, dai_g, dai_b, syo_r, syo_g, syo_b):
        global result
        # 決定結果を配列に格納
        tmp_result[0]['test_name'] = test_name
        tmp_result[0]['big_r'] = dai_r
        tmp_result[0]['big_g'] = dai_g
        tmp_result[0]['big_b'] = dai_b
        tmp_result[0]['big_r_per'] = (dai_r/255) ** 2.2 * 100
        tmp_result[0]['big_g_per'] = (dai_g/255) ** 2.2 * 100
        tmp_result[0]['big_b_per'] = (dai_b/255) ** 2.2 * 100
        tmp_result[0]['target_r'] = syo_r
        tmp_result[0]['target_g'] = syo_g
        tmp_result[0]['target_b'] = syo_b
        tmp_result[0]['target_r_per'] =  (syo_r/255) ** 2.2 * 100
        tmp_result[0]['target_g_per'] =  (syo_g/255) ** 2.2 * 100
        tmp_result[0]['target_b_per'] =  (syo_b/255) ** 2.2 * 100
        tmp_result[0]['time'] = get_elapsed_time()

        # tmp_result配列を、result配列に追加
        result = np.concatenate((result, tmp_result), axis = 0)


#########################
# プログラム終了時に実行
#########################
def program_end(event):
    # プログラム終了
    sys.exit()




#########################
# 測定画面へ移動時に実行
#########################
def to_test_frame(event, test_frame, dai_r, dai_g, dai_b, syo_r, syo_g, syo_b):
    # 4K対応でキャンバスサイズを3840×2160に変更
    global my_canvas, kondousyoku_center, kondousyoku_target, kondousyoku_num, Title
    my_canvas = tk.Canvas(test_frame, bg='black', height=2160, width=3840, highlightthickness=0)

    # ここで一旦Titleオブジェクトを作っておくと、drawing_test_imageでdestoryできる
    Title = tk.Label(my_canvas, text="testtesttest", font=("MSゴシック", 60, "bold"), background="#ffffff")

    # テスト画像を描画
    if measure_num_to_selecter[0][measure_num] == 11:
        syo_r = 16
    drawing_test_image(dai_r, dai_g, dai_b, syo_r, syo_g, syo_b)
    if measure_num_to_selecter[0][measure_num] == 4:
        drawing_test_image(kondousyoku_center[kondousyoku_num][0], kondousyoku_center[kondousyoku_num][1], kondousyoku_center[kondousyoku_num][2], \
                           kondousyoku_center[kondousyoku_num][0], kondousyoku_center[kondousyoku_num][1], kondousyoku_center[kondousyoku_num][2])
    elif measure_num_to_selecter[0][measure_num] == 5:
        drawing_test_image(kondousyoku_target[kondousyoku_num][0], kondousyoku_target[kondousyoku_num][1], kondousyoku_target[kondousyoku_num][2], \
                           kondousyoku_target[kondousyoku_num][0], kondousyoku_target[kondousyoku_num][1], kondousyoku_target[kondousyoku_num][2]) 
    # elif measure_num_to_selecter[0][measure_num] == 11:
    #     drawing_test_image(dai_r, dai_g, dai_b, 16, syo_g, syo_b)       

    test_frame.tkraise()
    test_frame.focus_set()

    # 大円の輝度の測定開始時刻を記録
    global time_start
    time_start = time.perf_counter()


##########################
# 測定画面で2キー押下時に実行：小円の輝度アップ（ホワイトは反対なことに注意）
#########################
def test_increase_small_circle_brightness(event):
    global measure_num_to_selecter, tmp_r, tmp_g, tmp_b, measure_num, kondousyoku_center, kondousyoku_target, kondousyoku_num 
    
    if measure_num_to_selecter[0][measure_num] == 0:
        #global tmp_r, tmp_g, tmp_b
        # アーレン用に下限を設定　0⇒17 16だと色がでない 
        if tmp_r - 1 >= 20:
            tmp_r -= 1
            tmp_g -= 1
            tmp_b -= 1
            drawing_test_image(tmp_r, tmp_g, tmp_b, tmp_r, tmp_g, tmp_b)
    elif measure_num_to_selecter[0][measure_num] == 1:
        #global tmp_g
        if tmp_g + 1 <= max_g:
           tmp_g += 1
           drawing_test_image(max_r, max_g, max_b, max_r, tmp_g, max_b)
    elif measure_num_to_selecter[0][measure_num] == 2:
        #global tmp_r
        if tmp_r + 1 <= max_r:
           tmp_r += 1
           drawing_test_image(max_r, max_g, max_b, tmp_r, max_g, max_b)
    elif measure_num_to_selecter[0][measure_num] == 3:
        #global tmp_b
        if tmp_b + 1 <= max_b:
           tmp_b += 1
           drawing_test_image(max_r, max_g, max_b, max_r, max_g, tmp_b) 
    elif measure_num_to_selecter[0][measure_num] == 4:
        if tmp_r + 1 <= kondousyoku_center[kondousyoku_num][0]:
            tmp_r += 1
            tmp_g = round(kondousyoku_target[kondousyoku_num][1]+(kondousyoku_center[kondousyoku_num][1]-kondousyoku_target[kondousyoku_num][1])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            tmp_b = round(kondousyoku_target[kondousyoku_num][2]+(kondousyoku_center[kondousyoku_num][2]-kondousyoku_target[kondousyoku_num][2])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            drawing_test_image(kondousyoku_center[kondousyoku_num][0], kondousyoku_center[kondousyoku_num][1], kondousyoku_center[kondousyoku_num][2], tmp_r, tmp_g, tmp_b)             
            # tmp_g = round(kondousyoku_target[0][1]+(kondousyoku_center[0][1]-kondousyoku_target[0][1])/(kondousyoku_center[0][0]-kondousyoku_target[0][0])*(tmp_r-kondousyoku_target[0][0]))
            # tmp_b = round(kondousyoku_target[0][2]+(kondousyoku_center[0][2]-kondousyoku_target[0][2])/(kondousyoku_center[0][0]-kondousyoku_target[0][0])*(tmp_r-kondousyoku_target[0][0]))
            # drawing_test_image(kondousyoku_center[0][0], kondousyoku_center[0][1], kondousyoku_center[0][2], tmp_r, tmp_g, tmp_b)
    elif measure_num_to_selecter[0][measure_num] == 5:
        if tmp_r - 1 >= kondousyoku_target[kondousyoku_num][0]:
            tmp_r -= 1
            tmp_g = round(kondousyoku_target[kondousyoku_num][1]+(kondousyoku_center[kondousyoku_num][1]-kondousyoku_target[kondousyoku_num][1])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            tmp_b = round(kondousyoku_target[kondousyoku_num][2]+(kondousyoku_center[kondousyoku_num][2]-kondousyoku_target[kondousyoku_num][2])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            drawing_test_image(kondousyoku_target[kondousyoku_num][0], kondousyoku_target[kondousyoku_num][1], kondousyoku_target[kondousyoku_num][2], tmp_r, tmp_g, tmp_b) 
    elif measure_num_to_selecter[0][measure_num] == 11:
        if tmp_r -1 >= 16:
            tmp_r -= 1
            drawing_test_image(max_r, max_g, max_b, tmp_r, max_g, max_b)


                  
         
#########################
# 測定画面で8キー押下時に実行：小円の輝度ダウン（ホワイトは反対なことに注意）
#########################
def test_decrease_small_circle_brightness(eventr):
    global measure_num_to_selecter, tmp_r, tmp_g, tmp_b, measure_num, kondousyoku_center, kondousyoku_target

    if measure_num_to_selecter[0][measure_num] == 0:
        #global tmp_r, tmp_g, tmp_b
        if tmp_r + 1 <= 255:
            tmp_r += 1
            tmp_g += 1
            tmp_b += 1
            drawing_test_image(tmp_r, tmp_g, tmp_b, tmp_r, tmp_g, tmp_b)
    elif measure_num_to_selecter[0][measure_num] == 1:
        #global tmp_g
        if tmp_g - 1 >= 0:
            tmp_g -= 1
            drawing_test_image(max_r, max_g, max_b, max_r, tmp_g, max_b) 
    elif measure_num_to_selecter[0][measure_num] == 2:
        #global tmp_r
        if tmp_r - 1 >= 0:
            tmp_r -= 1
            drawing_test_image(max_r, max_g, max_b, tmp_r, max_g, max_b)
    elif measure_num_to_selecter[0][measure_num] == 3:
        #global tmp_b
        if tmp_b - 1 >= 0:
            tmp_b -= 1
            drawing_test_image(max_r, max_g, max_b, max_r, max_g, tmp_b) 
    elif measure_num_to_selecter[0][measure_num] == 4:
        if tmp_r - 1 >= kondousyoku_target[kondousyoku_num][0]:
            tmp_r -= 1
            tmp_g = round(kondousyoku_target[kondousyoku_num][1]+(kondousyoku_center[kondousyoku_num][1]-kondousyoku_target[kondousyoku_num][1])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            tmp_b = round(kondousyoku_target[kondousyoku_num][2]+(kondousyoku_center[kondousyoku_num][2]-kondousyoku_target[kondousyoku_num][2])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            drawing_test_image(kondousyoku_center[kondousyoku_num][0], kondousyoku_center[kondousyoku_num][1], kondousyoku_center[kondousyoku_num][2], tmp_r, tmp_g, tmp_b) 
            # tmp_g = round(226+(55-226)/(250-102)*(tmp_r-102))
            # tmp_b = round(90+(26-90)/(250-102)*(tmp_r-102))
            # drawing_test_image(250, 55, 26, tmp_r, tmp_g, tmp_b)
    elif measure_num_to_selecter[0][measure_num] == 5:
        if tmp_r + 1 <= kondousyoku_center[kondousyoku_num][0]:
            tmp_r += 1
            tmp_g = round(kondousyoku_target[kondousyoku_num][1]+(kondousyoku_center[kondousyoku_num][1]-kondousyoku_target[kondousyoku_num][1])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            tmp_b = round(kondousyoku_target[kondousyoku_num][2]+(kondousyoku_center[kondousyoku_num][2]-kondousyoku_target[kondousyoku_num][2])/ \
                          (kondousyoku_center[kondousyoku_num][0]-kondousyoku_target[kondousyoku_num][0])*(tmp_r-kondousyoku_target[kondousyoku_num][0]))
            drawing_test_image(kondousyoku_target[kondousyoku_num][0], kondousyoku_target[kondousyoku_num][1], kondousyoku_target[kondousyoku_num][2], tmp_r, tmp_g, tmp_b)
    elif measure_num_to_selecter[0][measure_num] == 11:
        # フォントの最大値を意識したあっぱバウンドを設定。 max_r ⇒　30
        if tmp_r +1 <= 50:
            tmp_r += 1
            drawing_test_image(max_r, max_g, max_b, tmp_r, max_g, max_b)


#########################
# 測定画面でEnterキー押下時に実行：小円が見えた場合
#########################
def test_i_can_see_now(even):
    global result, tmp_result, measure_num_to_selecter, tmp_r, tmp_g, tmp_b, measure_num, kondousyoku_center, kondousyoku_target, kondousyoku_num

    if measure_num_to_selecter[0][measure_num] ==0:
        global max_b, result, tmp_result, max_r, max_g

        file_write('ホワイト(B)決定結果', tmp_r, tmp_g, tmp_b, tmp_r, tmp_g, tmp_b)

        #ダミーであるresultの最初の行を削除
        result = np.delete(result, 0, axis=0) 

        # Bの値をホワイトの決定値として格納
        max_b = tmp_b
        # RG測定削除に伴い小川追加
        max_r = tmp_r
        max_g = tmp_g

        # 識別文字大きさ測定で追加
        tmp_r=16

        # 測定前画面へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        my_canvas.destroy()
        measure_num=measure_num+1
    elif measure_num_to_selecter[0][measure_num] == 1:
        #global tmp_g

        file_write('緑色視感度測定結果', max_r, max_g, max_b, max_r, tmp_g, max_b)

        # 測定前画面2へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        #my_canvas.delete('all')
        my_canvas.destroy()
        tmp_g=max_g
        measure_num=measure_num+1
    elif measure_num_to_selecter[0][measure_num] == 2:
        #global tmp_r

        file_write('赤色視感度測定結果', max_r, max_g, max_b, tmp_r, max_g, max_b)

        # 測定前画面2へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        #my_canvas.delete('all')
        my_canvas.destroy()
        tmp_r=max_r
        measure_num=measure_num+1
        if measure_num_to_selecter[0][measure_num] == 4:
            tmp_r = kondousyoku_center[kondousyoku_num][0]
            tmp_g = kondousyoku_center[kondousyoku_num][1]
            tmp_b = kondousyoku_center[kondousyoku_num][2]
        if measure_num_to_selecter[0][measure_num] == 5:
            tmp_r = kondousyoku_target[kondousyoku_num][0]
            tmp_g = kondousyoku_target[kondousyoku_num][1]
            tmp_b = kondousyoku_target[kondousyoku_num][2]           
    elif measure_num_to_selecter[0][measure_num] == 3:
        #global tmp_b

        file_write('青色視感度測定結果', max_r, max_g, max_b, max_r, max_g, tmp_b)

         # 測定前画面2へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        #my_canvas.delete('all')
        my_canvas.destroy()
        tmp_b=max_b
        measure_num=measure_num+1
        if measure_num_to_selecter[0][measure_num] == 4:
            tmp_r = kondousyoku_center[kondousyoku_num][0]
            tmp_g = kondousyoku_center[kondousyoku_num][1]
            tmp_b = kondousyoku_center[kondousyoku_num][2]
        if measure_num_to_selecter[0][measure_num] == 5:
            tmp_r = kondousyoku_target[kondousyoku_num][0]
            tmp_g = kondousyoku_target[kondousyoku_num][1]
            tmp_b = kondousyoku_target[kondousyoku_num][2]        

        if measure_num_to_selecter[0][measure_num] == 100: 
            # 結果をCSVファイルに保存
            save_result_file()
            #測定終了画面へ移動
            end_frame.tkraise()
            end_frame.focus_set()
    elif measure_num_to_selecter[0][measure_num] == 4:
        file_write('No.7 foward 測定結果', kondousyoku_center[kondousyoku_num][0], kondousyoku_center[kondousyoku_num][1], kondousyoku_center[kondousyoku_num][2], \
                   tmp_r, tmp_g, tmp_b)

        # 測定前画面2へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        #my_canvas.delete('all')
        my_canvas.destroy()
        tmp_r=max_r
        tmp_g=max_g
        tmp_b=max_b
        measure_num=measure_num+1
        kondousyoku_num=kondousyoku_num+1
        if kondousyoku_num == 6:
            kondousyoku_num=0
        if measure_num_to_selecter[0][measure_num] == 4:
            tmp_r = kondousyoku_center[kondousyoku_num][0]
            tmp_g = kondousyoku_center[kondousyoku_num][1]
            tmp_b = kondousyoku_center[kondousyoku_num][2]
        if measure_num_to_selecter[0][measure_num] == 5:
            tmp_r = kondousyoku_target[kondousyoku_num][0]
            tmp_g = kondousyoku_target[kondousyoku_num][1]
            tmp_b = kondousyoku_target[kondousyoku_num][2]
        if measure_num_to_selecter[0][measure_num] == 100: 
            # 結果をCSVファイルに保存
            save_result_file()
            #測定終了画面へ移動
            end_frame.tkraise()
            end_frame.focus_set()             
    elif measure_num_to_selecter[0][measure_num] == 5:
        file_write('No.7 foward 測定結果', kondousyoku_target[kondousyoku_num][0], kondousyoku_target[kondousyoku_num][1], kondousyoku_target[kondousyoku_num][2], \
                   tmp_r, tmp_g, tmp_b)

        # 測定前画面2へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        #my_canvas.delete('all')
        my_canvas.destroy()
        tmp_r=max_r
        tmp_g=max_g
        tmp_b=max_b
        measure_num=measure_num+1
        kondousyoku_num=kondousyoku_num+1
        if kondousyoku_num == 6:
            kondousyoku_num=0       
        if measure_num_to_selecter[0][measure_num] == 4:
            tmp_r = kondousyoku_center[kondousyoku_num][0]
            tmp_g = kondousyoku_center[kondousyoku_num][1]
            tmp_b = kondousyoku_center[kondousyoku_num][2]        
        if measure_num_to_selecter[0][measure_num] == 5:
            tmp_r = kondousyoku_target[kondousyoku_num][0]
            tmp_g = kondousyoku_target[kondousyoku_num][1]
            tmp_b = kondousyoku_target[kondousyoku_num][2]
        if measure_num_to_selecter[0][measure_num] == 100: 
            # 結果をCSVファイルに保存
            save_result_file()
            #測定終了画面へ移動
            end_frame.tkraise()
            end_frame.focus_set()
    elif measure_num_to_selecter[0][measure_num] == 11:
        file_write('識別文字大きさ測定', max_r, max_g, max_b, tmp_r, max_g, max_b)

        # 測定前画面2へ移動
        pre_wb_test_frame.tkraise()
        pre_wb_test_frame.focus_set()
        #my_canvas.delete('all')
        my_canvas.destroy()
        #tmp_r=max_r
        tmp_r = 16
        measure_num=measure_num+1

        if measure_num_to_selecter[0][measure_num] == 100: 
            # 結果をCSVファイルに保存
            save_result_file()
            #測定終了画面へ移動
            end_frame.tkraise()
            end_frame.focus_set()       
                              


#########################
# メインプログラム
#########################
# or以降は、exe化時のエラー回避のための追加。ファイル名を変更してexe化する場合、修正が必要
if __name__ == '__main__' or __name__ == '__irishue_simple_test_app_v05__':

    ################
    # 測定の設定(配列の値はselecterの値)
    ################
    # selecter=100は測定終了の意味 
    measure_num_to_selecter=np.empty((1,17),int)
    measure_num_to_selecter[0][0]=0
    measure_num_to_selecter[0][1]=11
    measure_num_to_selecter[0][2]=11
    measure_num_to_selecter[0][3]=11
    measure_num_to_selecter[0][4]=11
    #measure_num_to_selecter[0][5]=3 
    measure_num_to_selecter[0][5]=11
    measure_num_to_selecter[0][6]=11
    measure_num_to_selecter[0][7]=11
    measure_num_to_selecter[0][8]=100
    measure_num_to_selecter[0][9]=4
    measure_num_to_selecter[0][10]=5
    measure_num_to_selecter[0][11]=5
    measure_num_to_selecter[0][12]=5
    measure_num_to_selecter[0][13]=5
    measure_num_to_selecter[0][14]=5
    measure_num_to_selecter[0][15]=5
    measure_num_to_selecter[0][16]=100
    measure_num=0

    ################
    # 混同色線の設定(配列の値は座標)
    ################
    kondousyoku_center=np.empty((6,3),int)
    kondousyoku_target=np.empty((6,3),int)
    kondousyoku_num=0
    # No.7
    kondousyoku_center[0][0]=250
    kondousyoku_center[0][1]=55
    kondousyoku_center[0][2]=26
    kondousyoku_target[0][0]=102
    kondousyoku_target[0][1]=226
    kondousyoku_target[0][2]=90
    # No.8
    kondousyoku_center[1][0]=251
    kondousyoku_center[1][1]=28
    kondousyoku_center[1][2]=46
    kondousyoku_target[1][0]=155
    kondousyoku_target[1][1]=155
    kondousyoku_target[1][2]=155
    # No.9
    kondousyoku_center[2][0]=242
    kondousyoku_center[2][1]=37
    kondousyoku_center[2][2]=86
    kondousyoku_target[2][0]=52
    kondousyoku_target[2][1]=130
    kondousyoku_target[2][2]=223
    # No.10
    kondousyoku_center[3][0]=244
    kondousyoku_center[3][1]=62
    kondousyoku_center[3][2]=64
    kondousyoku_target[3][0]=102
    kondousyoku_target[3][1]=226
    kondousyoku_target[3][2]=90
    # No.11
    kondousyoku_center[4][0]=225
    kondousyoku_center[4][1]=44
    kondousyoku_center[4][2]=127
    kondousyoku_target[4][0]=155
    kondousyoku_target[4][1]=155
    kondousyoku_target[4][2]=155
    # No.12
    kondousyoku_center[5][0]=180
    kondousyoku_center[5][1]=28
    kondousyoku_center[5][2]=191
    kondousyoku_target[5][0]=52
    kondousyoku_target[5][1]=130
    kondousyoku_target[5][2]=223      

    # ################
    # # セレクタの設定
    # ################
    # # selecterは測定種別にして、numをインクリメンタル。numとselecterを紐づける
    # selecter=0

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

    # # Nキーによる測定開始 #
    # pre_test_frame.bind('<Key-N>', to_white_b_test_frame)
    # pre_test_frame.bind('<Key-n>', to_white_b_test_frame)
    # Nキーによる測定開始 #
    pre_test_frame.bind('<Key-N>', lambda event: to_test_frame(event, wb_test_frame, tmp_r, tmp_g, tmp_b,\
                                                       tmp_r, tmp_g, tmp_b))
    pre_test_frame.bind('<Key-n>', lambda event: to_test_frame(event, wb_test_frame, tmp_r, tmp_g, tmp_b,\
                                                       tmp_r, tmp_g, tmp_b))
    # Escapeキーによる強制終了 #
    pre_test_frame.bind('<Escape>', exit)


    ################
    # 輝度決定前画面
    ################
    # pre_wb_test_frameの作成と設置
    pre_wb_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    pre_wb_test_frame.grid(row=0, column=0, sticky='nsew')

    # Nキーによる測定開始 #
    # pre_wb_test_frame.bind('<Key-n>', lambda event: to_test_frame(event, wb_test_frame, dai_r, dai_g, dai_b,\
    #                                                    syo_r, syo_g, syo_b))
    pre_wb_test_frame.bind('<Key-N>', lambda event: to_test_frame(event, wb_test_frame, max_r, max_g, max_b,\
                                                       max_r, max_g, max_b))
    pre_wb_test_frame.bind('<Key-n>', lambda event: to_test_frame(event, wb_test_frame, max_r, max_g, max_b,\
                                                       max_r, max_g, max_b))
    # Escapeキーによる強制終了 #
    pre_wb_test_frame.bind('<Escape>', exit)


    ################
    # 輝度決定画面
    ################
    # 測定画の作成と設置
    wb_test_frame = ttk.Frame(root, style='My.TFrame', cursor='none')
    wb_test_frame.grid(row=0, column=0, sticky='nsew')

    # 回答キー入力設定
    wb_test_frame.bind('<Key-2>', lambda event: test_increase_small_circle_brightness(event))
    # wb_test_frame.bind('<Key-2>', lambda event: test_increase_small_circle_brightness(event, max_r, max_g, max_b, max_r, tmp_g, max_b, 1))
    wb_test_frame.bind('<Key-8>', lambda event: test_decrease_small_circle_brightness(event))
    wb_test_frame.bind('<Return>', lambda event: test_i_can_see_now(event))

    # Escapeキーによる強制終了 #
    wb_test_frame.bind('<Escape>', exit)


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
