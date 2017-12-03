if __name__ == '__main__':
    num = map(int, raw_input().split())
    print sorted(list(set(num)))[-2]


