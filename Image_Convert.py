from PIL import Image, ImageOps

# 1:1 비율 적용 함수
def one2one(image, margin, mode):
    width, height = image.size
    new_size = max(width, height)

    # 이미지에 1:1 비율과 여백을 적용
    if mode == 'light':
        square_image = ImageOps.pad(image, (new_size, new_size), color="white", centering=(0.5, 0.5))
        square_image = ImageOps.expand(square_image, border=margin, fill="white")
    else:
        square_image = ImageOps.pad(image, (new_size, new_size), color="black", centering=(0.5, 0.5))
        square_image = ImageOps.expand(square_image, border=margin, fill="black")

    square_image = square_image.convert('RGB')
    return square_image

# 가로가 4, 세로가 5 비율 적용 함수
def four2five(image, margin, mode):
    width, height = image.size
    target_ratio = 4 / 5

    # 비율을 맞추기 위해 여백을 추가
    if width / height > target_ratio:
        new_height = int(width / target_ratio)
        new_width = width
    else:
        new_width = int(height * target_ratio)
        new_height = height

    # 모드에 따라 이미지 여백과 색상 적용
    if mode == 'light':
        resized_image = ImageOps.pad(image, (new_width, new_height), color="white", centering=(0.5, 0.5))
        final_image = ImageOps.expand(resized_image, border=(margin, margin*int(target_ratio)), fill="white")
    else:
        resized_image = ImageOps.pad(image, (new_width, new_height), color="black", centering=(0.5, 0.5))
        final_image = ImageOps.expand(resized_image, border=(margin, margin*int(target_ratio)), fill="black")

    return final_image

# 가로가 5, 세로가 4 비율 적용 함수
def five2four(image, margin, mode):
    width, height = image.size
    target_ratio = 5 / 4

    # 비율을 맞추기 위해 여백을 추가
    if width / height > target_ratio:
        new_height = int(width / target_ratio)
        new_width = width
    else:
        new_width = int(height * target_ratio)
        new_height = height

    # 모드에 따라 이미지 여백과 색상 적용
    if mode == 'light':
        resized_image = ImageOps.pad(image, (new_width, new_height), color="white", centering=(0.5, 0.5))
        final_image = ImageOps.expand(resized_image, border=(margin*int(target_ratio), margin), fill="white")
    else:
        resized_image = ImageOps.pad(image, (new_width, new_height), color="black", centering=(0.5, 0.5))
        final_image = ImageOps.expand(resized_image, border=(margin*int(target_ratio), margin), fill="black")

    return final_image
