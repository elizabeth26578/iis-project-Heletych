import clips

env = clips.Environment()

env.build(
    '(defrule hello => (printout t "CLIPS працює" crlf))'
)

env.run()