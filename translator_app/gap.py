import pandas as pd
import os

# Fayl yo‘llarini olish
current_dir = os.path.dirname(os.path.abspath(__file__))
umumiy_path = os.path.join(current_dir, "umumiy.xlsx")
qoshimchalar_path = os.path.join(current_dir, "q.xlsx")

# Excel fayllarni o‘qish
umumiy_df = pd.read_excel(umumiy_path, header=None)
qoshimchalar_df = pd.read_excel(qoshimchalar_path, header=None)

# Ustun nomlash
umumiy_df.columns = ['sheva', 'adabiy', 'tuman']
qoshimchalar_df.columns = ['adabiy_qoshimcha', 'sheva_qoshimcha']

# Ma’lumotlarni tozalash
umumiy_df['adabiy'] = umumiy_df['adabiy'].astype(str).str.strip().str.lower()
umumiy_df['sheva'] = umumiy_df['sheva'].astype(str).str.strip().str.lower()
umumiy_df['tuman'] = umumiy_df['tuman'].astype(str).str.strip()

qoshimchalar_df['adabiy_qoshimcha'] = qoshimchalar_df['adabiy_qoshimcha'].astype(str).str.strip().str.lower()
qoshimchalar_df['sheva_qoshimcha'] = qoshimchalar_df['sheva_qoshimcha'].astype(str).str.strip().str.lower()

# Qo‘shimchalarni uzunlik bo‘yicha kamayish tartibida saralaymiz (eng uzunlar birinchi)
qoshimchalar_df = qoshimchalar_df.sort_values(by='adabiy_qoshimcha', key=lambda x: x.str.len(), ascending=False)

# Foydalanuvchi kiritgan gap
def uz_to_kh_sentence(gap):
    sozlar = gap.strip().split()

    natijalar = []
    shevadagi_gap = []

    for soz in sozlar:
        soz_lower = soz.lower().strip()
        topildi = False
        sheva_soz = soz_lower
        qoshilgan_qoshimchalar = ""

        # 1. Bazada to‘g‘ridan-to‘g‘ri topilsa
        moslar = umumiy_df[umumiy_df['adabiy'] == soz_lower]
        if not moslar.empty:
            for _, row in moslar.iterrows():
                natijalar.append(f"{soz} → {row['sheva']} ({row['tuman']})")
            shevadagi_gap.append(moslar.iloc[0]['sheva'])
            continue

        # 2. Qo‘shimchalarni ajratib, asosni bazadan qidiramiz
        qolgan = soz_lower
        sheva_qoshimchalar = ""
        while True:
            topildi_qosh = False
            for _, row_q in qoshimchalar_df.iterrows():
                adabiy_qosh = row_q['adabiy_qoshimcha']
                sheva_qosh = row_q['sheva_qoshimcha']
                if qolgan.endswith(adabiy_qosh):
                    qolgan = qolgan[:-len(adabiy_qosh)]
                    sheva_qoshimchalar = sheva_qosh + sheva_qoshimchalar
                    topildi_qosh = True
                    break
            if not topildi_qosh:
                break

        mos_asoslar = umumiy_df[umumiy_df['adabiy'] == qolgan]
        if not mos_asoslar.empty:
            for _, row in mos_asoslar.iterrows():
                full_sheva = row['sheva'] + sheva_qoshimchalar
                natijalar.append(f"{soz} → {full_sheva} ({row['tuman']})")
            shevadagi_gap.append(mos_asoslar.iloc[0]['sheva'] + sheva_qoshimchalar)
        else:
            if sheva_qoshimchalar:
                full_sheva = qolgan + sheva_qoshimchalar
                natijalar.append(f"{soz} → {full_sheva} (asos topilmadi, faqat qo‘shimchalar o‘zgartirildi)")
                shevadagi_gap.append(full_sheva)
            else:
                natijalar.append(f"{soz} → {soz} (topilmadi)")
                shevadagi_gap.append(soz)

    result = ""
    # Natijani chiqarish
    result += "<br>Natijalar:"
    for natija in natijalar:
        result += f"<br>{natija}"

    result += "<br>Xorazm shevasidagi shakli:"
    result += " ".join(shevadagi_gap)

    return result
