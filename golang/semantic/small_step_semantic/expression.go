package small_step_semantic

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
	Reducible() bool
	Reduce(env Env) Exprer
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

func (n Number) Reducible() bool {
	return false
}

func (n Number) Reduce(env Env) Exprer {
	panic("implement me")
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

func (b Boolean) Reducible() bool {
	return false
}

func (b Boolean) Reduce(env Env) Exprer {
	panic("implement me")
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

func (a Add) Reduce(env Env) Exprer {
	if a.Left.Reducible() {
		return Add{a.Left.Reduce(env), a.Right}
	} else if a.Right.Reducible() {
		return Add{a.Left, a.Right.Reduce(env)}
	} else {
		return Number{a.Left.GetVal() + a.Right.GetVal()}
	}
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

func (m Mul) Reducible() bool {
	return true
}

func (m Mul) Reduce(env Env) Exprer {
	if m.Left.Reducible() {
		return Mul{m.Left.Reduce(env), m.Right}
	} else if m.Right.Reducible() {
		return Mul{m.Left, m.Right.Reduce(env)}
	} else {
		return Number{m.Left.GetVal() * m.Right.GetVal()}
	}
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

func (lt LessThan) Reducible() bool {
	return true
}

func (lt LessThan) Reduce(env Env) Exprer {
	if lt.Left.Reducible() {
		return LessThan{lt.Left.Reduce(env), lt.Right}
	} else if lt.Right.Reducible() {
		return LessThan{lt.Left, lt.Right.Reduce(env)}
	} else {
		return Boolean{lt.Left.GetVal() < lt.Right.GetVal()}
	}
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

func (a And) Reducible() bool {
	return true
}

func (a And) Reduce(env Env) Exprer {
	if a.Left.Reducible() {
		return And{a.Left.Reduce(env), a.Right}
	} else if a.Right.Reducible() {
		return And{a.Left, a.Right.Reduce(env)}
	} else {

		left := Int2Bool[a.Left.GetVal()]
		right := Int2Bool[a.Right.GetVal()]
		return Boolean{left && right}
	}
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

func (v Variable) Reducible() bool {
	return true
}

func (v Variable) Reduce(env Env) Exprer {
	return env[v.Name]
}
