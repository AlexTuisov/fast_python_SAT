import numpy as np

from formula import CNF


# class FastCNF:
#     def __init__(self, slow_cnf: CNF):
#         self.length = len(slow_cnf.clauses)
#         self.width = max(map(len, slow_cnf.clauses))
#         self.clauses = np.zeros((self.length, self.width), dtype=np.int32)


class Clause:
    def __init__(self, list_of_literals):
        self.literals = tuple(list_of_literals)
        self.left_watcher = None
        self.right_watcher = None
        self.heuristic_score = 0

    def __len__(self):
        return len(self.literals)

    def next_not_false(self):
        pass


    """inline ClauseState Clause::next_not_false(bool is_left_watch, Lit other_watch, bool binary, int& loc) {  
        if (verbose_now()) cout << "next_not_false" << endl;
        
        if (!binary)
            for (vector<int>::iterator it = c.begin(); it != c.end(); ++it) {
                LitState LitState = S.lit_state(*it);
                if (LitState != LitState::L_UNSAT && *it != other_watch) { // found another watch_lit
                    loc = distance(c.begin(), it);
                    if (is_left_watch) lw = loc;    // if literal was the left one 
                    else rw = loc;				
                    return ClauseState::C_UNDEF;
                }
            }
        switch (S.lit_state(other_watch)) {
        case LitState::L_UNSAT: // conflict
            if (verbose_now()) { print_real_lits(); cout << " is conflicting" << endl; }
            return ClauseState::C_UNSAT;
        case LitState::L_UNASSIGNED: return ClauseState::C_UNIT; // unit clause. Should assert the other watch_lit.	
        case LitState::L_SAT: return ClauseState::C_SAT; // other literal is satisfied. 
        default: Assert(0); return ClauseState::C_UNDEF; // just to supress warning. 
        }
    }"""

    def reset(self):
        pass

"""
class Clause {
	clause_t c;
	int lw,rw; //watches;	
public:	
	Clause(){};
	void insert(int i) {c.push_back(i);}
	void lw_set(int i) {lw = i; /*assert(lw != rw);*/}
	void rw_set(int i) {rw = i; /*assert(lw != rw);*/}	
	clause_t& cl() {return c;}
	int get_lw() {return lw;}
	int get_rw() {return rw;}
	int get_lw_lit() {return c[lw];}
	int get_rw_lit() {return c[rw];}
	int  lit(int i) {return c[i];} 		
	inline ClauseState next_not_false(bool is_left_watch, Lit other_watch, bool binary, int& loc); 
	size_t size() {return c.size();}
	void reset() { c.clear(); }	
	void print() {for (clause_it it = c.begin(); it != c.end(); ++it) {cout << *it << " ";}; }
	void print_real_lits() {
		Lit l; 
		cout << "("; 
		for (clause_it it = c.begin(); it != c.end(); ++it) { 
			l = l2rl(*it); 
			cout << l << " ";} cout << ")"; 
	}
	void print_with_watches() {		
		for (clause_it it = c.begin(); it != c.end(); ++it) {
			cout << l2rl(*it);
			int j = distance(c.begin(), it); //also could write "int j = i - c.begin();"  : the '-' operator is overloaded to allow such things. but distance is more standard, as it works on all standard containers.
			if (j == lw) cout << "L";
			if (j == rw) cout << "R";
			cout << " ";
		};
	}
};
"""
