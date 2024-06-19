from PIL import Image

pfp_1 = Image.open('pfp_1.png')
pfp_2 = Image.open('pfp_2.png')
bg = Image.open('bg.png')


bg_img = bg.convert("RGBA")
pfp_1_img = pfp_1.convert("RGBA")
pfp_2_img = pfp_2.convert("RGBA")


pos1 = (0, 0)
pos2 = (200, 0)


bg_img.paste(pfp_1_img, pos1, pfp_1_img)
bg_img.paste(pfp_2_img, pos2, pfp_2_img)


bg_img.save('result_image.png')
