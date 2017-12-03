"""
Sample input:
5 3
89 90 78 93 80
90 91 85 88 86
91 92 83 89 90.5


Sample output:
90.0
91.0
82.0
90.0
85.5
"""


if __name__ == '__main__':

    N = map(int, raw_input('Enter a number of students and subjects: ').split())
    M = [map(float, raw_input('Enter a marks of students: ').split()) for i in range(N[1])]

    # Get marks of all subject for each student and calculate average score
    for elem in zip(*M):
        print sum(elem) / N[1]