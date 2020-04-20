from mathanim import Scene, Timecode, actions, sequences

with Scene() as scene:
    # FPS = 30
    sequence_a = sequences.Sequence(actions.Ramp(0, 1, 2), actions.Ramp(1, 0, 2))
    sequence_b = sequences.Sequence(sequence_a, actions.Ramp(3, 0, 6, func=lambda a, b, t: a + (b - a) * t**2))
    seq_accumulator = sequences.accumulate(actions.Ramp(0, 1, 2), actions.Ramp(1, 0, 3))

    class Transform:
        def __init__(self):
            self.position = 100

    class Test:
        def __init__(self):
            self.transform = Transform()

    test = Test()
    # Scale the position by the animated value (from 1 to 0 => from 100 to 0).
    bounded_sequence = sequences.bind_to(actions.Ramp(1, 0, 3), 'transform.position', func=lambda x, v: x * v)

    # simulate frames
    for frame in range(bounded_sequence.duration * scene.settings.fps + 1):
        seconds = frame / scene.settings.fps
        bounded_sequence.get_value(seconds, test)
        print(test.transform.position)
