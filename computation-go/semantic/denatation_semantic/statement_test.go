package denatation_semantic

import (
	"fmt"
	assertLib "github.com/stretchr/testify/assert"
	"testing"
)

func TestAssign(t *testing.T) {
	assert := assertLib.New(t)
	expr := Add{Variable{"x"}, Number{2}}
	var stmt Stmter = Assign{"y", expr}
	fmt.Println(stmt)
	assert.Equal(fmt.Sprintf("%s", stmt), "y = x + 2")

	lambda := "lambda e: e | {'y': (lambda e: (lambda e: e['x'])(e) + (lambda e: 2)(e))(e)}"
	assert.Equal(stmt.ToPython(), lambda)
}

func TestIf(t *testing.T) {
	assert := assertLib.New(t)

	var stmt Stmter = If{
		Cond:        Variable{"x"},
		Consequence: Assign{"y", Number{1}},
		Alternative: Assign{"y", Number{2}},
	}
	assert.Equal(fmt.Sprintf("%v", stmt), "if (x) {y = 1} else {y = 2}")

	lambda := "lambda e: (lambda e: e | {'y': (lambda e: 1)(e)})(e) if (lambda e: e['x'])(e) else (lambda e: e | {'y': (lambda e: 2)(e)})(e)"
	assert.Equal(stmt.ToPython(), lambda)
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

	lambda := "lambda e: (lambda e: e | {'y': (lambda e: (lambda e: e['x'])(e) + (lambda e: 2)(e))(e)})((lambda e: e | {'x': (lambda e: (lambda e: 1)(e) + (lambda e: 1)(e))(e)})(e))"
	assert.Equal(stmt.ToPython(), lambda)
}

func TestWhile(t *testing.T) {
	assert := assertLib.New(t)

	name := "x"
	var stmt Stmter = While{
		Cond: LessThan{Variable{name}, Number{5}},
		Body: Assign{name, Mul{Variable{name}, Number{3}}},
	}
	stmtLiteral := fmt.Sprintf("%s", stmt)
	fmt.Println(stmtLiteral)
	assert.Equal(stmtLiteral, "while (x < 5) { x = x * 3 }")

	lambda := "(lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args))))(lambda wh: lambda e: e if (lambda e: (lambda e: e['x'])(e) < (lambda e: 5)(e))(e) is False else wh((lambda e: e | {'x': (lambda e: (lambda e: e['x'])(e) * (lambda e: 3)(e))(e)})(e)))"
	assert.Equal(stmt.ToPython(), lambda)
}
