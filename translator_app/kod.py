import pandas as pd

# XLSX faylini o'qish
df = pd.read_excel('translator_app/umumiy.xlsx')  # Fayl nomini o'zingiznikiga moslashtiring

def search_adabiy(word):
    # Adabiy so'z (B ustuni) bo'yicha qidirish
    result = df[df['B'].str.lower() == word.lower()]
    if not result.empty:
        for _, row in result.iterrows():
            print(f"{word.lower()} - {row['A'].lower()} - {row['C'].lower()}")
    else:
        print(f"{word.lower()} (hozircha bazada mavjud emas)")

def search_sheva(word):
    # Sheva so'z (A ustuni) bo'yicha qidirish
    result = df[df['A'].str.lower() == word.lower()]
    if not result.empty:
        for _, row in result.iterrows():
            print(f"{word.lower()} - {row['B'].lower()} - {row['C'].lower()}")
    else:
        print(f"{word.lower()} (hozircha bazada mavjud emas)")

def main():
    while True:
        print("\nQaysi rejimda qidirmoqchisiz?")
        print("1. Adabiy")
        print("2. Sheva")
        print("3. Chiqish")
        choice = input("Tanlovingiz (1/2/3): ")

        if choice == '3':
            print("Dastur yakunlandi.")
            break

        if choice not in ['1', '2']:
            print("Noto'g'ri tanlov, iltimos qayta urining.")
            continue

        word = input("So'z kiriting: ").strip()

        if choice == '1':
            search_adabiy(word)
        else:
            search_sheva(word)

if __name__ == "__main__":
    main()