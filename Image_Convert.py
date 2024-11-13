from PIL import Image, ImageOps


def one2one(image, margin, mode):
    width, height = image.size
    new_size = max(width, height)

    if mode == 'light':
        square_image = ImageOps.pad(image, (new_size, new_size), color="white", centering=(0.5, 0.5))
        square_image = ImageOps.pad(square_image, (new_size+margin*2, new_size+margin*2), color="white", centering=(0.5, 0.5))
    else:
        square_image = ImageOps.pad(image, (new_size, new_size), color="black", centering=(0.5, 0.5))
        square_image = ImageOps.pad(square_image, (new_size+margin*2, new_size+margin*2), color="white", centering=(0.5, 0.5))

    square_image.convert('RGB')
    return square_image


# 가로가 4, 세로가 5
def four2five(image, margin, mode):
    # 원본 이미지의 가로, 세로 크기 가져오기
    width, height = image.size
    target_ratio = 4 / 5

    # 가로가 더 긴 경우
    if width / height > target_ratio:
        new_width = width
        new_height = int(width / target_ratio)
        garo_margin = margin*target_ratio
        sero_margin = margin
    else:  # 세로가 더 긴 경우
        new_width = int(height * target_ratio)
        new_height = height
        garo_margin = margin*target_ratio
        sero_margin = margin*target_ratio

    # 여백을 추가하여 5:4 비율의 이미지 만들기
    if mode == 'light':
        final_image = ImageOps.pad(image, (new_width, new_height), color="white", centering=(0.5, 0.5))
    else:
        final_image = ImageOps.pad(image, (new_width, new_height), color="black", centering=(0.5, 0.5))

    return final_image


# 가로가 5, 세로가 4
def five2four(image, margin, mode):
    # 원본 이미지의 가로, 세로 크기 가져오기
    width, height = image.size
    target_ratio = 5 / 4

    # 가로가 더 긴 경우
    if width / height > target_ratio:
        new_width = width
        new_height = int(width / target_ratio)
    else:  # 세로가 더 긴 경우
        new_width = int(height * target_ratio)
        new_height = height

    # 여백을 추가하여 5:4 비율의 이미지 만들기
    if mode == 'light':
        final_image = ImageOps.pad(image, (new_width, new_height), color="white", centering=(0.5, 0.5))
    else:
        final_image = ImageOps.pad(image, (new_width, new_height), color="black", centering=(0.5, 0.5))

    return final_image
