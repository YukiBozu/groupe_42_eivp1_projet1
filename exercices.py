print('Hello world!')

print(2 + 2)
print(5 + 4 - 3)
print( 2 * (3 + 4) )
print( 10 / 2 )

print( 8 / 2 )
print( 6 * 7.0 )
print( 4 + 1.65 )

print( 2**5 )

print( 9 ** (1/2) )

print( 20 // 6 ) 
print(20 % 6)

print("Python is fun!")
print('Always look on the bright side of life')

print('Brian\'s mother: He\'s not an angel. He\'s a very naughty boy!')

print('One \nTwo \nThree') 
print("""this
is a
multiline
text""") 

print("Spam" + 'eggs')

print("spam" * 3)

user = "James"  

x = 7
print(x)
print(x + 3)
print(x)

x = "This is a string"
print(x + "!")

x = input()
print(x)

name = input("Enter your name: ")
print("Hello, " + name)

age = int(input())
print(age) 

age = 42
print("His age is " + str(age)) 

name = input()
age = input()
print(name + " is " + age)  

x = 2
print(x)
x += 3
print(x)

x = "spam"
print(x)
x += "eggs"
print(x)

my_boolean = True
print(my_boolean)
True
print(2 == 3)
False
print("hello" == "hello")
True

print( 1 != 1 )
False
print("eleven" != "seven")
True
print(2 != 10)
True

print( 7 > 5 )
True
print( 10 < 10 )
False

print(7 <= 8)
True
print(9 >= 9.0)
True

num = 12
if num > 5:
   print("Bigger than 5")
   if num <=47:
      print("Between 5 and 47")

num = 3
if num == 1:
  print("One")
elif num == 2:
  print("Two")
elif num == 3: 
  print("Three")
else: 
  print("Something else")

print( 1 == 1 and 2 == 2 )
True
print( 1 == 1 and 2 == 3 )
False
print( 1 != 1 and 2 == 2 )
False
print( 2 < 1 and 3 >  6 )
False

print( 1 == 1 or 2 == 2 )
True
print( 1 == 1 or 2 == 3 )
True
print( 1 != 1 or 2 == 2 )
True
print( 2 < 1 or 3 >  6 )
False

print(not 1 == 1)
False
print(not 1 > 7)
True

words = ["Hello", "world", "!"]
print(words[0])
print(words[1])
print(words[2]) 

number = 3
things = ["string", 0, [1, 2, number], 4.56]
print(things[1])
print(things[2])
print(things[2][2])

m = [
    [1, 2, 3],
    [4, 5, 6]
    ]
    
print(m[1][2])  

str = "Hello world!"
print(str[6])

nums = [7, 7, 7, 7, 7]
nums[2] = 5
print(nums)

nums = [1, 2, 3]
print(nums + [4, 5, 6])
print(nums * 3)

words = ["spam", "egg", "spam", "sausage"]
print("spam" in words)
print("egg" in words)
print("tomato" in words)

nums = [1, 2, 3]
print(not 4 in nums)
print(4 not in nums)
print(not 3 in nums)
print(3 not in nums)

nums = [1, 2, 3]
nums.append(4)
print(nums)

nums = [1, 3, 5, 2, 4]
print(len(nums))

words = ["Python", "fun"]
index = 1
words.insert(index, "is")
print(words)

letters = ['p', 'q', 'r', 's', 'p', 'u']
print(letters.index('r'))
print(letters.index('p'))
print(letters.index('z'))

i = 1
while i <=5:
   print(i)
   i = i + 1

print("Finished!")

i = 0
while True:
  print(i)
  i = i + 1
  if i >= 5:
    print("Breaking")
    break

print("Finished")

i = 1
while i<=5:
    print(i)
    i+=1
    if i==3:
      print("Skipping 3")
      continue

words = ["hello", "world", "spam", "eggs"]
for word in words:
  print(word + "!")

str = "testing for loops"
count = 0

for x in str:
  if(x == 't'):
    count += 1

print(count) 

numbers = list(range(10))
print(numbers)

numbers = list(range(3, 8))
print(numbers)
print(range(20) == range(0, 20))

numbers = list(range(5, 20, 2))
print(numbers)

for i in range(5):
  print("hello!")


def my_func():
   print("spam")
   print("spam")
   print("spam")

my_func()

def print_with_exclamation(word):
   print(word + "!")
    
print_with_exclamation("spam")
print_with_exclamation("eggs")
print_with_exclamation("python")

def print_sum_twice(x, y):
   print(x + y)
   print(x + y)

print_sum_twice(5, 8)

def function(variable):
   variable += 1
   print(variable)

function(7)
print(variable)


def max(x, y):
    if x >=y:
        return x
    else:
        return y
        
print(max(4, 7))
z = max(8, 5)
print(z)


def multiply(x, y):
   return x * y

a = 4
b = 7
operation = multiply
print(operation(a, b))


def add(x, y):
  return x + y

def do_twice(func, x, y):
  return func(func(x, y), func(x, y))

a = 5
b = 10

print(do_twice(add, a, b))