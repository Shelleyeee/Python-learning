f = open('C:/Users/10740/Downloads/scores.txt','r',encoding ='utf-8')
file_lines = f.readlines()
f.close()

finalscore = []

for i in file_lines:
    data = i.split()
    sum = 0
    for score in data[1:]:
        sum = sum + int(score)
    result = data[0]+str(sum)+'\n'      
    finalscore.append(result)

winner = open('C:/Users/10740/Downloads/winner.txt','a',encoding='utf-8')
winnercontent = winner.writelines(finalscore)
print(winnercontent)
winner.close()

print(ord('周'))
