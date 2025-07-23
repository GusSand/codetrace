from processor import normalize_images


def __tmp2(__tmp0: <FILL>, outputdirectory):
    print('Input directory is {}.'.format(__tmp0))
    print('Output directory is {}.'.format(outputdirectory))

    normalize_images(__tmp0, outputdirectory)


def __tmp1():
    from argparse import ArgumentParser
    from argparse import ArgumentTypeError
    from os.path import isdir

    def directory_type(arg: str) -> str:
        if not isdir(arg):
            raise ArgumentTypeError('{} is not a directory'.format(arg))
        return arg

    parser = ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=directory_type,
                        help='the path to the input directory',
                        required=True)
    parser.add_argument('-o', '--output',
                        type=directory_type,
                        help='the path to the output directory',
                        required=True)
    args = parser.parse_args()

    __tmp2(args.input, args.output)


if __name__ == "__main__":
    __tmp1()
