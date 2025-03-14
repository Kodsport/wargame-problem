#![recursion_limit = "∞"]

macro_rules! m {
    (S [-] [] [] $a:tt $b:tt $($c:tt)*) => { m!($b $a $($c)*) };
    (K [-] [] [] $a:tt $b:tt $($c:tt)*) => { m!($b $a $($c)*) };
    (I [S $($a:tt)*] $b:tt $c:tt $d:tt $e:tt $($f:tt)*) => { m!(I [$($a)*] $b $c $d $e $($f)*) };
    (B $a:tt [] $b:tt $c:tt $($d:tt)*) => { m!($c $a $($d)*) };
    (I [K $($a:tt)*] $b:tt $c:tt $d:tt $e:tt $($f:tt)*) => { m!(I [$($a)*-] $b $c $d $e $($f)*) };
    (D $a:tt [I] K $b:tt $($c:tt)*) => { m!($b $a $($c)*) };
    (I [I $($a:tt)*] $b:tt $c:tt $d:tt $e:tt $($f:tt)*) => { m!(I [$($a)*--] $b $c $d $e $($f)*) };
    (A $a:tt $b:tt $($c:tt)*) => { m!($b $a $($c)*) };
    (S [$($a:tt)*] [$b:tt $($c:tt)*] [$d:tt $($e:tt)*] $f:tt $($g:tt)*) => { m!(I [$b $d $($a)*] [$($c)*] [$($e)*] $f S $($g)*) };
    (K [$($a:tt)*] [$b:tt $($c:tt)*] [S $($d:tt)*] $e:tt $($f:tt)*) => { m!(I [$b -- $($a)*] [$($c)*] [$($d)*] $e K $($f)*) };
    (I [$($a:tt--)*] $b:tt $c:tt [$($d:tt)*] $e:tt $($f:tt)*) => { m!($e [$($a)*] $b $c [$($d)* K] $($f)*) };
    (B $a:tt [K $($b:tt)*] [$($c:tt)*] $($d:tt)*) => { m!(B $a [$($b)*] [K $($c)*] $($d)*) };
    (I [-$($a:tt--)*] $b:tt $c:tt [$($d:tt)*] $e:tt $($f:tt)*) => { m!($e [$($a)*] $b $c [$($d)* I] $($f)*) };
    (D $a:tt [I] S $b:tt $($c:tt)*) => { m!($b [I] $($c)*) };
    (I [--$($a:tt--)*] $b:tt $c:tt [$($d:tt)*] $e:tt $($f:tt)*) => { m!($e [-$($a)*] $b $c [$($d)* S] $($f)*) };
    (E $a:tt $b:tt $c:tt $($d:tt)*) => { m!($b $c $a $($d)*) };
    (K [$($a:tt)*] [$b:tt $($c:tt)*] [K $($d:tt)*] $e:tt $($f:tt)*) => { m!(I [$b - $($a)*] [$($c)*] [$($d)*] $e K $($f)*) };
    (S [$($a:tt)*] [$b:tt $($c:tt)*] [] $d:tt $($e:tt)*) => { m!(I [$b - $($a)*] [$($c)*] [] $d S $($e)*) };
    (K [$($a:tt)*] [$b:tt $($c:tt)*] [I $($d:tt)*] $e:tt $($f:tt)*) => { m!(I [$b $($a)*] [$($c)*] [$($d)*] $e K $($f)*) };
    (D $a:tt [K $($b:tt)+] K $($c:tt)*) => { m!(B [] $a $a E B [] $a D [$($b)+] K $($c)*) };
    (D $a:tt [K $($b:tt)+] S $($c:tt)*) => { m!(B [] $a $a E B [] $a D [$($b)+] S E B [] $a E B [] $a $($c)*) };
    (K [$($a:tt)*] [$b:tt $($c:tt)*] [] $d:tt $($e:tt)*) => { m!(I [$b - $($a)*] [$($c)*] [] $d K $($e)*) };
    (B $a:tt [I $($b:tt)*] [$($c:tt)*] $($d:tt)*) => { m!(S [-] $a [$($c)*] [] B [$($b)*] [K $($c)*] $($d)*) };
    (S [$($a:tt)*] [] [] $b:tt $($c:tt)*) => { m!(I [$($a)* --] [] [] $b S $($c)*) };
    (D $a:tt [I $($b:tt)+] K $($c:tt)*) => { m!(B [] $a $a E B [] $a D [$($b)+] K E B [] $a $($c)*) };
    (K [$($a:tt)*] [] [] $b:tt $($c:tt)*) => { m!(I [$($a)*--] [] [] $b K $($c)*) };
    (D $a:tt [I $($b:tt)+] S $($c:tt)*) => { m!(B [] $a $a E B [] $a D [$($b)+] K $($c)*) };
    (B $a:tt [S $($b:tt)*] [$($c:tt)*] $($d:tt)*) => { m!(K [-] $a [$($c)*] [] B [$($b)*] [K $($c)*] $($d)*) };
    (D $a:tt [S $($b:tt)+] K $($c:tt)*) => { m!(B [] $a $a E B [] $a D [$($b)+] S E B [] $a E B [] $a $($c)*) };
    (K $a:tt [] $b:tt $c:tt $($d:tt)*) => { m!(K $a [K] $b $c $($d)*) };
    (N $a:tt $b:tt $c:tt $d:tt $e:tt $f:tt $g:tt $h:tt $($i:tt)*) => { m!($b $c $d $e $f $g $h $a $($i)*) };
    (S [$($a:tt)*] [] [$b:tt $($c:tt)*] $d:tt $($e:tt)*) => { m!(I [$b - $($a)*] [$($c)*] [] $d S $($e)*) };
    (D $a:tt [S $($b:tt)+] S $($c:tt)*) => { m!(B [] $a $a E B [] $a D [$($b)+] S E B [] $a $($c)*) };
    (U [$(K)*]) => { println!("Correct flag!") };
    (U $a:tt) => { println!("That's not the flag!") };
}

