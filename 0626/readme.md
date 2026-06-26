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

# 파이썬의 연산자와 if 조건문

파이썬에서는 **연산자**를 사용해 계산하거나 비교하고, `if` 조건문을 사용해 상황에 따라 다른 코드를 실행할 수 있습니다. 조건문은 결과가 `True` 또는 `False`인지에 따라 프로그램의 흐름을 바꿉니다. [web:11][web:20]

## 1. 연산자란?

연산자는 값과 값을 이용해 계산하거나 비교하는 기호입니다. 파이썬에서 자주 쓰는 연산자는 산술 연산자, 비교 연산자, 논리 연산자입니다. [web:11][web:20]

### 산술 연산자

산술 연산자는 숫자를 계산할 때 사용합니다.

- `+` : 더하기.
- `-` : 빼기.
- `*` : 곱하기.
- `/` : 나누기.
- `//` : 몫 구하기.
- `%` : 나머지 구하기.
- `**` : 거듭제곱.

```python
a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** b)
```

### 비교 연산자

비교 연산자는 두 값을 비교해서 `True` 또는 `False`를 반환합니다. 이런 결과는 `if` 조건문에서 자주 사용됩니다. [web:11][web:20]

- `==` : 같다.
- `!=` : 같지 않다.
- `>` : 크다.
- `<` : 작다.
- `>=` : 크거나 같다.
- `<=` : 작거나 같다.

```python
x = 10
y = 20

print(x == y)
print(x != y)
print(x < y)
print(x >= y)
```

### 논리 연산자

논리 연산자는 여러 조건을 한 번에 판단할 때 사용합니다.

- `and` : 모든 조건이 참일 때 참.
- `or` : 조건 중 하나라도 참이면 참.
- `not` : 참과 거짓을 반대로 바꿈.

```python
age = 20
is_student = True

print(age >= 18 and is_student)
print(age < 18 or is_student)
print(not is_student)
```

## 2. if 조건문

`if` 조건문은 조건이 참일 때만 특정 코드를 실행합니다. 조건이 거짓이면 해당 코드는 건너뜁니다. [web:11][web:20]

```python
number = 15

if number > 0:
    print("양수입니다.")
```

위 예제에서 `number > 0`이 참이므로 `"양수입니다."`가 출력됩니다. 조건이 거짓이면 출력되지 않습니다. [web:11]

## 3. if, elif, else

조건이 여러 개일 때는 `elif`와 `else`를 함께 사용합니다. `elif`는 앞의 조건이 거짓일 때 다른 조건을 검사하고, `else`는 앞의 모든 조건이 거짓일 때 실행됩니다. [web:11][web:20]

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")
```

## 4. 조건문 작성 규칙

파이썬은 들여쓰기를 매우 중요하게 봅니다. `if`, `elif`, `else` 아래의 코드는 같은 들여쓰기로 맞춰야 합니다. [web:11]

```python
if True:
    print("들여쓰기 필요")
```

들여쓰기가 맞지 않으면 오류가 발생할 수 있습니다. 따라서 조건문을 작성할 때는 공백 수를 일정하게 유지해야 합니다. [web:11]

## 5. 자주 쓰는 예시

```python
age = 19

if age >= 18:
    print("성인입니다.")
else:
    print("미성년자입니다.")
```

이 예시는 비교 연산자 `>=`와 `if-else`를 함께 사용한 기본 형태입니다. 프로그램은 조건에 따라 서로 다른 메시지를 보여 줄 수 있습니다. [web:11][web:20]

## 6. 정리

파이썬의 연산자는 값을 계산하거나 비교하는 데 사용됩니다. `if` 조건문은 이런 비교 결과를 바탕으로 프로그램의 실행 흐름을 바꾸는 핵심 문법입니다. [web:11][web:20]
