from mathanim import Scene, Animation, actions, sequences

with Scene() as scene:
    sequence_a = sequences.Sequence(actions.Ramp(0, 1, 2), actions.Ramp(1, 0, 2))
    sequence_b = sequences.Sequence(sequence_a, actions.Ramp(3, 0, 6, func=lambda a, b, t: a + (b - a) * t**2))

    class TestObject:
        def __init__(self):
            self.position = 0
        
    obj = TestObject()
    scene.timeline.add(Animation(obj, {'position': sequence_b}))
    scene.timeline.add(Animation(obj, {'position': actions.Ramp(2, 1, 2)}))

    for frame_objects in scene.timeline:
        print('Position:', frame_objects[0].position)
        print('#######')