import pandas as pd

adress = [{"name": "Issam", "lastname": "Hariri"},
        {"name": "Mario", "lastname": "Rudolf"},
        {"name":  "Hekmat", "lastname": "Hejsan"},
        {"name": "Laslo", "lastname": "Frickle"}]



data = pd.DataFrame(adress)
print(data)