def frequency_analytic():
    string = input("input : ")
    dic = {}
    
    for chr in string:
        if chr in dic:
            dic[chr] += 1
        else:
            dic[chr] = 1
    print(dic)
    
frequency_analytic()