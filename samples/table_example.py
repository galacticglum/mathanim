'''
Animates a table similar to https://puu.sh/FkyQC/77bd3e83a7.gif.
'''

from mathanim import actions, sequences, objects, effects, Animation, Alignment

with mathanim.Scene(1920, 1080, fps=30) as scene:
    primes = [4, 25, 168, ...]
    table = objects.Table(
        objects.Table.Column(Alignment.Centre),
        objects.Table.Column(Alignment.Left),
        objects.Table.Column(Alignment.Left),
        objects.Table.Column(Alignment.Left)
        # A column by default will take up as much space as it needs (plus the padding); that is, 
        # it's base width is the width of largest element in the column.

        # You can also specify what percentage of the width it will take up using the width_percent kwarg.
    )
    
    # table.MergeColumns generates a directive indicating that the table should merge the following X columns...
    # For example, table.add_row(A, table.MergeColumns(B, 2), C) will create a layout where B occupies the 2 middle columns flanked by and A and C.
    # Note: merging rows is similar but is a property of the table.add_row method. Since table rows are built sequentially, 
    #   specifying the merge_rows kwarg of the table will merge the NEXT X rows...
    #   For example, table.add_row(..., merge_rows=2) will merge this row with the NEXT 2 rows, creating a layout where three rows are merged into one.
    header = objects.LatexText('\\textbf{Prime Densities}')
    table.add_row(table.MergeColumns(header, 4))
    table.add_horizontal_rule(style='solid')
    table.add_row(None, objects.LatexText('Range $(a, b)$'), objects.LatexText('Primes $(p)$'), objects.LatexText('Density $(d)$'))
    table.add_horizontal_rule(style='solid')

    for i in range(len(primes)):
        prime = primes[i]
        density = prime / 10**(i - 1)

        table.add_row(
            objects.LatexText('${}$'.format(i + 1)),
            objects.LatexText('$(0, 10^{})$'.format(i + 1)),
            objects.LatexText('${}$'.format(prime)),
            objects.LatexText('${}\%$'.format(density))
        )

        if i != len(primes) - 1:
            table.add_horizontal_rule(style='dashed')

    # timeline.add will, by default, append the animation to the end of the timeline (i.e. directly after the last animation).
    # You can specify a padding (using the padding kwarg), the number of seconds to pad between the two animations, 
    # or directly place the animation at a specific time (using the time kwarg)
    timeline.add(header.WriteAnimation)

    # Expand the horizontal width of the rule in 0.2 seconds
    # Animation.make_generic returns a new Animation type that can be reused. It is an altenative to creating a subclass.
    HorizontalRuleReveal = Animation.make_generic(
        # binds a sequence to a property of the animated object. The func kwarg provides a custom mapping function.
        # In this case, rather than simply using the value of the ramp as the width, we scale the width by that value.
        sequences.bind_to(actions.Ramp(0, 1, 0.2), 'width', func=lambda x, v: x * v)
    )

    # The angle of the linear wipe indicates the direction that it goes in, which can be thought as the 
    # positive y-axis (tail at origin) rotated clockwise. Thus, an angle of 0 means the linear wipe goes from BOTTOM to TOP.
    table.rows[1].add_effect(effects.LinearWipe(angle=90, feather=500), name='linear_wipe')
    # Add animations, in parallel. This will append all of the animations to the end of the timeline, starting at the same time.
    timeline.add(
        HorizontalRuleReveal(table.horizontal_rules[0]),
        Animation(table.rows[1], sequences.bind_to(actions.Ramp(0, 1, 0.2), 'effects.linear_wipe.percent_complete')),
        HorizontalRuleReveal(table.horizontal_rules[1]))

    # Get all the rows, excluding the header and column name row.
    table_body = objects.SceneObject().add_children(*table.rows[2:])
    table_body.add_effect(effects.LinearWipe(angle=180, feather=500), name='linear_wipe')
    timeline.add(Animation(table_body, sequences.bind_to(actions.Ramp(0, 1, 1.5), 'effects.linear_wipe.percent_complete')))
