name = input("Введіть своє ім'я: ")
print(f"Привіт, {name}!")

lessons = int(input("Скільки сьогодні у тебе уроків? "))
if lessons > 8:
    print("Сьогодні буде важкий день")
elif lessons == 0:
    print("Сьогодні вихідний")
else:
    print("Сьогодні буде легкий день!")

tomorrow_lessons = int(input("На скільки більше уроків завтра, ніж сьогодні? "))
tomorrow_lessons += lessons
print("Завтра буде", tomorrow_lessons, "уроків")
if tomorrow_lessons > 8:
    print("Завтра буде важкий день")
elif lessons == 0:
    print("Завтра вихідний")
else:
    print("Завтра буде легкий день!")

print("До побачення,", name)
