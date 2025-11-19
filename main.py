from struct import calcsize

def calc(cost=66):
    for i12 in range(cost//12 + 1):
        for i15 in range(cost//15 + 1):
            for i18 in range(cost//18 + 1):
                # print(i12, i15, i18)
                if i12 * 12 + i15 * 15 + i18 * 18 == cost:
                    print(f'{i12} * 12 + {i15} * 15 + {i18} * 18 == {cost}')

if __name__ == '__main__':
    calc(66)
    calc(84)