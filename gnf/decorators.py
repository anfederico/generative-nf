def pretty_format(func):
    def formatting(*args, **kwargs):
        mls = func(*args, **kwargs)
        mlsl = mls.split('\n')
        l = len(mlsl[0]) - len(mlsl[0].lstrip())
        return '\n'.join([i[:l].lstrip(' ')+i[l:] for i in mlsl])
    return formatting