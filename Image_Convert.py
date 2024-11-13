from PIL import Image, ImageOps


def one2one(image, margin, mode):
    width, height = image.size
    print(margin)
    new_size = max(width, height) + (margin * 2)

    if mode == 'light':
        square_image = ImageOps.pad(image, (new_size, new_size), color="white", centering=(0.5, 0.5))
    else:
        square_image = ImageOps.pad(image, (new_size, new_size), color="black", centering=(0.5, 0.5))

    square_image.convert('RGB')
    return square_image


def four2five(image, margin, mode):
    # 원본 이미지의 가로, 세로 크기 가져오기
    #그렇지
    width, height = image.size
    target_ratio = 4 / 5

    # 세로가 더 긴 경우
    if height / width > target_ratio:
        new_width = int(height * target_ratio)
        new_height = height
    else:  # 가로 더 긴 경우: 가로를 맞추고 세로에 여백 추가
        new_width = width
        new_height = int(width / target_ratio)

    # 여백을 추가하여 5:4 비율의 이미지 만들기
    if mode == 'light':
        final_image = ImageOps.pad(image, (new_width, new_height), color="white", centering=(0.5, 0.5))
    else:
        final_image = ImageOps.pad(image, (new_width, new_height), color="black", centering=(0.5, 0.5))

    return final_image


def five2four(image, margin, mode):
    # 원본 이미지의 가로, 세로 크기 가져오기
    width, height = image.size
    target_ratio = 5 / 4

    # 세로가 더 긴 경우
    if height / width > target_ratio:
        new_width = int(height * target_ratio)
        new_height = height
    else:  # 가로 더 긴 경우: 가로를 맞추고 세로에 여백 추가
        new_width = width
        new_height = int(width / target_ratio)

    # 여백을 추가하여 5:4 비율의 이미지 만들기
    if mode == 'light':
        final_image = ImageOps.pad(image, (new_width, new_height), color="white", centering=(0.5, 0.5))
    else:
        final_image = ImageOps.pad(image, (new_width, new_height), color="black", centering=(0.5, 0.5))

    return final_image
