import sys,re
from json import dump

class Graph:
    
    def __init__(self) -> None:
        self.adjc = {}
        self.vertex = []


    def graph_construction(self, data : list) -> None:
        vs = set()
        for el in data:
            vs.add(el[0])
            vs.add(el[1])
            if el[0] not in self.adjc:
                self.adjc[el[0]] = []
            self.adjc[el[0]].append((el[1], el[2]))
        vs = list(vs)
        vs.sort()
        self.vertex = vs


class GraphCreation:

    def __init__(self, input, output) -> None:
        self._in = input
        self._out = output
        self.data = None
        self.graph = None
        self.g = Graph()

    def check_params(self) -> bool:
        if self._in is None:
            return False
        if self._out is None:
            self._out = f"output.json"
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
        arcs_cnt = {}
        arcs = {}
        for el in self.data:
            s = f'{el[0]}-{el[1]}'
            if s not in arcs and s not in arcs_cnt:
                arcs_cnt[s] = 0
                arcs[s] = set()
            arcs_cnt[s] += 1
            arcs[s].add(el[2])
        for k in arcs.keys():
            if len(arcs[k]) != arcs_cnt[k]:
                return False
        return True


    def get_graph(self) -> None:
        self.g.graph_construction(self.data)
        print(self.g.vertex, self.g.adjc)
        arc = []
        for el in self.g.vertex:
            for tpl in self.g.adjc[el]:
                arc.append({ "from" : el
                           ,  "to" : tpl[0]
                           , "order" : int(tpl[1])})
        self.graph = {"graph" : {"vertex" : self.g.vertex, "arc" : arc}}


    def write_to_file(self) -> bool:
        try:
            with open(self._out, 'w') as f:
                dump(self.graph, f)
        except:
            print(f"Не удалось записать в файл `{self._out}`.\n")
            return False
        return True


    def graph_creation(self) -> None:
        if self.check_params():
            if self.read_from_file():
                self.data_parser()
                if not self.check_data():
                    print('Некорректный ввод данных.\n'
                          'Проверьте уникальность порядковых номеров '
                          'у каждой из дуг.')
                    return
                self.get_graph()
                if self.write_to_file():
                    print(f"Граф был успешно записан в файл")


def args_parser(argv : list) -> None:
    global graphs
    in1, in2, out1, out2 = None, None, None, None
    for el in argv:
        if "input1=" in el:
            in1 = el[el.find("=") + 1:]
        elif "input2=" in el:
            in2 = el[el.find("=") + 1:]
        elif "output1=" in el:
            out1 = el[el.find("=") + 1:]
        elif "output2=" in el:
            out2 = el[el.find("=") + 1:]
    if (in1 is None) and (in2 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " для ввода и вывода.\n"
              "Пример: input1=in.txt output1=out.json\n")
        return False
    if in1 is not None:
        if out1 is None:
            out1 = f"output1.json"
            print(f"Файл для вывода не был введен.\n"
                f"Поэтому был установлен файл по умолчанию ({out1})")
        graphs.append(GraphCreation(in1, out1))
    if in2 is not None:
        if out2 is None:
            out2 = f"output2.json"
            print(f"Файл для вывода не был введен.\n"
                f"Поэтому был установлен файл по умолчанию ({out2})")
        graphs.append(GraphCreation(in2, out2)) 
    return True


def main() -> None:
    args_parser(sys.argv)
    for g in graphs:
        g.graph_creation()

if __name__ == "__main__":
    graphs = []
    main()
    # f = open('out-nntask1.json')
    # d = json.load(f)
    # print(d)