from processor import normalize_images


def __tmp1(__tmp3, __tmp0: <FILL>):
    print('Input directory is {}.'.format(__tmp3))
    print('Output directory is {}.'.format(__tmp0))

    normalize_images(__tmp3, __tmp0)


def __tmp2():
    from argparse import ArgumentParser
    from argparse import ArgumentTypeError
    from os.path import isdir

    def __tmp4(arg: str) -> str:
        if not isdir(arg):
            raise ArgumentTypeError('{} is not a directory'.format(arg))
        return arg

    parser = ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=__tmp4,
                        help='the path to the input directory',
                        required=True)
    parser.add_argument('-o', '--output',
                        type=__tmp4,
                        help='the path to the output directory',
                        required=True)
    args = parser.parse_args()

    __tmp1(args.input, args.output)


if __name__ == "__main__":
    __tmp2()
