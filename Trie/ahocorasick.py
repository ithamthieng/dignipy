'''ahocorasick.py

This module implements Aho-corasick Trie

Aho-corasick Trie
- can find patterns {A, B, C...} in Text efficiently
    - if n: length of text, m: length of each pattern
    - Brute-force method takes O(n * (m1 + m2 + m3 + ... + mk))
    - But, Aho-corasick takes O(n + m1 + m2 + ... mk)

Each nodes 
- have go-links and one failure-link(also called failure funciton)
- if it is the end of the pattern, is_ouput: True

'''
import collections

class AhoCorasickTrie():
    cnt = 0
    def __init__(self, key=None):
        AhoCorasickTrie.cnt += 1
        self.id = AhoCorasickTrie.cnt # for debugging
        self.key = key
        self.go = {}
        self.fail = None
        self.is_output = False
    
    def __repr__(self):
        fail_id = self.fail.id if self.fail else '@'
        return '{}@Node({}, {}, {})'.format(self.id, self.key, fail_id, self.is_output)
    
    @classmethod
    def insert_word_from(cls, root, word):
        cur_node = root
        for key in word:
            if key not in cur_node.go:
                new_node = AhoCorasickTrie(key)
                cur_node.go[key] = new_node
                cur_node = new_node
            else:
                cur_node = cur_node.go[key]
        cur_node.is_output = True
    
    @classmethod
    def set_failure_links(cls, root):
        Q = collections.deque() # for BFS
        root.fail = root;
        Q.append(root)
        while Q:
            # check 'current', 'next' node then set the failure, output link
            current = Q.popleft()
            for _, child_node in current.go.items():
                next = child_node
                if current == root:
                    next.fail = root
                else:
                    dest = current.fail
                    # go upward to find node which has next.key in its go link
                    while dest != root and not (next.key in dest.go):
                        dest = dest.fail
                    if next.key in dest.go:
                        dest = dest.go[next.key]
                    next.fail = dest
                # fail(x) = y, output(y) ⊂ output(x)
                if next.fail.is_output:
                    next.is_output = True
                Q.append(next)
        # End of while Q

    @classmethod
    def show_all_by_dfs(cls, node, level=0):
        print((' ' * 2 * level) + str(node))
        for _, child_node in node.go.items():
            cls.show_all_by_dfs(child_node, level + 1)
    
if __name__ == '__main__':
    patterns = ['a', 'ab', 'ac', 'adab', 'adada']
    root = AhoCorasickTrie()
    for pattern in patterns:
        AhoCorasickTrie.insert_word_from(root, pattern)
    
    print('Before Setting Failure Llink')
    print('--------------------------------------')
    AhoCorasickTrie.show_all_by_dfs(root)
    
    print('--------------------------------------')
    AhoCorasickTrie.set_failure_links(root)
    AhoCorasickTrie.show_all_by_dfs(root)
    

    
