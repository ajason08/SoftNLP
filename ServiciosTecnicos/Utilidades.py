def run(program="Start"):
    script = program+".py"
    with open(script) as f:
        c = compile(f.read(), script, 'exec')
        exec(c)

