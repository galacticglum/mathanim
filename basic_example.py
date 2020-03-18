from mathanim import Scene, actions, sequences

with Scene() as scene:
    sequence_a = sequences.Sequence(actions.Ramp(0, 1, 2), actions.Ramp(1, 0, 2))
    sequence_b = sequences.Sequence(sequence_a, actions.Ramp(3, 0, 6, func=lambda a, b, t: a + (b - a) * t**2))
    print(sequence_a.duration, sequence_b.duration)