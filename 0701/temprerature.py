def menu():
    print("1. 섭씨 온도->화씨 온도 변환")
    print("2. 화씨 온도->섭씨 온도 변환")
    print("3. 종료")
    selection = int(input("메뉴를 선택하세요: "))
    return selection

def ctof(c):
    temp=c*9.0/5.0+32.0
    return temp

def ftoc(f):
    temp=(f-32.0)*5.0/9.0
    return temp

def input_f():
    f=float(input("화씨 온도를 입력하세요: "))
    return f

def input_c():
    c=float(input("섭씨 온도를 입력하세요: "))
    return c

def main():
    while True:
        index=menu()
        if index==1:
            c=input_c()
            f=ctof(c)
            print(f"화씨 온도는 " t2, "\n")
        elif index==2:
            f=input_f()
            c=ftoc(f)
            print(f"섭씨 온도는 " t1, "\n")
        else:
            break

    if __name__=="__main__":
        main()