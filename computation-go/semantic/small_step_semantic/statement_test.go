package small_step_semantic

import (
	"fmt"
	assertLib "github.com/stretchr/testify/assert"
	"testing"
)

func TestAssign(t *testing.T) {
	assert := assertLib.New(t)

	name := "x"
	expr := Add{Variable{name}, Number{1}}
	env := Env{name: Number{2}}
	var stmt Stmter = Assign{name, expr}
	fmt.Println(stmt)
	assert.Equal(fmt.Sprintf("%s", stmt), "x = x + 1")

	assert.True(stmt.Reducible())
	stmt, env = stmt.Reduce(env)
	fmt.Println(stmt, env)

	assert.True(stmt.Reducible())
	stmt, env = stmt.Reduce(env)
	fmt.Println(stmt, env)

	assert.True(stmt.Reducible())
	stmt, env = stmt.Reduce(env)
	fmt.Println(stmt, env)

	assert.False(stmt.Reducible())
	assert.Equal(fmt.Sprintf("%v", env[name]), "3")
}

func TestAssign_Machine(t *testing.T) {
	assert := assertLib.New(t)

	name := "x"
	expr := Add{Variable{name}, Number{1}}
	env := Env{name: Number{2}}
	stmt := Assign{name, expr}

	assert.Equal(fmt.Sprintf("%v", stmt), "x = x + 1")
	m := NewMachine(stmt, env)
	m.Run()

	assert.False(m.stmt.Reducible())
	assert.Equal(fmt.Sprintf("%v", env[name]), "3")
}

func TestIf_Machine(t *testing.T) {
	assert := assertLib.New(t)

	env := Env{
		"x": Boolean{true},
	}
	var stmt Stmter = If{
		Cond:        Variable{"x"},
		Consequence: Assign{"y", Number{1}},
		Alternative: Assign{"y", Number{2}},
	}
	assert.Equal(fmt.Sprintf("%v", stmt), "if (x) {y = 1} else {y = 2}")

	m := NewMachine(stmt, env)
	m.Run()

	assert.False(m.stmt.Reducible())
	assert.Equal(fmt.Sprintf("%v", env["y"]), "1")


	env = Env{
		"x": Boolean{false},
	}

	m = NewMachine(stmt, env)

	m.Run()
	assert.Equal(fmt.Sprintf("%v", env["y"]), "2")
}

func TestSequence_Machine(t *testing.T) {
	assert := assertLib.New(t)

	env := Env{}
	var stmt Stmter = Sequence{
		First:  Assign{"x", Add{Number{1}, Number{1}}},
		Second: Assign{"y", Add{Variable{"x"}, Number{2}}},
	}

	m := NewMachine(stmt, env)
	m.Run()

	assert.False(m.stmt.Reducible())
	assert.Equal(fmt.Sprintf("%v", env["y"]), "4")
}

func TestWhile_Machine(t *testing.T) {
	assert := assertLib.New(t)

	name := "x"
	env := Env{name: Number{1}}
	var stmt Stmter = While{
		Cond: LessThan{Variable{name}, Number{5}},
		Body: Assign{name, Mul{Variable{name}, Number{3}}},
	}
	assert.Equal(fmt.Sprintf("%s", stmt), "while (x < 5) { x = x * 3 }")
	m := NewMachine(stmt, env)
	m.Run()

	assert.False(m.stmt.Reducible())
	assert.Equal(fmt.Sprintf("%v", env["x"]), "9")
}
