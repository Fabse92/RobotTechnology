unset border
set key center top reverse Left
set xzeroaxis
set yzeroaxis
set ytics axis
set xrange [ -5 : 10 ]
set yrange [ -5 : 10 ]

plot sample [*:0] 0, [0:*] 1*x+1+0.5*x**2
