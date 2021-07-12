package small_step_semantic

import "fmt"

type Stmter interface {
	Reducible() bool
	Reduce(env Env) (Stmter, Env)
}

type DoNothing struct{}

func (d DoNothing) String() string {
	return "do-nothing"
}

func (d DoNothing) Reducible() bool {
	return false
}

func (d DoNothing) Reduce(_ Env) (Stmter, Env) {
	panic("implement me")
}

type Assign struct {
	Name string
	Expr Exprer
}

func (a Assign) String() string {
	return fmt.Sprintf("%s = %v", a.Name, a.Expr)
}

func (a Assign) Reducible() bool {
	return true
}

func (a Assign) Reduce(env Env) (Stmter, Env) {
	if a.Expr.Reducible() {
		return Assign{a.Name, a.Expr.Reduce(env)}, env
	} else {
		env[a.Name] = a.Expr
		return DoNothing{}, env
	}
}

type If struct {
	Cond        Exprer
	Consequence Stmter
	Alternative Stmter
}

func (i If) String() string {
	return fmt.Sprintf("if (%s) {%v} else {%v}", i.Cond, i.Consequence, i.Alternative)
}

func (i If) Reducible() bool {
	return true
}

func (i If) Reduce(env Env) (Stmter, Env) {
	if i.Cond.Reducible() {
		return If{i.Cond.Reduce(env), i.Consequence, i.Alternative}, env
	} else {
		b := Boolean{true}
		if i.Cond.GetVal() == b.GetVal() {
			return i.Consequence, env
		} else { // i.Cond.GetVal() == NewBoolean(false).GetVal()
			return i.Alternative, env
		}
	}
}

type Sequence struct {
	First  Stmter
	Second Stmter
}

func (s Sequence) String() string {
	return fmt.Sprintf("%v;%v", s.First, s.Second)
}

func (s Sequence) Reducible() bool {
	return true
}

func (s Sequence) Reduce(env Env) (Stmter, Env) {
	if s.First.Reducible() {
		reduceFirst, reduceEnv := s.First.Reduce(env)
		return Sequence{reduceFirst, s.Second}, reduceEnv
	} else {
		return s.Second, env
	}
}

type While struct {
	Cond Exprer
	Body Stmter
}

func (w While) String() string {
	return fmt.Sprintf("while (%v) { %s }", w.Cond, w.Body)
}

func (w While) Reducible() bool {
	return true
}

func (w While) Reduce(env Env) (Stmter, Env) {
	return If{w.Cond, Sequence{w.Body, w}, DoNothing{}}, env
}
