package denatation_semantic

import (
	assertLib "github.com/stretchr/testify/assert"
	"testing"
)

func TestGaussAlgo(t *testing.T) {
	assert := assertLib.New(t)
	lambda := GaussAlgo()

	assert.Equal(lambda, "(lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args))))(lambda wh: lambda e: e if (lambda e: (lambda e: e['i'])(e) < (lambda e: e['n'])(e))(e) is False else wh((lambda e: (lambda e: e | {'i': (lambda e: (lambda e: e['i'])(e) + (lambda e: 1)(e))(e)})((lambda e: e | {'sum': (lambda e: (lambda e: e['sum'])(e) + (lambda e: e['i'])(e))(e)})(e)))(e)))")
}
