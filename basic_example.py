from mathanim import Scene, actions

with Scene() as scene:
    ramp = actions.Ramp(0, 1, 2)
    print(ramp.get_value(1))