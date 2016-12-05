import Prelude hiding (lookup)
data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup n (Node k v left right) | (k == n) = Just v
                               | (k > n)  = lookup n left
                               | (k < n)  = lookup n right
lookup _ _                                = Nothing


insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert key val (Node k v left right) | (key == k) = (Node key val left right)
                                     | (key > k)  = (Node k v left (insert key val right))
                                     | (key < k)  = (Node k v (insert key val left) right)
insert key val _                                  = (Node key val Nil Nil)


merge :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge (Node k v left right) tree  = merge (merge left right) (insert k v tree)
merge _ tree                      = tree


delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete key (Node k v left right)| (key == k) = merge left right
                                | (key > k)  = (Node k v left (delete key right))
                                | (key < k)  = (Node k v (delete key left) right)
delete key _                                 =  Nil