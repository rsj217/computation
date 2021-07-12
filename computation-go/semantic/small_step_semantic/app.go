package small_step_semantic

func GaussAlgo() map[string]Exprer {

	env := map[string]Exprer{
		"i":   Number{1},
		"n":   Number{101},
		"sum": Number{0},
	}

	stmt := While{
		Cond: LessThan{Variable{"i"}, Variable{"n"}},
		Body: Sequence{
			First:  Assign{"sum", Add{Variable{"sum"}, Variable{"i"}}},
			Second: Assign{"i", Add{Variable{"i"}, Number{1}}},
		},
	}

	m := NewMachine(stmt, env)
	m.Run()

	return env

}
