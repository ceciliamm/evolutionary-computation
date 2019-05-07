echo "Creating mean.gif"
convert -delay 30 -loop 0 output/mean/*.jpg mean.gif
echo "Creating curves.gif"
convert -delay 10 -loop 0 output/curves/*.jpg curves.gif