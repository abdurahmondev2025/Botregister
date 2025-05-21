import pandas as pd

# Ma'lumotlar
data = {
    'Ism': ['Ali', 'Vali', 'Gulbahor'],
    'Yosh': [25, 30, 22],
    'Kasb': ['Dasturchi', 'O‘qituvchi', 'Talaba']
}

# DataFrame yaratamiz
df = pd.DataFrame(data)

# Excel faylga yozamiz
df.to_excel('Test_shablon.xlsx', index=False)  # index=False bo‘lsa, tartib raqami yozilmaydi