macro_rules! n {
    ([$($a:tt)*] [A $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S S I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [B $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I I I K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [C $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I S K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [D $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K I K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [E $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K K I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [F $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S I K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [G $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [H $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [I $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I I I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [J $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S K S I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [K $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K I K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [L $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [M $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K S S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [N $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [O $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K I K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [P $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S I I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [Q $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [R $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [S $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S K I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [T $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [U $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [V $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [W $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [X $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [Y $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [Z $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S I I K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [a $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [b $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K I S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [c $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S K K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [d $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K K I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [e $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [f $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I I K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [g $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S I K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [h $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [i $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I I K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [j $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I I S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [k $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I S S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [l $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [m $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [n $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [o $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S K K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [p $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K I I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [q $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K K K S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [r $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [s $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [t $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S K I K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [u $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K S K K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [v $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I S S I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [w $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K K S I I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [x $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I K S S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [y $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [K S I S I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [z $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [S I S K I] K E B []] [$($b)*] $($d)*) };
    ([$($a:tt)*] [_ $($b:tt)*] $c:tt $($d:tt)*) => { n!([$($a)* N D $c [I S I S I] K E B []] [$($b)*] $($d)*) };

    ([$($a:tt)*] [] $($b:tt)*) => { m!($($a)* E K [-] [S S K S K S S K S S K S I I I I S S I I K I S K S K S K S S S S S S K I S I S I S K I K K S K I K I S S K S I S K S S S I S S S S I K S I S I S I K K S S K I K I S I I S S K I K S S S I I I K S K K I K S K I K I I S S K I S K I K I I I S K S I S K K S I I S K I K K I K K S K K S I K S K K K K K S I I I S K K K S I S K I I K I S K K S S S I K K I I K K I I I S I S I I I K K S S I K S K K K S I K S I S K I S K K K S S K I I I S I S I S I S I I S S K I K I I I K K I S K S I I K K S I S I I I S S I K S I I K K K K K K I K K I K I S K S K K K K K S K K K K S I K I S S K I I S I S S S I S K S S S S S I I K S K K I K K S S K I I I K S S K K S K K I S S K K S I K I K I I S I K K S I S K I I I K K I I I K K I I K I I I I K K K I K S S S I S I S S I S K S S S I K S K I K K K I K S I S I K S I K S S K K I K K K I S S I I I S K I K I K K I K K K I I I K K K I K K S K S K I K I S I I K S S I K K S K S K I I I I I I I I S S I I K I I S K I K S I S K K I I K I K S K I I K S K S K K K S S S S S K S S S K K S I S K K S I S K S K K K K I I I I S S S K I I K K K K I K I S I I K I S S K K K S S S S K S I I K S S I I I I S K I I I K I K S S K S I K K K I I K I I K S I I I S I S K I S S S I S S K S I I I S S S S K K S S I K I S I I K K S K S K K I S K K K K S I S I S K I I S S I S K K K S S I S I K I I I S S K I K S I K I K K I K S I K I I S I I K I S I K S S I S I K S K K I K S K S K K I I I I I S S I S S S S I I S K S I I I S K I I S S K K K S I K S K S K I S S I I K K I I K I I S K S K K I S K I I I S I K K S K S I S K S K S I I S I I I I K K I S I I S I I S I K S K K I K I I K S K I K K K S I S K I S I S S S I K S S S S I S K K K K I K I K I K I S S S S S S S K K K I S S I I S I S S K K K K I I S I K S K I I I S I S I I S K I I K I I I S K S I S K I I K S I I S S S I I I I S I S S S K S I I I S I I K K K I K K K I S K K I I S I K I K I S S I K I K I K S I S I K S S S S I I I K I S K S S S S I S S S I S S I I I I S I S S K I S I S S I I K S K K I S K S I I K I S I I K I S I I I S K I S K I S S K S K I I S I S S K K S S I I I I S K I S K I K S S S K S I K I I S S K I S K I I K S I S S K S I K I K K I K K I K K I K S I S K I S S I S S K K K S S S K I S K K K I S S K K K K S I I I S I K I K I S I S K I I S K I K K K S I K S I S S K I I K I K S I K I S K I S S S I K S S K S I I S K S I S S S K K I S K S K K S I K I S I K I K I S I I I K K K K K I I K K K I I I I S K S I S I K K S S S I I I K S S I I K S K K S S K I S S S S S K S S K K I K K K I I K K S K K S S K I I K K S I S I K I K I K I K I K S I S I S S S S I K S K S I I K K K I I S K K K K K I I K S S S I I I I I I I S S S K S K S I K I S K K S I S I K S I S K I K S K S S S K I S I S I S K K S S K I I I S S S S K K S S S K S I K I S K K K I S K S K K I S S I I S K K S S S S I I I I K I I K S K I S S S S K S S K K K S S I S S K K I K K K K I K I K S K S S I K S K S K K K K I S I I S I S I K I I S S I I I S K S K S S K S K S S S K S K K K K S I K K I I S I S K K S I S I S I S I K K I K I K I S S K K S S K S I S I I S K I K S K K K K K I I I I K I K S I S K I I K K I I S K I I I K K K S S I S S I I K S I I K S K I I K K S I S K S K K K K S S S S S S S I I K K K I S I S S I K K K I K I I I I K I K I S S S S K K K K I I I I K I S S S K S K S S K I S S K K S K S S S I I I K I K K I K I K S I I S S I K K S K K S S I K I S S I I I K K K K S I S I I S S K I I S K I K K S I I K K I I I K S I I K I I S I I K K K S S S K S I S I K I I I I K S I S K S I I I S S K S K K K K I K I S I S S K K S K K I I K I S I S K K K I K S S K K I S S K I I S I K S I S I I I K S K I K S I S K S K I S K I K K K I K I S I I I S I S I K S K I I K I I S K I K I K S S I K I I I K K K S I I I S K S K I S I S I S I S S K K I K S K I I I I K I K I I K K I K I K S I I K S K K S K S K I I K S S S K I I I K S S I I K I I I S I K S K K I K S K S I S K I S S I I S K I K K I K S S S S K K I K I S S I K K I K S S K I K I S I K K K I I K I K I S K S I I K I S K K I I S I S K K K K S I I I S S S I S I I I K S K S K I K K K K K I I S I K S I K I K K I K S I K I K S K I S S K S S I K I I K S S K I S S S K S S S K S I S K I I S K I S S I K K S I S I S K S K K S S I K I S I K K K K S K I S K I S I K K S I I S S K K S S S S I I I I I I S I I S S K I I K I S I K I I K K S S K S I I S S K I K S I S K I K I S K I K I I K K I S I K K S S K S S I I I I I I S S S S I K I S K I I S I I I I I K K K I I I I K I K S K I K S S S K K S S K K K S K I K S S S I S S S I S S S K S K S S K S S S I I S I S S I I S K S I S S S K K S I I S K I K I K K I K S S S I K I S I S S K K K I S K K I S K I I S K I I S I I K S I K S I S K S I K S K K S S I S S I K S I S S K I I I K I S I K S I K K I I K S K I I I I S K K I S S I S S K S K S I S I K I S K I I I S K S K I K S S S I S I S I K K K S I I S K S S I S K S S K S K S S K S S I I S S I K K S I S I S K I S I S S K S K I K I I K S S K I I K I S I S I K I S I K S I S I I S K I I K I S I K I S K I S K K I S K S S K K S K K S I S S I K I S I I S K K S I I S K I K K I S K K S K S S I K S I S K S I K S K S K S I I I S S S I I K S K I S S K I K S K I I S S K S K I K S I S K S K I I I S S S K I S S S S K I S K I K K I I I I I S S K K K S K K I K I K S I S K I K S I K K I S S S S S I S I I K S I S K K K K K I K K S S I S S I I K I S I I K K K S I S S K I K K S S K S K K K I S K I K K I K K I S S I I S I S K I S I I S I K I S K I S S I I K I S K I S S I I K I K K S S I S S S S K K I S S I I S I I S I I S K S S S K I S I K S I S I S S I S K K I K S K S S K I S K S S K I K K I S S K I S I K I S K I K K K K K S K I I I I K I K K S K K S I S K S I K K K S S K K S I I I S I I I K I K K S K S I I K I S K K S S K S S I I I K I S S S K I S K S K K K K I K S K S I S S I K I S S K I S S I S S K I K S I S S S K K S I S K K I I K S I I S S K S I K I S K I I S S S K I I S S I K S K I I I K I S K K K K I S S K I I S S I I I S S K K K K S K K I I S I S S S K S K K S I S S S K K S I I K K I S S I S K K I I I I S I K K S S K K K K K I S I K K S S I K S K I S I I K I K K S K S I I I I S K I I K K I K K K I I S I I S S K S I S S I S S S I I I K I K K I I K K S S S K S I K K S K I I S S K S S I I S S K I S K S K S I I K S K S I K S I I S K K I K K K K K K S K S K K I K K K S S S K K S S K S S K K K S I S I K I S S I S I K S K I I I S K K S I K K K I S K S S I K S S K S K I S S K S I K S S S S S I I S I S K S S K S S K I K S S K K K K I K S I I K S I K S S S S K K I K I S K S K K S K S I S K I I K I K S S S S I I S S I S I S I K K S S I K I I K K I I I S K S I S K S S I I I S I K K K I I S K I S I K K I I S K S I K K I S S S I S S I K S I I S I K K S S I K S S K I S I K K S K I S I K I S S K K K I I I K K K I K I S S S I S S S I S I K S K I I S I S S S K K I K K K I S S K S S K K K I S I I S K K K S K I K K S K I I I S K K K I K I S K S S K I K S S K K I I I I K I S K S K I I S S S I K S S K S S S K K K K K I K K S K S S I S K S K K K S S S I K S S K S S S K I K I K K I I S K I I I S I K K K K S I S S I S S S I S S S I K S S I I I K K I I I I K I S K K K I K K K S K K S I S S I S K S S S I S K I K S K K S K S S I S S I K I K S S K K K S K S I I K K K I K I I K S K I I I S K S I S K S K S S S K K K I S S S I K K I S K I S I S I S K K K S S I K I S S K S S S K I K I S I K S K I S K S I S I I I S I S I I S K K I S K I S K K S I I S I K I S I I K S I S K I I K I I I S I I S I I K S I S I I I K K K I I K I I K K S I I S I S I S I K K K S I I I K S I S S S I K K S S I K I I S I I K I S K I S S K I I S K I I K I S K S S I I S I S K I S I K I I K S S I S I S I K K S K S S I K K S K K S K I S I I I] [] U) };
}

macro_rules! input {
    (S N H T { $($input:tt)* }) => {
        n!([A [I]] [$($input)*] [I I K I] [S K S I] [I K S I] [I S I] [I K I I] [I S S S I] [I S K K I] [S S K I] [I K S K I] [S S I S I] [S I S S I] [S I I] [I S I S I] [I I I S I] [I I I] [I S S I I] [S I] [S S S S I] [I I S I I] [S S I] [S I K K I] [S K K S I] [S I S I I] [S K S K I] [S I K I] [S K I K I]);
    };
}

fn main() {
    input!(S N H T { R E D A C T E D });
}
