import utils.lang.ru as ut
p = ut.morph.parse
q = ut.past
for i in range(1000):
    print(i, end=' ')
    q(p('сделать')[0], i%6)
print('ok')

