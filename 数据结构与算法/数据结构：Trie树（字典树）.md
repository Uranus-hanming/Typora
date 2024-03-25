[toc]

##### Trie树（字典树）

> 它是一个**树形结构**。它是一种**专门处理字符串匹配**的数据结构，用来解决在一组字符串集合中快速查找某个字符串的问题。
>
> Trie 树的本质，就是利用字符串之间的**公共前缀**，将重复的前缀合并在一起。
>
> Trie 树是一个**多叉树**。
>
> Trie 树的这个应用可以扩展到更加广泛的一个应用上，就是**自动输入补全**，比如输入法自动补全功能、IDE 代码编辑器自动补全功能、浏览器网址输入的自动补全功能等等。

```python
"""
    Author: Wenru Dong
"""


class TrieNode:
    def __init__(self, data: str):
        self._data = data
        self._children = [None] * 26
        self._is_ending_char = False


class Trie:
    def __init__(self):
        self._root = TrieNode("/")

    def insert(self, text: str) -> None:
        node = self._root
        for index, char in map(lambda x: (ord(x) - ord("a"), x), text):
            if not node._children[index]:
                node._children[index] = TrieNode(char)
            node = node._children[index]
        node._is_ending_char = True

    def find(self, pattern: str) -> bool:
        node = self._root
        for index in map(lambda x: ord(x) - ord("a"), pattern):
            if not node._children[index]: return False
            node = node._children[index]
        return node._is_ending_char


if __name__ == "__main__":

    strs = ["how", "hi", "her", "hello", "so", "see"]
    trie = Trie()
    for s in strs:
        trie.insert(s)

    for s in strs:
        print(trie.find(s))

    print(trie.find("swift"))
```

##### Tire树的实现

> Trie 树主要有两个操作，一个是**将字符串集合构造成 Trie 树**。这个过程分解开来的话，就是一个将字符串插入到 Trie 树的过程。另一个是**在 Trie 树中查询一个字符串**。

###### Tire树的存储

- 构建 Trie 树的过程，需要扫描所有的字符串，时间复杂度是 **O(n)**（n 表示所有字符串的长度和）。
- 构建好 Trie 树后，在其中查找字符串的时间复杂度是 **O(k)**，k 表示要查找的字符串的长度。