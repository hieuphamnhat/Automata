class Automata:
    def __init__(self, states, sigma, start_state, end_states, transition_functions):
        self.states = set(states)   #tap trang thai
        self.sigma = set(sigma) #bang chu cai
        self.start_state = start_state #trang thai khoi dau
        self.end_states = set(end_states) #tap trang thai ket
        self.transition_functions = transition_functions #ham chuyen tt
        self.extra_state = "" #trang thai moi

        self.fill_automata()    # day du otomat truoc khi toi tieu
        self.minimization_DFA() # toi tieu hoa otomat

    def fill_automata(self):
        #create new state for fill automata
        make_extra_state = False
        
        for s in self.states:
            if not s in self.transition_functions:
                make_extra_state = True
                self.transition_functions[s] = {}
            for symbol in self.sigma:
                if not symbol in self.transition_functions[s]:
                    make_extra_state = True 
                    self.transition_functions[s][symbol] = [self.extra_state]

        if make_extra_state:
            self.start_state.add(self.extra_state)
            self.transition_functions[self.extra_state] = {}
            for symbol in self.sigma:
                self.transition_functions[self.extra_state][symbol] = [self.extra_state]

    def minimization_DFA(self):
        matrix = {}

        for i in self.states:
            if not i in matrix:
                matrix[i] = {}
            for j in self.states:
                if not j in matrix:
                    matrix[j] = {}
                matrix[i][j] = 0
                if (i in self.end_states and j not in self.end_states) or (not i in self.end_states and j in self.end_states):
                    matrix[i][j] = 1
                matrix[j][i] = matrix[i][j]
        
        #print(table)
                
        check = True

        while(check):
            check = False
            for i in self.states:
                for j in self.states:
                    if matrix[i][j] == 1:
                        continue
                    for symbol in self.sigma:
                        toI = self.transition_functions[i][symbol]
                        toJ = self.transition_functions[j][symbol]
                        
                        if(matrix[ toI[0] ][ toJ[0] ] == 1):
                            matrix[i][j] = 1
                            check = True
        
        new_state = []
        s = {}
        for i in self.states:
            for j in self.states:
                if matrix[i][j] == 0:
                    if i in s and j not in s:
                        new_state[s[i]].append(j)
                        s[j] = s[i]
                    elif j in s and i not in s:
                        new_state[s[j]].append(i)
                        s[i] = s[j]
                    elif i not in s and j not in s:
                        new_state.append(list(set([i, j])))
                        s[i] = len(new_state) - 1
                        s[j] = s[j]

        new_transition_functions = {} #ham chuyen trang thai sau khi toi tieu

        #tao cung cho do thi ham chuyen
        for s in new_state:
            for symbol in self.sigma:
                state_str = '_'.join(str(v) for v in s)
                if not state_str in new_transition_functions:
                    new_transition_functions[state_str] = {}
                next_s = self.transition_functions[s[0]][symbol]
                next_state = ""
                for ns in new_state:
                    if next_s[0] in ns:
                        next_state = "_".join(str(v) for v in ns)
                        break
                new_transition_functions[state_str][symbol] = next_state
        
        #xac dinh trang thai khoi dau va tap trang thai ket cua otomat sau khi toi tieu
        new_end = set()
        res_states = []
        for list_s in new_state:
            current_state = '_'.join(str(v) for v in list_s)
            res_states.append(current_state)
            for s in list_s:
                if s in self.end_states:
                    new_end.add(current_state)
                if s == self.start_state:
                    self.start_state = current_state
        
        self.states = res_states
        self.end_states = new_end
        self.transition_functions = new_transition_functions


if __name__ == "__main__":
    states = set()
    sigma = set()
    start_state = ''
    end_states = set()
    transition_functions = {}


    ip_file = open('example.txt', 'r')
    states = ip_file.readline()[:-1].split(",")
    print(states)
    sigma = ip_file.readline()[:-1].split(",")
    
    start_state = ip_file.readline()[:-1]
    if start_state not in states:
        print("File input error: ", start_state)
        exit()

    end_states = ip_file.readline()[:-1].split(",")
    print(start_state)
    print(end_states)
    for e in end_states:
        if e not in states:
            print("File input error: ", e)
            exit()

    # transition_functions
    for x in ip_file:
        tmp = []
        if x[-1] == '\n':
            tmp = x[:-1].split(",")
        else:
            tmp = x.split(",")
        if tmp[0] not in transition_functions:
            transition_functions[ tmp[0] ] = {}
        transition_functions[ tmp[0] ][ tmp[1] ] = tmp[2:]
        
    ip_file.close()

    automata = Automata(states, sigma, start_state, end_states, transition_functions)
    print("After minimization: ")
    print("States: ", automata.states)
    print("Sigma: ", automata.sigma)
    print("Start state: ", automata.start_state)
    print("End_states: ", automata.end_states)

    print("{:<10}".format("δ"), end="")
    for symbol in automata.sigma:
        print("{:<10}".format(symbol), end="")
    print()
    for s in sorted(automata.states):
        print("{:<10}".format(s), end="")
        for symbol in automata.sigma:
            if not s in automata.transition_functions:
                print("{:<10}".format(tmp), end="")
                continue
            print("{:<10}".format(automata.transition_functions[s][symbol]), end="")
        print()
