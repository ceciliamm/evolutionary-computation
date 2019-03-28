"""Create schema from population."""

import schematax
import time


def compute_schemas(source, output):
    """Compute schemas."""
    print('Working with:', source)
    data = [l.strip('\n') for l in open(source, 'r')]
    start_time = time.time()
    schemas = schematax.complete(data)
    end_time = round(time.time() - start_time, 1)

    print('\tElapsed time:', end_time, 'seconds')
    print('\t{} schemas obtained'.format(len(schemas)))
    print('\tWriting result on:', output)

    out = open(output, 'w')
    out.write('schema,order,defining_length\n')
    for s in schemas:
        if str(s) != 'e':
            line = '{},{},{}\n'.format(str(s), s.get_order(), s.get_defining_length())
            out.write(line)

    print('Success!')


if __name__ == '__main__':
    for i in range(0, 101):
        in_file = '../data/individuals/{}.txt'.format(i)
        out_file = '../data/schemas/{}.schema'.format(i)
        compute_schemas(in_file, out_file)