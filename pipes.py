PIPES = {
    'I_h': [1, 3],
    'I_v': [0, 2],
    'L_ur': [0, 1],
    'L_rd': [1, 2],
    'L_dl': [2, 3],
    'L_lu': [3, 0],
}
DRAG_OFFSET = 90

def get_pipe_for_dirs(d1, d2):
    for name, cons in PIPES.items():
        if sorted(cons) == sorted([d1, d2]):
            return name
    return 'I_h'