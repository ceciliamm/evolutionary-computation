echo "Creating sphere.gif"
convert -delay 10 -loop 0 output/sphere/*.jpg GIFs/sphere.gif
echo "Creating ackley.gif"
convert -delay 10 -loop 0 output/ackley/*.jpg GIFs/ackley.gif
echo "Creating griewangk.gif"
convert -delay 10 -loop 0 output/griewangk/*.jpg GIFs/griewangk.gif