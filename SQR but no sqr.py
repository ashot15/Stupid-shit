import math

def find_square_root(x):
    if x < 0:
        print("Ошибка: Нет действительного квадратного корня для отрицательных чисел.")
        return None
    
    # Используем встроенную функцию для нахождения квадратного корня
    sqrt_value = math.isqrt(x)  # Для целых чисел
    if sqrt_value * sqrt_value == x:
        print(f"Квадратный корень из {x} равен {sqrt_value}.")
        return sqrt_value
    else:
        print(f"Квадратный корень из {x} не существует среди целых чисел.")
        return None

def main():
    try:
        x = int(input("Введите число: "))
        result = find_square_root(x)
        if result is not None:
            print(f"Результат: {result}")
        else:
            print("Поиск завершен.")
    except ValueError:
        print("Ошибка: Введите корректное целое число.")

if __name__ == "__main__":
    main()
