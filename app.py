import os
from PIL import Image
import math
import streamlit as st

def delete_files(path):
    for filename in get_all_file_paths(path):
        try:
            print(filename)
            os.remove(filename)
        except:
            pass

def get_all_file_paths(dir_path):
    file_paths = []
    for root, dir_path, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def resize_image(file_path, save_path, width, height):
    im = Image.open(file_path)
    w, h = im.size
    if w < width and h < height:
        return True
    im.thumbnail((width, height), Image.LANCZOS)
    im.save(save_path)

def create_filled_image(width, height, color):
    # 新しい画像を作成（RGBモード、指定サイズ、指定色）
    image = Image.new('RGB', (width, height), color)
    return image

def create_image_grid(images, rows, cols):
    if len(images) != rows * cols:
        raise ValueError("画像の数と行・列の数が一致しません。")

    # 1枚目の画像を基準にサイズを決定
    width, height = images[0].size
    grid_image = Image.new('RGB', (cols * width, rows * height))

    for i, image in enumerate(images):
        row = i // cols
        col = i % cols
        grid_image.paste(image, (col * width, row * height))

    return grid_image

def main():
    dir_path = "./image"
    resize_path = "./resize"
    delete_files(dir_path)
    delete_files(resize_path)

    st.subheader('スクショを1枚の画像に並べるアプリ（for X）ver.0.1')

    user_number = st.number_input("列数(横に並べる数)を入力してください", min_value=1, max_value=100, value=5, step=1)
    color = st.color_picker('背景色を選択してください', "#000000")

    # 複数ファイルのアップロード
    uploaded_files = st.file_uploader("画像ファイルをアップロード", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            image = Image.open(uploaded_file)
            file_path = os.path.join(dir_path, file_name)
            image.save(file_path)

        files = get_all_file_paths(dir_path)
        print(files)

        for i, file in enumerate(files):
            resize_image(file, f'{resize_path}/output{i}.png', 300, 4096)

        files = get_all_file_paths(resize_path)

        if len(files) == 0:
            return True

        num = len(files)
        col = user_number

        rem = num % col
        row = math.ceil(num / col)
        print(num, rem, row, col)

        im = Image.open(f'{resize_path}/output{i}.png')
        width, height = im.size
        if rem != 0:
            for i in range(col - rem):
                filled_image = create_filled_image(width, height, color)
                filled_image.save(f'{resize_path}/outputs{i}.png')

        # 画像を読み込む
        files = get_all_file_paths(resize_path)
        images = [Image.open(path) for path in files]

        # 2x2のタイル状に配置
        grid_image = create_image_grid(images, rows=row, cols=col)

        # グリッド画像を保存する
        grid_image.save('grid_image.png')
        resize_image(file, 'grid_image.png', 4096, 4096)


        # ダウンロード
        st.download_button('ダウンロード', open('grid_image.png', 'br'), "grid_1.png")

        os.remove("grid_image.png")

        delete_files(dir_path)
        delete_files(resize_path)

    url = "https://x.com/ta_ta_ta_nu_ki"
    st.write("Copyright © 2024 [たたたぬき](%s) #たぬきツール" % url)

if __name__ == '__main__':
    main()
