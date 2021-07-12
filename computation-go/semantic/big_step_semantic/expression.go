package big_step_semantic

import (
	"fmt"
)

var Int2Bool = map[int]bool{
	0: false,
	1: true,
}

type Env map[string]Exprer

type Exprer interface {
	GetVal() int
	Evaluate(env Env) Exprer
}

type Number struct {
	val int
}

func (n Number) String() string {
	return fmt.Sprintf("%d", n.val)
}

func (n Number) GetVal() int {
	return n.val
}

func (n Number) Evaluate(_ Env) Exprer {
	return n
}

type Boolean struct {
	val bool
}

func (b Boolean) String() string {
	return fmt.Sprintf("%v", b.val)
}

func (b Boolean) GetVal() int {
	if b.val {
		return 1
	}
	return 0
}

func (b Boolean) Evaluate(_ Env) Exprer {
	return b
}

type Add struct {
	Left  Exprer
	Right Exprer
}

func (a Add) String() string {
	return fmt.Sprintf("%v + %v", a.Left, a.Right)
}

func (a Add) GetVal() int {
	panic("implement me")
}

func (a Add) Reducible() bool {
	return true
}

func (a Add) Evaluate(env Env) Exprer {
	return Number{a.Left.Evaluate(env).GetVal() + a.Right.Evaluate(env).GetVal()}
}

type Mul struct {
	Left  Exprer
	Right Exprer
}

func (m Mul) String() string {
	return fmt.Sprintf("%v * %v", m.Left, m.Right)
}

func (m Mul) GetVal() int {
	panic("implement me")
}

func (m Mul) Evaluate(env Env) Exprer {
	return Number{m.Left.Evaluate(env).GetVal() * m.Right.Evaluate(env).GetVal()}
}

type LessThan struct {
	Left  Exprer
	Right Exprer
}

func (lt LessThan) String() string {
	return fmt.Sprintf("%v < %v", lt.Left, lt.Right)
}

func (lt LessThan) GetVal() int {
	panic("implement me")
}

func (lt LessThan) Evaluate(env Env) Exprer {
	return Boolean{lt.Left.Evaluate(env).GetVal() < lt.Right.Evaluate(env).GetVal()}
}

type And struct {
	Left  Exprer
	Right Exprer
}

func (a And) String() string {
	return fmt.Sprintf("%v && %v", a.Left, a.Right)
}

func (a And) GetVal() int {
	panic("implement me")
}

func (a And) Evaluate(env Env) Exprer {
	left := Int2Bool[a.Left.Evaluate(env).GetVal()]
	right := Int2Bool[a.Right.Evaluate(env).GetVal()]
	return Boolean{left && right}
}

type Variable struct {
	Name string
}

func (v Variable) String() string {
	return fmt.Sprintf("%s", v.Name)
}

func (v Variable) GetVal() int {
	panic("implement me")
}

func (v Variable) Evaluate(env Env) Exprer {
	return env[v.Name]
}

