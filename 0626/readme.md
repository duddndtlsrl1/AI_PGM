# 파이썬 리스트

파이썬 리스트는 여러 값을 하나의 변수에 저장하는 자료형입니다. 리스트는 순서가 있고, 변경 가능하며, 중복 값을 허용합니다. [web:1][web:2]

## 1. 리스트 생성

리스트는 대괄호 `[]`로 만들거나 `list()` 생성자를 사용할 수 있습니다. 항목들은 쉼표로 구분합니다. [web:1][web:2]

```python
fruits = ["apple", "banana", "cherry"]
numbers = list((1, 2, 3))
```

## 2. 리스트의 특징

- 순서가 있습니다. 첫 번째 항목은 인덱스 `0`입니다. [web:1]
- 변경할 수 있습니다. 항목을 추가, 수정, 삭제할 수 있습니다. [web:1][web:2]
- 중복 값을 허용합니다. [web:1]
- 여러 종류의 데이터를 함께 넣을 수 있습니다. [web:2]

## 3. 자주 쓰는 기능

### 길이 확인

`len()` 함수로 리스트의 개수를 확인할 수 있습니다. [web:1]

```python
fruits = ["apple", "banana", "cherry"]
print(len(fruits))
```

### 항목 추가

- `append()`는 끝에 한 개의 항목을 추가합니다. [web:2]
- `insert()`는 원하는 위치에 항목을 넣습니다. [web:2]
- `extend()`는 여러 항목을 한 번에 추가합니다. [web:2]

```python
fruits.append("orange")
fruits.insert(1, "melon")
fruits.extend(["grape", "kiwi"])
```

### 항목 삭제

- `remove()`는 값으로 삭제합니다. [web:2]
- `pop()`은 위치로 삭제하고 꺼낸 값을 반환합니다. [web:2]
- `clear()`는 모든 항목을 삭제합니다. [web:2]

```python
fruits.remove("banana")
last_item = fruits.pop()
fruits.clear()
```

### 정렬과 뒤집기

- `sort()`는 리스트를 정렬합니다. [web:2]
- `reverse()`는 순서를 거꾸로 바꿉니다. [web:2]

```python
numbers =[2][3][1]
numbers.sort()
numbers.reverse()
```

## 4. 인덱싱과 슬라이싱

리스트의 각 항목은 인덱스로 접근할 수 있습니다. 음수 인덱스도 사용할 수 있습니다. [web:1]

```python
fruits = ["apple", "banana", "cherry"]
print(fruits)
print(fruits[-1])
print(fruits[0:2])
```

## 5. 반복문 예시

리스트는 `for`문과 함께 자주 사용합니다. [web:9]

```python
for fruit in fruits:
    print(fruit)
```

## 6. 간단한 예제

```python
shopping = ["milk", "egg", "bread"]
shopping.append("coffee")
shopping.remove("egg")
print(shopping)
```

이 예제는 리스트에 항목을 추가하고 삭제하는 기본 흐름을 보여줍니다.
