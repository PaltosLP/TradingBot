

# f = open("info.txt")
#
# # print(f.read())
#
# print("-----------------------------------------")
#
# lines = f.readlines()
#
# l = list(x[1])
#
# y = int(l[0])
#
# print(y, type(y))
#
# f.close()


def file_get(self, side):
    f = open("info.txt")
    lines = f.readlines()
    buying = int(list(lines[1])[0])
    selling = int(list(lines[4])[0])
    f.close()
    if side == 'BUY':
        return buying
    else:
        return selling

def file_change(self, side):
    buying = file_get(self, 'BUY')
    selling = file_get(self, 'SELL')

    if side == 'BUY':
        buying -= 1
        selling += 1
    else:
        buying += 1
        selling -= 1

    f = open("info.txt", 'w')
    f.write(f"Buying:\n{buying}\n\nSelling:\n{selling}")
    f.close()


file_change(1, 'SELL')
