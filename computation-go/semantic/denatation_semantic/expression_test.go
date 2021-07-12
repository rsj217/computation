package denatation_semantic

import (
	"fmt"
	assertLib "github.com/stretchr/testify/assert"
	"testing"
)

func TestNumber(t *testing.T) {
	assert := assertLib.New(t)

	var number Exprer = Number{1}
	fmt.Println(number)
	assert.Equal(fmt.Sprintf("%s", number), "1")

	number = number.Evaluate(nil)
	assert.Equal(fmt.Sprintf("%s", number), "1")

}

func TestBoolean(t *testing.T) {
	assert := assertLib.New(t)

	var boolean Exprer = Boolean{true}
	fmt.Println(boolean)
	assert.Equal(fmt.Sprintf("%s", boolean), "true")

	boolean = boolean.Evaluate(nil)
	assert.Equal(fmt.Sprintf("%s", boolean), "true")
}

func TestAdd(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = Add{Number{1}, Number{2}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 + 2")
	lambda := "lambda e: (lambda e: 1)(e) + (lambda e: 2)(e)"
	assert.Equal(expr.ToPython(), lambda)
}

func TestMul(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = Add{
		Mul{Number{1}, Number{2}},
		Mul{Number{3}, Number{4}},
	}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 * 2 + 3 * 4")
	lambda := "lambda e: (lambda e: (lambda e: 1)(e) * (lambda e: 2)(e))(e) + (lambda e: (lambda e: 3)(e) * (lambda e: 4)(e))(e)"
	assert.Equal(expr.ToPython(), lambda)
}

func TestLessThan(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = LessThan{Number{1}, Number{2}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 < 2")
	lambda := "lambda e: (lambda e: 1)(e) < (lambda e: 2)(e)"
	assert.Equal(expr.ToPython(), lambda)

}

func TestAnd(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = And{Boolean{true}, LessThan{Number{1}, Number{2}}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "true && 1 < 2")
	lambda := "lambda e: (lambda e: True)(e) and (lambda e: (lambda e: 1)(e) < (lambda e: 2)(e))(e)"
	assert.Equal(expr.ToPython(), lambda)
}

func TestVariable(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = Variable{"x"}
	fmt.Println(expr)
	lambda := expr.ToPython()
	ans := "lambda e: e['x']"
	assert.Equal(fmt.Sprintf("%v", lambda), ans)
}
