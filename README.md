# -print("مرحبًا بك في عالم بايثون!")

# تعريف المتغيرات وإجراء عملية حسابية
num1 = 10
num2 = 5
result = num1 + num2
print("هي النتيجة:", result)  # تصحيح دالة الطباعة

# حلقة تكرار لطباعة الأرقام من 1 إلى 10
for i in range(1, 11):
    print(i)

# التحقق مما إذا كان العدد زوجيًا أو فرديًا
num = int(input("أدخل رقمًا: "))
if num % 2 == 0:
    print("الرقم زوجي")
else:
    print("الرقم فردي")

# استيراد مكتبات ضرورية
from math import factorial
import random
import string

# تصحيح إنشاء كلمة المرور العشوائية
length = 8  # تصحيح اسم المتغير
password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
print(f"اكتب كلمة السر: {password}")  # تصحيح الطباعة

# دالة حساب المضروب
def factorial(n):
    if n == 0 or n == 1: 
        return 1
    else:
        return n * factorial(n - 1)

num = int(input("أدخل رقمًا لحساب المضروب: "))
print(f"المضروب للرقم {num} هو: {factorial(num)}")  # تصحيح الطباعة

# دالة الآلة الحاسبة
def calculator():
    num1 = float(input("أدخل الرقم الأول: "))
    num2 = float(input("أدخل الرقم الثاني: "))
    operation = input("اختر العملية (+, -, *, /): ")

    if operation == "+":
        print("النتيجة:", num1 + num2)
    elif operation == '-':
        print("النتيجة:", num1 - num2)
    elif operation == '*':
        print("النتيجة:", num1 * num2)
    elif operation == '/':
        if num2 != 0:
            print("النتيجة:", num1 / num2)
        else:
            print("لا يمكن القسمة على صفر!")
    else:
        print("عملية غير صحيحة!")

calculator()  # استدعاء الدالة





مدري
