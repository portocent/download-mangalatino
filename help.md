### Remove small images
```
rm $(find . -iname "*.jpg" -type f | xargs -I{} identify -format '%w %h %i\n' {} | awk '$1<300 {print $3}')
```
### Delete empty folders
```
find . -type d -name 'Capitulo*' -empty -print -delete
```
### Converting into PDF
```
find . -type d -name "Mahou Tsukai No Yome*" | while read dir; do
  # Run the convert command inside the Mahou Tsukai No Yome* directory
  convert "$dir"/*.jpg "$dir.pdf"
done
```
