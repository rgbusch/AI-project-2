temp_list = []
for x in range(1,12):
    temp_list.append(1 + (x-1)/12)

f = open("weights.txt","w+")

temp_str = ""
for y in temp_list:
    if y != temp_list[-1]:
        temp_str += (str(y) + ",")
    else:
        temp_str += (str(y))
f.write(temp_str)
f.close()

    
