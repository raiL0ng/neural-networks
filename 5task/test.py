import numpy as np # Подключаем NumPy для работы с массивами

def f(x): # Определяем сигмоидную функцию активации 
    return 2/(1 + np.exp(-x)) -1

def df(x): # Рассчитываем производную сигмоидной функции
    return 0.5 * (1 + x) * (1 - x)

W1 = np.array([[-0.2, 0.3, -0.4], [0.1, -0.3, -0.4]])
W2 = np.array([0.2, 0.3])

def go_forward(inp):
    print(len(W1), len(W1[0]), len(inp))
    sum = np.dot(W1, inp)
    print(f'{sum = }')
    out = np.array([f(x) for x in sum])
    print(f'{out = }')
    print(len(W2), len(out))

    sum = np.dot(W2, out)
    print(f'{sum = }')

    y = f(sum)
    print(f'{y = }')

    return (y, out)

def train(epoch):
    global W2, W1
    lmd = 0.001
    N = 100000
    count = len(epoch)
    for k in range(1):
        x = epoch[np.random.randint(0, count)]
        y, out = go_forward(x[0:3])
        e = y - x[-1]
        delta = e * df(y)
        print(len(W2), W2, out)
        W2[0] = W2[0] - lmd * delta * out[0]
        W2[1] = W2[1] - lmd * delta * out[1]

        delta2 = W2 * delta * df(out)
        print("w1 = ", W1, "w2 = ", W2, delta2)
        W1[0, :] = W1[0, :] - np.array(x[0:3]) * delta2[0] * lmd
        W1[1, :] = W1[1, :] - np.array(x[0:3]) * delta2[1] * lmd

epoch = [(-1, -1, -1, -1),
         (-1, -1, 1, 1),
          (1, 1, -1, -1),
         (-1, 1, -1, -1),
         (-1, 1, 1, -1),
         (1, -1, -1, -1),
         (1, -1, 1, 1),
         (1, 1, 1, -1)]
# train(epoch)
# t, s = go_forward(epoch[0][0:3])
# print(t, s)
# print(W1)
# print(W2)

# for x in epoch:
#     y, out = go_forward(x[0:3])
#     print(f'Выходное значение нейронной сети: {y} => {x[-1]}')


def test():
    w1 = [[0.1], [0.2], [0.3], [0.4], [0.5], [0.6], [0.7], [0.8], [0.9], [0.0]]
    w2 = [[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]]
    w2 = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    x__ = [[0.1],[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9],[1.0]]
    # x = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]
    y__ = [[0.9], [0.8], [0.7], [0.6], [0.5], [0.4], [0.3], [0.2], [0.1], [0.0]]
    print(np.array(w1).shape)
    # x = [[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]]
    # x = np.array(x)
    # w1 = np.array(w1)
    # print(len(w1), len(w1[0]), len(x))
    # print(np.dot(w1, x))

    # c = BackPropagation(np.array(w1),np.array(w2))
    # c.get_learning_rate(0.2)
    # y_, out = c.go_forward(np.array(x__[0]))
    # e = c.mse(y_, np.array(y__[0]))
    # print(e, y_, out)
    # c.train(np.array(x__), np.array(y__), 10)
    # print(c.W1[0, :], c.W1[0])

x = np.array([[1], [2], [3]])
w2 = [4, 5, 6]
y = [0.52497919, 0.549834,  0.57444252]
delta = np.array([[0.00020144, 0.00024992, 0.0002962 ]])
w2 = np.array(w2)
for i in range(len(x)):
    x[i, :] = x[i, :] - delta[:, i]
    print(x[i])
print(x)