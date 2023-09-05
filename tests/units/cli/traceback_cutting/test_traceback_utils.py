from instld.cli.traceback_cutting.traceback_utils import count_traceback_lenth, cut_base_of_traceback


def test_count_traceback_lenth_empty():
    assert count_traceback_lenth(None) == 0


def test_count_traceback_lenth_not_empty():
    def function_3():
        raise ValueError
    def function_2():
        function_3()
    def function_1():
        function_2()

    try:
        function_1()
    except ValueError as e:
        assert count_traceback_lenth(e.__traceback__) == 4


def test_cut_base_of_traceback():
    def function_3():
        raise ValueError
    def function_2():
        function_3()
    def function_1():
        function_2()

    try:
        function_1()
    except ValueError as e:
        assert count_traceback_lenth(e.__traceback__) == 4

        cutted_traceback = cut_base_of_traceback(e.__traceback__, 0)

        assert count_traceback_lenth(cutted_traceback) == 4
        assert cutted_traceback is e.__traceback__

        cutted_traceback = cut_base_of_traceback(cutted_traceback, 1)

        assert count_traceback_lenth(cutted_traceback) == 3

        cutted_traceback = cut_base_of_traceback(cutted_traceback, 2)

        assert count_traceback_lenth(cutted_traceback) == 1

        cutted_traceback = cut_base_of_traceback(cutted_traceback, 1)

        assert count_traceback_lenth(cutted_traceback) == 0
        assert cutted_traceback is None
