# 1 celsius = 33.8 fahrenheit 
# 1 celsius = 274.15 kelvin 
# 1 fahrenheit = -17.22 celsius
# 1 fahrenheit = 255.92 kelvin 
# 1 kelvin = -272.15 celsius 
# 1 kelvin = -457.87 fahrenheit


#formulas for converting one degree to another degree
'''
f=c*9/5+32           c-f
c=5/9(f-32)          f-c 
k=c+273.15           c-k
c=k-273.15           k-c
k=(f-32)*5/9+273.15  f-k
f=(k-273.15)*9/5+32  k-f
'''

print("*************************************************************************************************************************************************")
print("Press any key to perform the Operation")
s=input("Enter C for Celsius or F for Fahrenheit or K for Kelvin : ")
'''
if s=="c" or s=="C" or s=="f" or s=="F" or s=="k" or s=="K":
'''
l=['c','C','f','F','k','K']
if s in l:
    if s=="c" or s=="C":
        print("Enter another value to convert degree from celsius value")
        c=input("F for Fahrenheit or K for Kelvin : ")
        fork=['f','F','k','K']
        if c in fork:
            if c=='f' or c=='F':
               c1=float(input("Enter the celsius value : "))
               f=c1*9/5+32  
               print(c1,"Celsius = ",f,"fahrenheit")
               print("Successfully Converted")
            elif c=='k' or c=='K':
                c2=float(input("Enter the celsius value : "))
                k=c2+273.15
                print(c2,"Celsius = ",k,"kelvin")
                print("Successfully Converted")
        else:
            print("Enter the correct Conversion")

    elif s=="f" or s=="F":
        print("Enter another value to convert degree from Fahrenheit value")
        f=input("C for Celsius or K for Kelvin : ") 
        cork=['c','C','k','K']
        if f in cork:
            if f=='c' or f=='C':
                f1=float(input("Enter the fahrenheit value : "))
                c=(f1-32)*5/9
                print(f1,"fahrenheit = ",c,"celsius")
                print("Successfully Converted")
            elif f=='k' or f=='K':
                f2=float(input("Enter the fahrenheit value : "))
                k=(f2-32)*5/9+273.15
                print(f2,"fahrenheit = ",k,"kelvin")
                print("Successfully Converted")
        else:
            print("Enter the correct Conversion")

    elif s=="k" or s=="K":
        print("Enter another value to convert degree from Kelvin value")
        k=input("C for Celsius or F for Fahrenheit : ")
        corf=['c','C','f','F']
        if k in corf:
            if k=='c' or k=='C':
                k1=float(input("Enter the kelvin value : "))
                c=k1-273.15
                print(k1,"kelvin = ",c,"celsius")
                print("Successfully Converted")
            elif k=='f' or k=='F':
                k2=float(input("Enter the kelvin value : "))
                f=(k2-273.15)*9/5+32
                print(k2,"kelvin = ",f,"fahrenheit")
                print("Successfully Converted")
        else:
            print("Enter the correct Conversion")        

else:
    print("Enter only above characters to perform the right operation")

