FILTER="Plain Text File (*.txt)"
TYPE="TEXT"

def save(data, path):
    file=open(path, "wt")
    file.write(data)
    file.close()


def load(path):
    file=open(path, "rt")
    data = file.read()
    file.close()
    return data