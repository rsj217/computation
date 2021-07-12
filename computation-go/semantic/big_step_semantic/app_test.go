package big_step_semantic

import (
	"fmt"
	assertLib "github.com/stretchr/testify/assert"
	"testing"
)

func TestGaussAlgo(t *testing.T) {
	assert := assertLib.New(t)
	env := GaussAlgo()

	assert.Equal(fmt.Sprintf("%s", env["sum"]), "5050")
}
