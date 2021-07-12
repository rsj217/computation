package small_step_semantic

import "fmt"

type Machine struct {
	stmt Stmter
	env  map[string]Exprer
}

func NewMachine(stmt Stmter, env map[string]Exprer) *Machine {
	return &Machine{stmt: stmt, env: env}
}

func (m *Machine) Step() {
	m.stmt, m.env = m.stmt.Reduce(m.env)
}

func (m *Machine) Run() {
	for m.stmt.Reducible() {
		fmt.Println(m.stmt, m.env)
		m.Step()
	}
	fmt.Println(m.stmt, m.env)
}
