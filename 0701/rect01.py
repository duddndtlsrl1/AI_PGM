def get_rect_area(w, h):
    """
    Calculate the area of a rectangle.

    """
    return w * h

def main():
    width = float(input("Enter the width of the rectangle: "))
    height = float(input("Enter the height of the rectangle: "))
    area = get_rect_area(width, height)
    print(f"The area of the rectangle is: {area}")

#module을 import할 때는 main()이 실행되지 않도록 하기 위해서 아래와 같이 작성
if __name__ == "__main__":
    main()