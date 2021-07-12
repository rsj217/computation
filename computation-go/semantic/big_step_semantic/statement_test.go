package big_step_semantic

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

	env = stmt.Evaluate(env)
	assert.Equal(fmt.Sprintf("%v", env[name]), "3")
}

func TestIf(t *testing.T) {
	assert := assertLib.New(t)

	env := map[string]Exprer{
		"x": Boolean{true},
	}
	var stmt Stmter = If{
		Cond:        Variable{"x"},
		Consequence: Assign{"y", Number{1}},
		Alternative: Assign{"y", Number{2}},
	}
	assert.Equal(fmt.Sprintf("%v", stmt), "if (x) {y = 1} else {y = 2}")

	env = stmt.Evaluate(env)
	assert.Equal(fmt.Sprintf("%v", env["y"]), "1")

	env = map[string]Exprer{
		"x": Boolean{false},
	}
	env = stmt.Evaluate(env)
	assert.Equal(fmt.Sprintf("%v", env["y"]), "2")
}

func TestSequence(t *testing.T) {
	assert := assertLib.New(t)

	env := map[string]Exprer{}
	var stmt Stmter = Sequence{
		First:  Assign{"x", Add{Number{1}, Number{1}}},
		Second: Assign{"y", Add{Variable{"x"}, Number{2}}},
	}

	env = stmt.Evaluate(env)
	stmtLiteral := fmt.Sprintf("%s", stmt)
	fmt.Println(stmtLiteral)
	assert.Equal(stmtLiteral, "x = 1 + 1;y = x + 2")
	assert.Equal(fmt.Sprintf("%v", env["y"]), "4")
}

func TestWhile(t *testing.T) {
	assert := assertLib.New(t)

	name := "x"
	env := Env{name: Number{1}}
	var stmt Stmter = While{
		Cond: LessThan{Variable{name}, Number{5}},
		Body: Assign{name, Mul{Variable{name}, Number{3}}},
	}
	stmtLiteral := fmt.Sprintf("%s", stmt)
	fmt.Println(stmtLiteral)
	assert.Equal(stmtLiteral, "while (x < 5) { x = x * 3 }")
	env = stmt.Evaluate(env)
	assert.Equal(fmt.Sprintf("%v", env["x"]), "9")
}
