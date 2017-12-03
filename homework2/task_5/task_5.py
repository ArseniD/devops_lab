class Solution(object):
    def findWords(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """
        usa_keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        new_list = []

        for word in words:
            for letter_set in usa_keyboard:
                new_word = word.lower()
                if set(new_word).issubset(set(letter_set)):
                    new_list.append(word)
        return new_list


if __name__ == '__main__':

    assert Solution().findWords(["Hello", "Alaska", "Dad", "Peace"]) == ["Alaska", "Dad"]

    instance = Solution()
    print instance.findWords(["Hello", "Alaska", "Dad", "Peace"])
