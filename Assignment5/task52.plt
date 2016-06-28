unset border
set key center top reverse Left
set xzeroaxis
set yzeroaxis
set ytics axis
set xrange [ -5 : 10 ]
set yrange [ -5 : 10 ]

set style line 20 lc rgb 'black' pt 7

plot (x**3-9*x**2+23*x-15)/-15 ,\
 (x**3-8*x**2+15*x)/8,\
 (x**3-6*x**2+5*x)/-12,\
 (x**3-4*x**2+3*x)/40,\
 23*x**3/40-19*x**2/5+209*x/40+1,\
 "<echo '0 1'"   with points ls 1, \
 "<echo '1 3'"   with points ls 1, \
 "<echo '3 -2'" with points ls 1,\
 "<echo '5 4'" with points ls 1


set term png size 960,480
set output "task52.png"
replot
set term x11
