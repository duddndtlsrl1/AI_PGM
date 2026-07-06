def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


def main():
    while True:
        print("\n=== 계산기 ===")
        print("1. 더하기")
        print("2. 빼기")
        print("3. 곱하기")
        print("4. 나누기")
        print("5. 종료")

        choice = input("메뉴 선택: ")

        if choice == "5":
            print("프로그램을 종료합니다.")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("잘못된 메뉴입니다.")
            continue

        try:
            a = float(input("첫 번째 숫자: "))
            b = float(input("두 번째 숫자: "))

            if choice == "1":
                result = add(a, b)
            elif choice == "2":
                result = sub(a, b)
            elif choice == "3":
                result = mul(a, b)
            elif choice == "4":
                result = div(a, b)

            print(f"\n결과: {result}")

        except ValueError as e:
            print(f"오류: {e}")


if __name__ == "__main__":
    main()