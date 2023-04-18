l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
index = 0
main = []
sub = []

for i in l:
    print(f'i: {i}')
    print(f'sub: {sub}')
    if len(sub) >= 3:
        temp = sub.copy()
        main.append(temp)
        sub.clear()
        if len(l[index::]) <= 3:
            main += [l[index::]]

    index += 1
    sub.append(i)

print(main)
