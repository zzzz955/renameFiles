from PIL import Image

def get_image_datas(image_path):
    # mainwindow에서 이미지 경로를 전달받아 사이즈 값 리턴
    try:
        get_image_val = {}
        for image in image_path:
            img = Image.open(image)
            width, height = img.size
            get_image_val[image] = (width, height)
        return get_image_val
    except Exception as e:
        print(f"Error: {e}")