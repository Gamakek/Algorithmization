class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def find_max(root):
    if root is None:
        return float('-inf')

    return max(root.value, find_max(root.left), find_max(root.right)
    )

root = TreeNode(1)

root.left = TreeNode(3)
root.right = TreeNode(5)

root.left.left = TreeNode(8)
root.left.right = TreeNode(10)

root.left.left.left = TreeNode(14)
root.left.left.right = TreeNode(15)

root.left.right.right = TreeNode(3)

root.right.left = TreeNode(2)
root.right.right = TreeNode(6)

root.right.right.left = TreeNode(0)
root.right.right.right = TreeNode(1)

print(find_max(root))