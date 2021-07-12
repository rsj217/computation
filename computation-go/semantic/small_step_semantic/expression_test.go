package small_step_semantic

import (
	"fmt"
	assertLib "github.com/stretchr/testify/assert"
	"testing"
)

func TestNumber(t *testing.T) {
	assert := assertLib.New(t)

	number := Number{1}
	fmt.Println(number)
	assert.Equal(fmt.Sprintf("%s", number), "1")
}

func TestBoolean(t *testing.T) {
	assert := assertLib.New(t)

	boolean := Boolean{true}
	fmt.Println(boolean)
	assert.Equal(fmt.Sprintf("%s", boolean), "true")
}

func TestAdd(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = Add{Number{1}, Number{2}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 + 2")
	expr = expr.Reduce(nil)
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
	expr = expr.Reduce(nil)
	expr = expr.Reduce(nil)
	expr = expr.Reduce(nil)
	assert.Equal(fmt.Sprintf("%s", expr), "14")
}

func TestLessThan(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = LessThan{Number{1}, Number{2}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "1 < 2")

	expr = expr.Reduce(nil)
	assert.Equal(fmt.Sprintf("%v", expr), "true")
}

func TestAnd(t *testing.T) {
	assert := assertLib.New(t)

	var expr Exprer = And{Boolean{true}, LessThan{Number{1}, Number{2}}}
	fmt.Println(expr)
	assert.Equal(fmt.Sprintf("%s", expr), "true && 1 < 2")
	expr = expr.Reduce(nil)
	expr = expr.Reduce(nil)
	assert.Equal(fmt.Sprintf("%v", expr), "true")
}

func TestVariable(t *testing.T) {
	assert := assertLib.New(t)

	env := Env{"x": Number{1}}
	var expr Exprer = Variable{"x"}
	fmt.Println(expr)
	expr = expr.Reduce(env)
	assert.Equal(fmt.Sprintf("%v", expr), "1")
}
