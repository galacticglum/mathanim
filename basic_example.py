from mathanim import Scene, Animation, Vector2, actions, sequences, objects

with Scene() as scene:
    box = objects.Rectangle(256, 256, fill_colour='magenta')
    scene.timeline.add(Animation(box, {
        'position.x': actions.Ramp(100, 1000, 3, func=lambda a, b, t: a + (b - a) * t**2),
        'position.y': actions.Ramp(100, 1000, 3, func=lambda a, b, t: a + (b - a) * t**2),
    }))

    scene.export('basic_example')