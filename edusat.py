from time import perf_counter
from clause import Clause


class TimeoutException(Exception):
    pass


class UNSATException(Exception):
    pass


class Solver:
    def __init__(self, timeout, input_formula, options):
        self.timeout = timeout
        self.cnf = {}
        self.literals = {}
        self.watchers = {}
        self.unit_clauses = set()
        self.number_of_variables = input_formula.vn
        for number, item in enumerate(input_formula.clauses):
            self.cnf[number] = (Clause(item))
            if len(item) == 1:
                self.unit_clauses.add(item)
            for literal in item:
                self.literals[literal] = number
                self.watchers[literal] = number
        self.state = {}

    def solve(self):
        try:
            self._solve()
        except TimeoutException:
            print("Got timeout on the problem")
        except UNSATException:
            print("The formula is unsatisfiable!")

    def _solve(self):
        start = perf_counter()
        while True:
            while True:
                result_of_bcp = self.BCP()
                if result_of_bcp == "conflict":
                    self.backtrack()
                else:
                    break
            end = perf_counter()
            result_of_decide = self.decide()
            if result_of_decide == "SAT":
                return "SAT"
            if end - start > self.timeout:
                raise TimeoutException

    def BCP(self):
        return 0

    def backtrack(self):
        pass

    def analyze_conflict(self):
        pass

    def decide(self):
        return 0




"""
class Solver {
	vector<Clause> cnf; // clause DB. 
	vector<int> unaries; 
	trail_t trail;  // assignment stack	
	vector<int> separators; // indices into trail showing increase in dl 	
	vector<int> LitScore; // literal => frequency of this literal (# appearances in all clauses). 
	vector<vector<int> > watches;  // Lit => vector of clause indices into CNF
	vector<VarState> state;  // current assignment
	vector<VarState> prev_state; // for phase-saving: same as state, only that it is not reset to 0 upon backtracking. 
	vector<int> antecedent; // var => clause index in the cnf vector. For variables that their value was assigned in BCP, this is the clause that gave this variable its value. 
	vector<bool> marked;	// var => seen during analyze()
	vector<int> dlevel; // var => decision level in which this variable was assigned its value. 
	vector<int> conflicts_at_dl; // decision level => # of conflicts under it. Used for local restarts. 

	// Used by VAR_DH_MINISAT:	
	map<double, unordered_set<Var>, greater<double>> m_Score2Vars; // 'greater' forces an order from large to small of the keys
	map<double, unordered_set<Var>, greater<double>>::iterator m_Score2Vars_it;
	unordered_set<Var>::iterator m_VarsSameScore_it;
	vector<double>	m_activity; // Var => activity
	double			m_var_inc;	// current increment of var score (it increases over time)
	double			m_curr_activity;
	bool			m_should_reset_iterators;

	unsigned int 
		nvars,			// # vars
		nclauses, 		// # clauses
		nlits,			// # literals = 2*nvars				
		qhead;			// index into trail. Used in BCP() to follow the propagation process.
	int					
		num_learned, 	
		num_decisions,
		num_assignments,
		num_restarts,
		dl,				// decision level
		max_dl,			// max dl seen so far since the last restart
		conflicting_clause_idx, // holds the index of the current conflicting clause in cnf[]. -1 if none.				
		restart_threshold,
		restart_lower,
		restart_upper;

	Lit 		asserted_lit;

	float restart_multiplier;
	
	// access	
	int get_learned() { return num_learned; }
	void set_nvars(int x) { nvars = x; }
	int get_nvars() { return nvars; }
	void set_nclauses(int x) { nclauses = x; }
	size_t cnf_size() { return cnf.size(); }
	VarState get_state(int x) { return state[x]; }

	// misc.
	void add_to_trail(int x) { trail.push_back(x); }

	void reset(); // initialization that is invoked initially + every restart
	void initialize();
	void reset_iterators(double activity_key = 0.0);	

	// solving	
	SolverState decide();
	void test();
	SolverState BCP();
	int  analyze(const Clause);
	inline int  getVal(Var v);
	inline void add_clause(Clause& c, int l, int r);
	inline void add_unary_clause(Lit l);
	inline void assert_lit(Lit l);	
	void m_rescaleScores(double& new_score);
	inline void backtrack(int k);
	void restart();
	
	// scores	
	inline void bumpVarScore(int idx);
	inline void bumpLitScore(int lit_idx);

public:
	Solver(): 
		nvars(0), nclauses(0), num_learned(0), num_decisions(0), num_assignments(0), 
		num_restarts(0), m_var_inc(1.0), qhead(0), 
		restart_threshold(Restart_lower), restart_lower(Restart_lower), 
		restart_upper(Restart_upper), restart_multiplier(Restart_multiplier)	 {};
	
	// service functions
	inline LitState lit_state(Lit l) {
		VarState var_state = state[l2v(l)];
		return var_state == VarState::V_UNASSIGNED ? LitState::L_UNASSIGNED : (Neg(l) && var_state == VarState::V_FALSE || !Neg(l) && var_state == VarState::V_TRUE) ? LitState::L_SAT : LitState::L_UNSAT;
	}
	inline LitState lit_state(Lit l, VarState var_state) {
		return var_state == VarState::V_UNASSIGNED ? LitState::L_UNASSIGNED : (Neg(l) && var_state == VarState::V_FALSE || !Neg(l) && var_state == VarState::V_TRUE) ? LitState::L_SAT : LitState::L_UNSAT;
	}
	void read_cnf(ifstream& in);

	SolverState _solve();
	void solve();
"""
