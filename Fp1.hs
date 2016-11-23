head' :: [a] -> a
head' (x:_) = x

tail' :: [a] -> [a]
tail' [] = []
tail' (_:xs) = xs

take' :: Int -> [a] -> [a]
take' 0 _ = []
take' _ [] = []
take' n (x:xs) = x:take' (n-1) xs

drop' :: Int -> [a] -> [a]
drop' _ [] = []
drop' 0 xs = xs
drop' n (x:xs) = drop' (n-1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' f (x:xs) | f x = x : (filter' f xs)
                 | otherwise = filter' f xs
				 
foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (l:ls) = foldl' f (f z l) ls

concat' :: [a]->[a]->[a]
concat' [] xs = xs
concat' (x:xs) ys = x:concat' xs ys

quickSort' [] = []
quickSort' (x:xs) = concat' (quickSort'(filter' (< x) xs)) (x:quickSort' (filter'(>= x) xs))