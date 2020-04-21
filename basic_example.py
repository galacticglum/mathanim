from mathanim import Scene, Animation, Vector2, actions, sequences, objects

with Scene() as scene:
    box = objects.Rectangle(256, 256, fill_colour='magenta', stroke_colour='white', stroke_width=10, border_radius=10)
    scene.timeline.add(Animation(box, {
        'position.x': actions.Ramp(100, 1000, 3),
        'position.y': actions.Ramp(100, 1000, 3),
    }))

    scene.export('basic_example')