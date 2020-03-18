from mathanim import Scene, Timecode, actions, sequences

with Scene() as scene:
    # FPS = 30
    sequence_a = sequences.Sequence(actions.Ramp(0, 1, 2), actions.Ramp(1, 0, 2))
    sequence_b = sequences.Sequence(sequence_a, actions.Ramp(3, 0, 6, func=lambda a, b, t: a + (b - a) * t**2))
    seq_accumulator = sequences.accumulate(actions.Ramp(0, 1, 2), actions.Ramp(1, 0, 3))
    print(seq_accumulator.get_value(3))