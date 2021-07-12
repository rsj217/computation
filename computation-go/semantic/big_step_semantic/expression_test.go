package big_step_semantic

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
	expr = expr.Evaluate(nil)
	assert.Equal(fmt.Sprintf("%s", expr), "3")
}

func TestMul(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = Add{
		Mul{Number{1}, Number{2}},
		Mul{Number{3}, Number{4}},
	}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 * 2 + 3 * 4")
	expr = expr.Evaluate(nil)
	assert.Equal(fmt.Sprintf("%s", expr), "14")
}

func TestLessThan(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = LessThan{Number{1}, Number{2}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 < 2")
	expr = expr.Evaluate(nil)
	assert.Equal(fmt.Sprintf("%v", expr), "true")

}

func TestAnd(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = And{Boolean{true}, LessThan{Number{1}, Number{2}}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "true && 1 < 2")
	expr = expr.Evaluate(nil)
	assert.Equal(fmt.Sprintf("%v", expr), "true")
}

func TestVariable(t *testing.T) {
	assert := assertLib.New(t)

	env := Env{"x": Number{1}}
	var expr Exprer = Variable{"x"}
	fmt.Println(expr)
	expr = expr.Evaluate(env)
	assert.Equal(fmt.Sprintf("%v", expr), "1")
}

