package big_step_semantic

import "fmt"

type Stmter interface {
	Evaluate(env Env) Env
}

type DoNothing struct{}

func (d DoNothing) String() string {
	return "do-nothing"
}

func (d DoNothing) Evaluate(env Env) Env {
	return env
}

type Assign struct {
	Name string
	Expr Exprer
}

func (a Assign) String() string {
	return fmt.Sprintf("%s = %v", a.Name, a.Expr)
}

func (a Assign) Evaluate(env Env) Env {
	env[a.Name] = a.Expr.Evaluate(env)
	return env
}

type If struct {
	Cond        Exprer
	Consequence Stmter
	Alternative Stmter
}

func (i If) String() string {
	return fmt.Sprintf("if (%s) {%v} else {%v}", i.Cond, i.Consequence, i.Alternative)
}

func (i If) Evaluate(env Env) Env {
	cond := i.Cond.Evaluate(env)
	switch cond.GetVal() {
	case Boolean{true}.GetVal():
		return i.Consequence.Evaluate(env)
	case Boolean{false}.GetVal():
		return i.Alternative.Evaluate(env)
	default:
		panic("error")
	}
}

type Sequence struct {
	First  Stmter
	Second Stmter
}

func (s Sequence) String() string {
	return fmt.Sprintf("%v;%v", s.First, s.Second)
}

func (s Sequence) Evaluate(env Env) Env {
	return s.Second.Evaluate(s.First.Evaluate(env))
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

func (w While) Reduce(env map[string]Exprer) (Stmter, map[string]Exprer) {
	return If{w.Cond, Sequence{w.Body, w}, DoNothing{}}, env
}

func (w While) Evaluate(env Env) Env {
	switch w.Cond.Evaluate(env).GetVal() {
	case Boolean{true}.GetVal():
		return w.Evaluate(w.Body.Evaluate(env))
	case Boolean{false}.GetVal():
		return env
	default:
		panic("error")
	}

}
