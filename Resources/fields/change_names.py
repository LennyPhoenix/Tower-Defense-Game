name = input('Name of file to copy: ')

with open(name+'.png', 'rb') as e:
    data = e.read()

names = [
    'LR',
    'TL',
    'TB',
    'TR',
    'BR',
    'LB'
]

for t in names:
    with open(name+'_'+t+'.png', 'wb') as e:
        e.write(data)
