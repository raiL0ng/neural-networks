import sys,re, math
import json

class Graph:
    
    def __init__(self) -> None:
        self.adjc = {}
        self.vertex = []
        self.prnts = {}
        self.children = {}
        self.hasCycle = False


    def parents_init(self):
        for el in self.vertex:
            self.prnts[el] = -1


    def children_init(self):
        for el in self.vertex:
            self.children[el] = -1


    def graph_construction(self, data : list) -> None:
        unic_vs = set()
        for el in data:
            unic_vs.add(el[0])
            unic_vs.add(el[1])
            if el[1] not in self.adjc:
                self.adjc[el[1]] = []
            self.adjc[el[1]].append((el[0], int(el[2])))
        for v, vs in self.adjc.items():
            n = len(vs)
            tmp = [''] * n
            for el, k in vs:
                tmp[(k - 1) % n] = el
            test = set()
            for el in tmp:
                test.add(el)
                if el == '':
                    self.vertex = [-1]
                    print('В графе некорректно заданы номера!\nПроверьте уникальность номеров.')
                    return
            # if len(test) != len(tmp):
            #     self.vertex = [-1]
            #     print('В данном случае от каждой вершины должна выходить одна дуга.')
            #     return
            self.adjc[v] = tmp
        for v in unic_vs:
            if v not in self.adjc:
                self.adjc[v] = []
        for v in self.adjc.keys():
            self.vertex.append(v)


    def find_cycle(self):
        def dfs(used : dict, v : int):
            used[v] = 1
            for u in self.adjc[v]:
                if used[u] == 0:
                    dfs(used, u)
                elif used[u] == 1:
                    self.hasCycle = True
            used[v] = 2
        used = {}
        for el in self.vertex:
            used[el] = 0
        self.hasCycle = False
        for el in self.vertex:
            if used[el] == 0:
                dfs(used, el)
        return self.hasCycle


    def dfs(self, used, v, ans):
        ans.append(v)
        for u in self.adjc[v]:
            self.dfs(used, u, ans)


    def get_parents(self):
        def dfs(used, v):
            used[v] = True
            for u in self.adjc[v]:
                if not used[u]:
                    self.prnts[u] = v
                    self.children[v] = u
                    dfs(used, u)
        self.parents_init()
        self.children_init()
        used = {}
        for v in self.vertex:        
            for el in self.vertex:
                used[el] = False
            dfs(used, v)


class FunctionCreation:

    def __init__(self, input, op, output) -> None:
        self._in = input
        self._op = op
        self._out = output
        self.data = None
        self.oper = {}
        self.graph = None
        self.values = []
        self.g = Graph()

    def check_params(self) -> bool:
        if self._in is None:
            return False
        if self._out is None:
            self._out = f"output.txt"
            print(f"Файл для вывода не был введен.\n"
                  f"Поэтому был установлен файл по умолчанию ({self._out})")
        return True

    
    def read_from_file(self) -> bool:
        try:
            f = open(self._in, 'r', encoding='utf-8')
            self.data = f.read()
            f.close()
        except:
            print(f"Файла `{self._in}` не существует. "
                  "Проверьте корректность имени файла.")
            return False
        return True


    def read_json_file(self) -> dict:
        try:
            f = open(self._op)
            self.oper = json.load(f)
            f.close()
        except:
            print(f"Файла `{self._in}` не существует. "
                  "Проверьте корректность имени файла.")
            return False
        return True


    def data_parser(self) -> None:
        rawdata = self.data
        self.data = []
        cnt = 0
        tmp = []
        for el in re.split(r"\W+", rawdata):
            if el.isalnum():
                cnt += 1
                tmp.append(el)
                if cnt == 3:
                    if not tmp[2].isdigit():
                        self.data = []
                        return
                    cnt = 0
                    self.data.append(tmp)
                    tmp = []


    def check_data(self) -> bool:
        if self.data == []:
            return False
        self.g.graph_construction(self.data)
        if self.g.vertex == [-1]:
            return False
        if self.g.find_cycle():
            print('\nВ графе найден цикл!')
            return False
        return True

    def count_value(self, order):
        try:
            stk = []
            for v in order:
                if str(self.oper[v]).isnumeric():
                    stk.append(int(self.oper[v]))
                else:
                    if self.oper[v] == "+":
                        stk.append(stk.pop() + stk.pop())
                    elif self.oper[v] == "*":
                        stk.append(stk.pop() * stk.pop())
                    elif self.oper[v] == "exp":
                        stk.append(math.exp(stk.pop()))
            return stk[-1]
        except:
            return None

    def find_values(self) -> None:
        
        self.g.get_parents()
        for v, p in self.g.prnts.items():
            if p == -1:
                order = []
                used = {}
                for el in self.g.vertex:
                    used[el] = False
                self.g.dfs(used, v, order)
                order.reverse()
                new_val = self.count_value(order)
                if new_val is None:
                    self.values.clear()
                    return    
                self.values.append(new_val)

         
    def write_to_file(self, filename, data) -> bool:
        try:
            with open(filename, 'w') as f:
                f.write(f'{data}')
        except:
            print(f"Не удалось записать в файл `{filename}`.\n")
        else:
            print(f"Ответ был успешно записан в файл `{filename}`")


    def creation(self) -> None:
        if self.check_params():
            if self.read_from_file() and self.read_json_file():
                self.data_parser()
                if not self.check_data():
                    print('Некорректный ввод данных.\n')
                    return
                self.find_values()
                if self.values == []:
                    print(f'Неверно был задан граф или операции не соответствуют вершинам!')
                if len(self.values) == 1:
                    self.write_to_file(self._out, self.values[-1])
                else:
                    for n, data in enumerate(self.values, 1):
                        self.write_to_file(f'{self._out[:self._out.find(".txt")]}-{n}.txt', data)


def args_parser(argv : list) -> None:
    global graphs
    in1, in2, op1, op2, out1, out2 = None, None, None, None, None, None
    for el in argv:
        if "input1=" in el:
            in1 = el[el.find("=") + 1:]
        elif "input2=" in el:
            in2 = el[el.find("=") + 1:]
        elif "oper1=" in el:
            op1 = el[el.find("=") + 1:]
        elif "oper2=" in el:
            op2 = el[el.find("=") + 1:]
        elif "output1=" in el:
            out1 = el[el.find("=") + 1:]
        elif "output2=" in el:
            out2 = el[el.find("=") + 1:]
    if (in1 is None) and (in2 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " для ввода и вывода.\n"
              "Пример: input1=in.txt oper1=operations.json output1=out.txt\n")
        return False
    if op1 is not None:
        graphs.append(FunctionCreation(in1, op1, out1))
    else:
        print('Необходимо также ввести название файла, в котором содержатся операции'
              '\nНапример oper1=op.json')
    if op2 is not None:
        graphs.append(FunctionCreation(in2, op2, out2)) 
    else:
        if in2 is not None:
            print('Необходимо также ввести название файла, в котором содержатся операции'
                '\nНапример oper2=op.json')
    return True


def main() -> None:
    args_parser(sys.argv)
    for g in graphs:
        g.creation()


if __name__ == "__main__":
    graphs = []
    main()